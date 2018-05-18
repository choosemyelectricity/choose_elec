# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.

from .models import PricePlan
from .forms import HourlyForm
from .forms import MonthlyForm
from .forms import HousingForm
from .forms import ContactForm
from .forms import FilterForm

CURRENT_TARIFF = 0.2215

AVERAGE_LOAD_PROFILE = [0.055654497,
                        0.050756901,
                        0.046749777,
                        0.043633126,
                        0.042297418,
                        0.043410508,
                        0.044968833,
                        0.042520036,
                        0.03762244,
                        0.033392698,
                        0.030721282,
                        0.029385574,
                        0.028495102,
                        0.028049866,
                        0.028495102,
                        0.02983081,
                        0.032279608,
                        0.03539626,
                        0.040293856,
                        0.045191451,
                        0.052760463,
                        0.058548531,
                        0.061442565,
                        0.058103295]

HOUSING_USAGE = {
    'oneRoom': 134.5833333,
    'twoRoom': 188.6666667,
    'threeRoom':270.5833333,
    'fourRoom':366,
    'fiveRoom':424.8333333,
    'exec':522.9166667,
    'apartm':530,
    'terrace':890.5,
    'semiD':1181.5,
    'bung':2402.75,
    }

PROVIDER_IMG = {
    'BEST ELECTRICITY SUPPLY PTE LTD': 'images/best.png',
    'DIAMOND ENERGY MERCHANTS PTE LTD': 'images/diamond.png',
    'I SWITCH PTE LTD': 'images/iswitch.png',
    'KEPPEL ELECTRIC PTE LTD': 'images/keppel.jpg',
    'OHM ENERGY PTE LTD': 'images/ohm.png',
    'PACIFICLIGHT ENERGY PTE LTD': 'images/pacific.png',
    'RED DOT POWER PTE LTD': 'images/reddot.jpg',
    'SEMBCORP POWER PTE LTD': 'images/sembcorp.jpg',
    'SENOKO ENERGY SUPPLY PTE LTD': 'images/senoko.jpg',
    'SERAYA ENERGY PTE LTD (GENECO)': 'images/geneco.png',
    'SUN ELECTRIC POWER PTE LTD': 'images/sun.png',
    'SUNSEAP ENERGY PTE LTD': 'images/sunseap.jpg',
    'TUAS POWER SUPPLY PTE LTD': 'images/tuas.jpg',
    }
    

def prepare_output(plan):
    provider = plan.provider
    provider = PROVIDER_IMG[provider]
    name = plan.plan_name
    plan_type = plan.plan_type
    remarks = plan.remarks
    date = plan.factsheet_date
    if remarks == '-':
        remarks = ''
    link = plan.link
    contract_period = plan.contract_period

    # Format plan summary
    if plan_type == 'd':
        dis = '{0:.2f}'.format(plan.discount*100)
        plan_type = 'DISCOUNT Plan'
        plan_summary = '{}% off regulated tariff'.format(dis)
    elif plan_type == 'f':
        rate = '{0:.2f}'.format(plan.fixed_rate*100)
        plan_type = 'FIXED RATE Plan'
        plan_summary = '{}cents/kWh'.format(rate)
    elif plan_type == 'p':
        peak = '{0:.2f}'.format(plan.peak_rate_wd*100)
        offpeak = '{0:.2f}'.format(plan.offpeak_rate_wd*100)
        plan_type = 'PEAK/OFFPEAK Plan'
        plan_summary = '{}cents/kWh peak rate, {}cents/kWh offpeak rate'.format(peak, offpeak)
    elif plan_type == 'fl':
        rate = '{0:.2f}'.format(plan.monthly_fixed_cost)
        plan_type = 'FLAT RATE Plan'
        plan_summary = '${} per month'.format(rate)
    elif plan_type == 'pd':
        peak = '{0:.2f}'.format(plan.peak_rate_wd*100)
        offpeak = '{0:.2f}'.format(plan.offpeak_rate_wd*100)
        plan_type = 'PEAK/OFFPEAK Discount Plan'
        plan_summary = '{}% peak discount, {}% offpeak discount'.format(peak, offpeak)

    # Format contract duration
    if contract_period == 0:
        contract_summary = 'No contract plan'
    else:
        contract_summary = '{} months contract'.format(contract_period)

    return [provider, name, plan_type, plan_summary, contract_summary, remarks, link, date]

def compare_bill(price_plans, monthly_consumption, hourly_consumption, current_tariff):
    """Given a list of price_plans, return a list of (plan, price) tuples sorted
    in increasing order or average monthly bill."""
    from operator import itemgetter
    output = []
    for plan in price_plans:
        bill = plan.calc_monthly_bill(monthly_consumption, hourly_consumption, current_tariff)
        plan_information = prepare_output(plan)
        output.append(plan_information+[bill])
    output = sorted(output,key=itemgetter(8))
    for i in output:
        i[8] = '{0:.2f}'.format(i[8])
    return output

def get_monthly_consumption_from_hourly(hourly_consumption):
    average_days_in_a_month = 30.436875
    daily_consumption = sum(hourly_consumption)
    average_monthly_consumption = average_days_in_a_month * daily_consumption
    return average_monthly_consumption

def get_hourly_consumption_from_monthly(monthly_consumption):
    average_days_in_a_month = 30.436875
    daily_consumption = monthly_consumption/average_days_in_a_month
    hourly_consumption = [prop*daily_consumption for prop in AVERAGE_LOAD_PROFILE]
    return hourly_consumption


def index(request):
    return render(
        request,
        'index.html',
        context = {}

    )

def hourly_form(request):
    
    if request.method == 'POST':
        form = HourlyForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            hourly_consumption = []
            hourly_consumption.append(data['a'])
            hourly_consumption.append(data['b'])
            hourly_consumption.append(data['c'])
            hourly_consumption.append(data['d'])
            hourly_consumption.append(data['e'])
            hourly_consumption.append(data['f'])
            hourly_consumption.append(data['g'])
            hourly_consumption.append(data['h'])
            hourly_consumption.append(data['i'])
            hourly_consumption.append(data['j'])
            hourly_consumption.append(data['k'])
            hourly_consumption.append(data['l'])
            hourly_consumption.append(data['m'])
            hourly_consumption.append(data['n'])
            hourly_consumption.append(data['o'])
            hourly_consumption.append(data['p'])
            hourly_consumption.append(data['q'])
            hourly_consumption.append(data['r'])
            hourly_consumption.append(data['s'])
            hourly_consumption.append(data['t'])
            hourly_consumption.append(data['u'])
            hourly_consumption.append(data['v'])
            hourly_consumption.append(data['w'])
            hourly_consumption.append(data['x'])

            hourly_consumption = [float(i) for i in hourly_consumption]
            
            request.session['hourly_consumption'] = hourly_consumption

            return redirect('/index/output/')
    else:
        form = HourlyForm()

    return render(
        request,
        'hourly_form.html',
        context = {'form': form}

    )

def monthly_form(request):
    
    if request.method == 'POST':
        form = MonthlyForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            monthly_consumption = data['monthly_usage']
            monthly_consumption = float(monthly_consumption)            
            hourly_consumption = get_hourly_consumption_from_monthly(monthly_consumption)

            request.session['hourly_consumption'] = hourly_consumption

            return redirect('/index/output/')
    else:
        form = MonthlyForm()

    return render(
        request,
        'monthly_form.html',
        context = {'form': form}
    )

def housing_form(request):

    if request.method == 'POST':
        form = HousingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            housing = data['housing']
            monthly_consumption = HOUSING_USAGE[housing]
            hourly_consumption = get_hourly_consumption_from_monthly(monthly_consumption)

            request.session['hourly_consumption'] = hourly_consumption

            return redirect('/index/output/')
    else:
        form = HousingForm()

    return render(
        request,
        'housing_form.html',
        context = {'form': form}
    )


def output(request):

    hourly_consumption = request.session['hourly_consumption']
    monthly_consumption = get_monthly_consumption_from_hourly(hourly_consumption)
    
    PROVIDER_CHOICES = (
        ('best', 'Best Electricity'),
        ('diamond', 'Diamond Electric'),
        ('geneco', 'Geneco'),
        ('hyflux', 'Hyflux Energy'),
        ('i switch', 'iswitch'),
        ('keppel', 'Keppel Electric'),
        ('ohm', 'Ohm'),
        ('pacific', 'Pacific Light'),
        ('reddot', 'RedDotPower'),
        ('sembcorp', 'Sembcorp'),
        ('senoko', 'Senoko'),
        ('sun electric', 'Sun Electric'),
        ('sunseap', 'Sunseap'),
        ('tuas', 'Tuas'),
        )

    PLAN_CHOICES = (
        ('d', 'Discount'),
        ('f', 'Fixed Rate'),
        ('p', 'Peak/Off Peak'),
        ('o', 'Others'),
        )

    ENERGY_CHOICES = (
        ('no_pref', 'No Preference'),
        ('some_pref', 'Partially clean'),
        ('full', '100% clean'),
        )

    filters = {'providers': PROVIDER_CHOICES,
               'plans': PLAN_CHOICES,
               'energy': ENERGY_CHOICES}
    
    if request.method == 'POST':
        providers = request.POST.getlist('providers')
        plan = request.POST.getlist('plans')
        clean_energy = request.POST.get('energy')

        previous_filters = {'providers': providers, 'plan': plan, 'clean_energy': clean_energy}

        import operator
        import decimal
        from django.db.models import Q

        # Filter by providers

        if providers:
            query = reduce(operator.or_, (Q(provider__icontains = i) for i in providers))
            price_plans = PricePlan.objects.filter(query)
        else:
            price_plans = PricePlan.objects.all()
        
        # Filter by plan types
        if 'p' in plan and 'pd' not in plan:
            plan.append('pd')
        if plan:
            query = reduce(operator.or_, (Q(plan_type__exact = i) for i in plan))
            price_plans = price_plans.filter(query)

        # Filter by clean_energy:
        if clean_energy == 'some_pref':
            price_plans = price_plans.filter(clean_energy__gt = decimal.Decimal('0.0'))
        elif clean_energy == 'full':
            price_plans = price_plans.filter(clean_energy__exact = decimal.Decimal('100'))

        price_plans = list(price_plans)
    else:
        previous_filters = {'providers': [], 'plan': [], 'clean_energy': 'no_pref'}
        price_plans = list(PricePlan.objects.all())
      
    output = compare_bill(price_plans, monthly_consumption, hourly_consumption, CURRENT_TARIFF)
    return render(
        request,
        'output.html',
        context = {'output': output, 'filters': filters, 'previous_filters': previous_filters}
    )

from django.core.mail import BadHeaderError, EmailMessage
from django.http import HttpResponse

def contact(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            topic = data['topic']
            email = data['email']
            name = data['name']
            message = data['message']
            body = name + " " + message
            try:
                email_msg = EmailMessage(topic, body, email,
                                         ['choosemyelectricity@gmail.com'],
                                         reply_to=[email])
                email_msg.send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            return render(
                request,
                'contact_thanks.html',
                context = {}
            )
    else:
        form = ContactForm()
    return render(
        request,
        'contact.html',
        context = {'form': form}
    )
