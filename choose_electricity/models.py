# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class PricePlan(models.Model):
    
    PLAN_TYPE = (
        ('d', 'Discount'),
        ('f', 'Fixed'),
        ('p', 'Peak'),
        ('fl', 'Flat'),
        ('pd', 'PeakDiscount'),
    )

    SMART_METER = (
        ('y', 'Yes'),
        ('n', 'No'),
        ('o', 'Optional'),
    )

    provider = models.CharField('Provider', max_length = 50)
    plan_name = models.CharField('PlanName', max_length = 50)
    plan_id = models.CharField('PlanID', max_length = 50)
    plan_type = models.CharField('PlanType', max_length = 2, choices = PLAN_TYPE)
    discount = models.DecimalField('DiscountRate', max_digits = 10, decimal_places = 9)
    fixed_rate = models.DecimalField('FixedRate', max_digits = 10, decimal_places = 9)
    peak_rate_wd = models.DecimalField('PeakRate', max_digits = 10, decimal_places = 9) #wd = weekday
    offpeak_rate_wd = models.DecimalField('OffpeakRate', max_digits = 10, decimal_places = 9)
    peak_rate_we = models.DecimalField('PeakRate', max_digits = 10, decimal_places = 9)
    offpeak_rate_we = models.DecimalField('OffpeakRate', max_digits = 10, decimal_places = 9)
    peak_start_wd = models.DecimalField('PeakStart', max_digits = 2, decimal_places = 0)
    peak_end_wd = models.DecimalField('PeakEnd', max_digits = 2, decimal_places = 0)
    peak_start_we = models.DecimalField('PeakStart', max_digits = 2, decimal_places = 0)
    peak_end_we = models.DecimalField('PeakEnd', max_digits = 2, decimal_places = 0)
    monthly_fixed_cost = models.DecimalField('MonthlyFixedCost', max_digits = 15, decimal_places = 9)
    one_time_fixed_cost = models.DecimalField('One-TimeFixedCost', max_digits = 15, decimal_places = 9)
    other_cost_eqn = models.CharField('OtherCostEqn', max_length = 200)
    contract_period = models.DecimalField('ContractPeriod', max_digits = 2, decimal_places = 0)
    smart_meter = models.CharField('SmartMeter', max_length = 1, choices = SMART_METER)
    tlf = models.DecimalField('TLF', max_digits = 1, decimal_places = 0) # 1 = charged, 0 = absorbed
    late_charge = models.CharField('LatePaymentCharge', max_length = 200)
    early_termination_charge = models.CharField('EarlyTerminationCharge', max_length = 200)
    ami_fee = models.CharField('AMIInstallationFee', max_length = 200)
    security_deposit = models.CharField('SecurityDeposit', max_length = 200)
    clean_energy = models.DecimalField('CleanEnergy', max_digits = 10, decimal_places = 5)
    remarks = models.CharField('Remarks', max_length = 200)
    link = models.CharField('Link', max_length = 200)
    factsheet_date = models.CharField('FactsheetDate', max_length = 200)
                            

    def __str__(self):
        return self.provider + " " + self.plan_name

    def calc_monthly_bill(self, monthly_consumption = None, hourly_consumption = None,
                          current_tariff = 0, tlf_rate = 1.03493):
        """monthly_consumption should be an interger in kWh,
        hourly_consumption should be a list of 24 integers that correspond to
        average electricity consumption from 12-1am, 1-2am, ..., 11-12pm"""

        import decimal
        import sympy

        current_tariff = decimal.Decimal(current_tariff)
        monthly_consumption = decimal.Decimal(monthly_consumption)

        # Account for TLF
        hourly_consumption = [i * (1 + int(self.tlf)*(tlf_rate - 1)) for i in hourly_consumption]
        tlf_rate = decimal.Decimal(tlf_rate)
        monthly_consumption *= decimal.Decimal(1 + self.tlf*(tlf_rate - 1))
        
        # Calculate based on plan type
        if self.plan_type == "d":
            discount_tariff = current_tariff * (1 - self.discount)
            variable_cost  = monthly_consumption * discount_tariff
        elif self.plan_type == "f":
            variable_cost = monthly_consumption * self.fixed_rate
        elif self.plan_type == "fl":
            variable_cost = 0
        elif self.plan_type == "p":
            average_weekdays_in_a_month = decimal.Decimal(21.740625)
            average_days_in_a_month = decimal.Decimal(30.436875)
            average_weekends_in_a_month = average_days_in_a_month - average_weekdays_in_a_month
            
            peak_consumption_wd = decimal.Decimal(
                sum(hourly_consumption[int(self.peak_start_wd): int(self.peak_end_wd)]))
            offpeak_consumption_wd = decimal.Decimal(sum(hourly_consumption)) - peak_consumption_wd
            variable_cost_wd = (peak_consumption_wd * self.peak_rate_wd +
                                offpeak_consumption_wd * self.offpeak_rate_wd) * average_weekdays_in_a_month

            peak_consumption_we = decimal.Decimal(
                sum(hourly_consumption[int(self.peak_start_we): int(self.peak_end_we)]))
            offpeak_consumption_we = decimal.Decimal(sum(hourly_consumption)) - peak_consumption_we
            variable_cost_we = (peak_consumption_we * self.peak_rate_we +
                                offpeak_consumption_we * self.offpeak_rate_we) * average_weekends_in_a_month

            variable_cost = variable_cost_wd + variable_cost_we
        elif self.plan_type == "pd":
            average_weekdays_in_a_month = decimal.Decimal(21.740625)
            average_days_in_a_month = decimal.Decimal(30.436875)
            average_weekends_in_a_month = average_days_in_a_month - average_weekdays_in_a_month
            
            peak_rate_wd = (1 - self.peak_rate_wd) * current_tariff
            offpeak_rate_wd = (1 - self.offpeak_rate_wd) * current_tariff
            peak_rate_we = (1 - self.peak_rate_we) * current_tariff
            offpeak_rate_we = (1 - self.offpeak_rate_we) * current_tariff
            peak_consumption_wd = decimal.Decimal(
                sum(hourly_consumption[int(self.peak_start_wd): int(self.peak_end_wd)]))
            offpeak_consumption_wd = decimal.Decimal(sum(hourly_consumption)) - peak_consumption_wd
            variable_cost_wd = (peak_consumption_wd * peak_rate_wd +
                                offpeak_consumption_wd * offpeak_rate_wd) * average_weekdays_in_a_month

            peak_consumption_we = decimal.Decimal(sum(hourly_consumption[int(self.peak_start_we): int(self.peak_end_we)]))
            offpeak_consumption_we = decimal.Decimal(sum(hourly_consumption)) - peak_consumption_we
            variable_cost_we = (peak_consumption_we * peak_rate_we +
                                offpeak_consumption_we * offpeak_rate_we) * average_weekends_in_a_month

            variable_cost = variable_cost_wd + variable_cost_we
            
        if self.contract_period == 0:
            fixed_cost = self.one_time_fixed_cost/12 + self.monthly_fixed_cost
        else:
            fixed_cost = self.one_time_fixed_cost/self.contract_period + self.monthly_fixed_cost

        x = sympy.symbols('x') # x = monthly_consumption amount
        x1 = sympy.symbols('x1') # x1 = current variable cost
        other_cost = sympy.sympify(eval(self.other_cost_eqn)).subs(x, monthly_consumption).subs(x1, variable_cost)
                
        total_cost = variable_cost + fixed_cost + other_cost
        return total_cost


class SimplePricePlan(models.Model):
    
    PLAN_TYPE = (
        ('d', 'Discount'),
        ('f', 'Fixed'),
        ('p', 'Peak'),
        ('fl', 'Flat'),
        ('pd', 'PeakDiscount'),
    )

    SMART_METER = (
        ('y', 'Yes'),
        ('n', 'No'),
        ('o', 'Optional'),
    )

    provider = models.CharField('Provider', max_length = 50)
    plan_name = models.CharField('PlanName', max_length = 50)
    plan_id = models.CharField('PlanID', max_length = 50)
    plan_type = models.CharField('PlanType', max_length = 1, choices = PLAN_TYPE)
    discount = models.DecimalField('DiscountRate', max_digits = 10, decimal_places = 9)
    fixed_rate = models.DecimalField('FixedRate', max_digits = 10, decimal_places = 9)
    peak_rate_wd = models.DecimalField('PeakRate', max_digits = 10, decimal_places = 9) #wd = weekday
    other_cost_eqn = models.CharField('OtherCostEqn', max_length = 200)
    tlf = models.DecimalField('TLF', max_digits = 2, decimal_places = 1) # 1 = charged, 0 = absorbed
    
