from flask import Flask, render_template, request, session

import extract_gbp
import extract_usd
import extract_aud
import extract_eur

# Set to store unique IP addresses
unique_visitors = set()

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':
        basic_salary = request.form['basic_salary']
        allowances = request.form['allowances']
        deductions = request.form['deductions']
        currency = request.form['currency']

        if not basic_salary:
            basic_salary = 0

        if not allowances:
            allowances = 0

        if not deductions:
            deductions = 0

        if not currency:
            currency = 'LKR'

        # Formatting assigned values

        basic_salary = int(basic_salary)
        allowances = int(allowances)
        deductions = int(deductions)
        currency = str(currency)

        session['basic_salary'] = basic_salary
        session['allowances'] = allowances
        session['deductions'] = deductions
        session['currency'] = currency

        # Calculating & Formatting annual_salary

        annual_salary = (basic_salary + allowances) * 12
        annual_salary = int(annual_salary)


        # Converting USD to LKR

        if currency == 'USD':

            usd_rate = extract_usd.extract_usd()
            usd_rate = float(usd_rate)

            converted_annual = annual_salary*usd_rate
            converted_basic = basic_salary*usd_rate
            converted_allowances = allowances*usd_rate
            converted_deductions = deductions*usd_rate


        # Converting EUR to LKR

        if currency == 'EUR':

            eur_rate = extract_eur.extract_eur()
            eur_rate = float(eur_rate)

            converted_annual = annual_salary*eur_rate
            converted_basic = basic_salary*eur_rate
            converted_allowances = allowances*eur_rate
            converted_deductions = deductions*eur_rate


        # Converting GBP to LKR

        if currency == 'GBP':

            gbp_rate = extract_gbp.extract_gbp()
            gbp_rate = float(gbp_rate)

            converted_annual = annual_salary*gbp_rate
            converted_basic = basic_salary*gbp_rate
            converted_allowances = allowances*gbp_rate
            converted_deductions = deductions*gbp_rate


        # Converting AUD to LKR

        if currency == 'AUD':

            aud_rate = extract_aud.extract_aud()
            aud_rate = float(aud_rate)

            converted_annual = annual_salary*aud_rate
            converted_basic = basic_salary*aud_rate
            converted_allowances = allowances*aud_rate
            converted_deductions = deductions*aud_rate


        # Converting AUD to LKR

        if currency == 'LKR':

            lkr_rate = float(1.00)

            converted_annual = annual_salary*lkr_rate
            converted_basic = basic_salary*lkr_rate
            converted_allowances = allowances*lkr_rate
            converted_deductions = deductions*lkr_rate


        # Formatting converted values

        converted_annual = int(converted_annual)
        converted_basic = int(converted_basic)
        converted_allowances = int(converted_allowances)
        converted_deductions = int(converted_deductions)


        # Calculating Income Tax

        if converted_annual in range(0, 1200001):
            income_tax = 0
        elif converted_annual in range(1200000, 1700001):
            income_tax = ((converted_annual - 1200000) / 12) * 0.06
        elif converted_annual in range(1700000, 2200001):
            income_tax = (500000 / 12) * 0.06 + ((converted_annual - 1700000) / 12) * 0.12
        elif converted_annual in range(2200000, 2700001):
            income_tax = (500000 / 12) * 0.06 + (500000 / 12) * 0.12 + ((converted_annual - 2200000) / 12) * 0.18
        elif converted_annual in range(2700000, 3200001):
            income_tax = (500000 / 12) * 0.06 + (500000 / 12) * 0.12 + (500000 / 12) * 0.18 + (
                        (converted_annual - 2700000) / 12) * 0.24
        elif converted_annual in range(3200000, 3700001):
            income_tax = (500000 / 12) * 0.06 + (500000 / 12) * 0.12 + (500000 / 12) * 0.18 + (500000 / 12) * 0.24 + (
                        (converted_annual - 3200000) / 12) * 0.30
        else:
            income_tax = (500000 / 12) * 0.06 + (500000 / 12) * 0.12 + (500000 / 12) * 0.18 + (500000 / 12) * 0.24 + (
                        500000 / 12) * 0.30 + ((converted_annual - 3700000) / 12) * 0.36

        # Calculating EPF/ETF Deductions

        epf_etf_amount = (converted_basic * 20 / 100) + (converted_allowances * 3 / 100)
        epf_8_amount = (converted_basic * 8 / 100)


        # Calculating Final Net Salary

        net_salary = (converted_basic + converted_allowances - income_tax - epf_8_amount) - converted_deductions


        # Formatting final outputs and return values

        net_salary = round(net_salary,2)
        income_tax = round(income_tax,2)
        epf_etf_amount = round(epf_etf_amount,2)
        epf_8_amount = round(epf_8_amount,2)

        net_salary = str(net_salary)
        income_tax = str(income_tax)
        epf_etf_amount = str(epf_etf_amount)
        epf_8_amount = str(epf_8_amount)

        net_salary = 'LKR ' + net_salary
        income_tax = 'LKR ' + income_tax
        epf_etf_amount = 'LKR ' + epf_etf_amount
        epf_8_amount = 'LKR ' + epf_8_amount

        # Get the visitor's IP address
        ip_address = request.remote_addr

        # Check if the IP address is not in the set
        if ip_address not in unique_visitors:
            unique_visitors.add(ip_address)

        # Retrieve total visitor count
        total_visitors = len(unique_visitors)

        return render_template('output.html', 
                               net_salary=net_salary, 
                               income_tax=income_tax, 
                               epf_8_amount=epf_8_amount, 
                               epf_etf_amount=epf_etf_amount, 
                               total_visitors=total_visitors)
    
    # Get the visitor's IP address
    ip_address = request.remote_addr

    # Check if the IP address is not in the set
    if ip_address not in unique_visitors:
        unique_visitors.add(ip_address)

    # Retrieve total visitor count
    total_visitors = len(unique_visitors)

    return render_template('index.html', 
                           total_visitors=total_visitors,
                           basic_salary=session.get('basic_salary'),
                           allowances=session.get('allowances'),
                           deductions=session.get('deductions'),
                           currency=session.get('currency'))


if __name__ == '__main__':
    app.run(debug=True)
