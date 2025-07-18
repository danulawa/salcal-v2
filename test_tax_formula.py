converted_annual = 600000*12  # Example annual salary in LKR    


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
    

income_tax = int(income_tax)  # Convert to integer for display
print(f"Income Tax: {income_tax} LKR")  # Display the calculated income tax




if converted_annual in range(0, 1800001):
    income_tax2 = 0
elif converted_annual in range(1800000, 2800001):
    income_tax2 = ((converted_annual - 1800000) / 12) * 0.06
elif converted_annual in range(2800000, 3300001):
    income_tax2 = (1000000 / 12) * 0.06 + ((converted_annual - 2800000) / 12) * 0.18
elif converted_annual in range(3300000, 3800001):
    income_tax2 = (1000000 / 12) * 0.06 + (500000 / 12) * 0.18 + ((converted_annual - 3300000) / 12) * 0.24
elif converted_annual in range(3800000, 4300001):
    income_tax2 = (1000000 / 12) * 0.06 + (500000 / 12) * 0.28 + (500000 / 12) * 0.24 + (
                (converted_annual - 3800000) / 12) * 0.30
else:
    income_tax2 = (1000000 / 12) * 0.06 + (500000 / 12) * 0.18 + (500000 / 12) * 0.24 + (500000 / 12) * 0.30 + (
                (converted_annual - 4300000) / 12) * 0.36
    

income_tax2 = int(income_tax2)  # Convert to integer for display
print(f"New Income Tax: {income_tax2} LKR")  # Display the calculated income tax


saved_income_tax = income_tax - income_tax2
print(f"Saved Income Tax: {saved_income_tax} LKR")  # Display the saved income tax


















