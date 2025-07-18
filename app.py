from flask import Flask, render_template, request, session
import os
from datetime import timedelta, datetime, timezone

import extract_gbp
import extract_usd
import extract_aud
import extract_eur

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.permanent_session_lifetime = timedelta(seconds=30)


@app.route('/', methods=['GET', 'POST'])
def home():

    now = datetime.now()
    session['last_activity'] = now

    usd_rate = extract_usd.extract_usd()
    usd_rate = float(usd_rate)

    eur_rate = extract_eur.extract_eur()
    eur_rate = float(eur_rate)

    gbp_rate = extract_gbp.extract_gbp()
    gbp_rate = float(gbp_rate)

    aud_rate = extract_aud.extract_aud()
    aud_rate = float(aud_rate)

    lkr_rate = float(1.00)
    


    if request.method == 'POST':
        
        basic_currency = request.form['basic_currency']
        basic_exchange_rate = request.form['basic_exchange_rate']
        basic_salary = request.form['basic_salary']

        allowances_currency = request.form['allowances_currency']
        allowances_exchange_rate = request.form['allowances_exchange_rate']
        allowances = request.form['allowances']

        deductions_currency = request.form['deductions_currency']
        deductions_exchange_rate = request.form['deductions_exchange_rate']
        deductions = request.form['deductions']


        if not basic_salary:
            basic_salary = 0

        if not allowances:
            allowances = 0

        if not deductions:
            deductions = 0

        # Formatting assigned values

        basic_currency = str(basic_currency)
        basic_exchange_rate = float(basic_exchange_rate)
        basic_salary = float(basic_salary)

        allowances_currency = str(allowances_currency)
        allowances_exchange_rate = float(allowances_exchange_rate)
        allowances = float(allowances)

        deductions_currency = str(deductions_currency)
        deductions_exchange_rate = float(deductions_exchange_rate)
        deductions = float(deductions)

        session['basic_currency'] = basic_currency
        session['basic_exchange_rate'] = basic_exchange_rate
        session['basic_salary'] = basic_salary

        session['allowances_currency'] = allowances_currency
        session['allowances_exchange_rate'] = allowances_exchange_rate
        session['allowances'] = allowances

        session['deductions_currency'] = deductions_currency
        session['deductions_exchange_rate'] = deductions_exchange_rate
        session['deductions'] = deductions



        # Calculating & Formatting annual_salary

        converted_basic = basic_salary * basic_exchange_rate
        converted_allowances = allowances * allowances_exchange_rate
        converted_deductions = deductions * deductions_exchange_rate

        converted_annual = (converted_basic + converted_allowances - converted_deductions) * 12
        converted_annual_for_old_tax = converted_basic * 12


        # Formatting converted values

        converted_annual = int(converted_annual)
        converted_basic = int(converted_basic)
        converted_allowances = int(converted_allowances)
        converted_deductions = int(converted_deductions)


        # Calculating OLD Income Tax (2023 January 01 - 2025 March 31)

        if converted_annual_for_old_tax in range(0, 1200001):
            old_income_tax = 0
        elif converted_annual_for_old_tax in range(1200000, 1700001):
            old_income_tax = ((converted_annual_for_old_tax - 1200000) / 12) * 0.06
        elif converted_annual_for_old_tax in range(1700000, 2200001):
            old_income_tax = (500000 / 12) * 0.06 + ((converted_annual_for_old_tax - 1700000) / 12) * 0.12
        elif converted_annual_for_old_tax in range(2200000, 2700001):
            old_income_tax = (500000 / 12) * 0.06 + (500000 / 12) * 0.12 + ((converted_annual_for_old_tax - 2200000) / 12) * 0.18
        elif converted_annual_for_old_tax in range(2700000, 3200001):
            old_income_tax = (500000 / 12) * 0.06 + (500000 / 12) * 0.12 + (500000 / 12) * 0.18 + (
                        (converted_annual_for_old_tax - 2700000) / 12) * 0.24
        elif converted_annual_for_old_tax in range(3200000, 3700001):
            old_income_tax = (500000 / 12) * 0.06 + (500000 / 12) * 0.12 + (500000 / 12) * 0.18 + (500000 / 12) * 0.24 + (
                        (converted_annual_for_old_tax - 3200000) / 12) * 0.30
        else:
            old_income_tax = (500000 / 12) * 0.06 + (500000 / 12) * 0.12 + (500000 / 12) * 0.18 + (500000 / 12) * 0.24 + (
                        500000 / 12) * 0.30 + ((converted_annual_for_old_tax - 3700000) / 12) * 0.36


        # Calculating NEW Income Tax (2025 April 01 Onwards)

        if converted_annual in range(0, 1800001):
            income_tax = 0
        elif converted_annual in range(1800000, 2800001):
            income_tax = ((converted_annual - 1800000) / 12) * 0.06
        elif converted_annual in range(2800000, 3300001):
            income_tax = (1000000 / 12) * 0.06 + ((converted_annual - 2800000) / 12) * 0.18
        elif converted_annual in range(3300000, 3800001):
            income_tax = (1000000 / 12) * 0.06 + (500000 / 12) * 0.18 + ((converted_annual - 3300000) / 12) * 0.24
        elif converted_annual in range(3800000, 4300001):
            income_tax = (1000000 / 12) * 0.06 + (500000 / 12) * 0.28 + (500000 / 12) * 0.24 + (
                        (converted_annual - 3800000) / 12) * 0.30
        else:
            income_tax = (1000000 / 12) * 0.06 + (500000 / 12) * 0.18 + (500000 / 12) * 0.24 + (500000 / 12) * 0.30 + (
                        (converted_annual - 4300000) / 12) * 0.36

        # Calculating EPF/ETF Deductions

        epf_etf_amount = (converted_basic * 20 / 100) + (converted_allowances * 3 / 100)
        epf_8_amount = (converted_basic * 8 / 100)


        # Calculating Final Net Salary

        net_salary = (converted_basic + converted_allowances - income_tax - epf_8_amount) - converted_deductions


        # Calculating Saved Income Tax

        saved_income_tax = old_income_tax - income_tax


        # Formatting final outputs and return values

        net_salary = round(net_salary,2)
        income_tax = round(income_tax,2)
        old_income_tax = round(old_income_tax,2)
        saved_income_tax = round(saved_income_tax,2)
        epf_etf_amount = round(epf_etf_amount,2)
        epf_8_amount = round(epf_8_amount,2)

        net_salary = str(net_salary)
        income_tax = str(income_tax)
        old_income_tax = str(old_income_tax)
        saved_income_tax = str(saved_income_tax)
        epf_etf_amount = str(epf_etf_amount)
        epf_8_amount = str(epf_8_amount)

        net_salary = 'LKR ' + net_salary
        income_tax = 'LKR ' + income_tax
        old_income_tax = 'LKR ' + old_income_tax
        saved_income_tax = 'LKR ' + saved_income_tax
        epf_etf_amount = 'LKR ' + epf_etf_amount
        epf_8_amount = 'LKR ' + epf_8_amount


        return render_template('output.html', 
                               net_salary=net_salary, 
                               income_tax=income_tax, 
                               old_income_tax=old_income_tax,
                               saved_income_tax=saved_income_tax,
                               epf_8_amount=epf_8_amount, 
                               epf_etf_amount=epf_etf_amount,
                               usd_rate=usd_rate,
                               eur_rate=eur_rate,
                               gbp_rate=gbp_rate,
                               aud_rate=aud_rate,
                               lkr_rate=lkr_rate)
    
    # Check session timeout
    now = datetime.now()
    
    if 'last_activity' in session and (now - session['last_activity']).seconds > app.permanent_session_lifetime.seconds:
        session.clear()

    # Update last activity time
    session['last_activity'] = now.replace(tzinfo=timezone.utc)

    return render_template('index.html', 
                           basic_currency=session.get('basic_currency'),
                           basic_exchange_rate=session.get('basic_exchange_rate'),
                           basic_salary=session.get('basic_salary'),
                           allowances_currency=session.get('allowances_currency'),
                           allowances_exchange_rate=session.get('allowances_exchange_rate'),
                           allowances=session.get('allowances'),
                           deductions_currency=session.get('deductions_currency'),
                           deductions_exchange_rate=session.get('deductions_exchange_rate'),
                           deductions=session.get('deductions'),
                           usd_rate=usd_rate,
                           eur_rate=eur_rate,
                           gbp_rate=gbp_rate,
                           aud_rate=aud_rate,
                           lkr_rate=lkr_rate)


if __name__ == '__main__':
    app.run(debug=True)
