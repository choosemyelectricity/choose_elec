from django import forms


class HourlyForm(forms.Form):
    
    twelveAM = forms.DecimalField(label = '12am - 1am')
    oneAM = forms.DecimalField(label = '1am - 2am')
    twoAM = forms.DecimalField(label = '2am - 3am')
    threeAM = forms.DecimalField(label = '3am - 4am')
    fourAM = forms.DecimalField(label = '4am - 5am')
    fiveAM = forms.DecimalField(label = '5am - 6am')
    sixAM = forms.DecimalField(label = '6am - 7am')
    sevenAM = forms.DecimalField(label = '7am - 8am')
    eightAM = forms.DecimalField(label = '8am - 9am')
    nineAM = forms.DecimalField(label = '9am - 10am')
    tenAM = forms.DecimalField(label = '10am - 11am')
    elevenAM = forms.DecimalField(label = '11am - 12pm')
    twelvePM = forms.DecimalField(label = '12pm - 1pm')
    onePM = forms.DecimalField(label = '1pm - 2pm')
    twoPM = forms.DecimalField(label = '2pm - 3pm')
    threePM = forms.DecimalField(label = '3pm - 4pm')
    fourPM = forms.DecimalField(label = '4pm - 5pm')
    fivePM = forms.DecimalField(label = '5pm - 6pm')
    sixPM = forms.DecimalField(label = '6pm - 7pm')
    sevenPM = forms.DecimalField(label = '7pm - 8pm')
    eightPM = forms.DecimalField(label = '8pm - 9pm')
    ninePM = forms.DecimalField(label = '9pm - 10pm')
    tenPM = forms.DecimalField(label = '10pm - 11pm')
    elevenPM = forms.DecimalField(label = '11pm - 12am')
    

class MonthlyForm(forms.Form):
    
    monthly_usage = forms.DecimalField(label = 'Monthly Usage (kWh)')


HOUSING_CHOICES = (
    ('oneRoom', 'HDB 1-Room'),
    ('twoRoom', 'HDB 2-Room'),
    ('threeRoom', 'HDB 3-Room'),
    ('fourRoom', 'HDB 4-Room'),
    ('fiveRoom', 'HDB 5-Room'),
    ('exec', 'HDB Executive'),
    ('apartm', 'Apartment'),
    ('terrace', 'Terrace'),
    ('semiD', 'Semi-Detached'),
    ('bung', 'Bungalow'),
    )

class HousingForm(forms.Form):

    housing = forms.ChoiceField(label = 'Housing Type', choices = HOUSING_CHOICES)

TOPIC_CHOICES = (
    ('missing', 'Missing providers or plan'),
    ('outdated', 'Outdated plan information'),
    ('calc', 'Calculation error'),
    ('enq', 'Enquiry'),
    ('feedbacl', 'Feedback'),
    ('oth', 'Others'),
    )

class ContactForm(forms.Form):

    topic = forms.ChoiceField(label = 'Topic', choices = TOPIC_CHOICES)
    email = forms.EmailField(label = 'Email', required = False)
    name = forms.CharField(label = 'Name')
    message = forms.CharField(label = 'Message', widget = forms.Textarea)


PROVIDER_CHOICES = (
    ('best', 'Best Electricity'),
    ('diamond', 'Diamond Electric'),
    ('geneco', 'Geneco'),
    ('hyflux', 'Hyflux Energy'),
    ('iswitch', 'iswitch'),
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

class FilterForm(forms.Form):

    provider = forms.MultipleChoiceField(label = 'Provider', choices = PROVIDER_CHOICES, widget=forms.CheckboxSelectMultiple)
    plan = forms.MultipleChoiceField(label = 'Plan Type', choices = PLAN_CHOICES, required = True)
    clean_energy = forms.ChoiceField(label = 'Clean Energy', choices = ENERGY_CHOICES)
    
