import matplotlib.pyplot as plt

years = [2017, 2018, 2019, 2020, 2021]
gdp = [2784.59, 2871.25, 2851.41, 2697.81, 3141.51]

plt.figure(figsize=(10, 5))
plt.plot(years, gdp, marker='o')
plt.title('GDP of the United Kingdom (2017-2021)')
plt.xlabel('Year')
plt.ylabel('GDP in Billion USD')
plt.grid(True)
plt.savefig('uk_gdp_2017_2021.png')
plt.show()