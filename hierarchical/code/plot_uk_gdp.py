import matplotlib.pyplot as plt

# GDP data for the UK over the past 5 years
years = [2019, 2020, 2021, 2022, 2023]
gdp = [2851.41, 2697.81, 3141.51, 3200.00, 3300.00]  # Adjust the 2022 and 2023 estimates accordingly

plt.figure(figsize=(10, 5))
plt.plot(years, gdp, marker='o')
plt.title('UK GDP Over the Past 5 Years')
plt.xlabel('Year')
plt.ylabel('GDP in billion GBP')
plt.grid(True)
plt.savefig('uk_gdp_past_5_years.png')
plt.show()
