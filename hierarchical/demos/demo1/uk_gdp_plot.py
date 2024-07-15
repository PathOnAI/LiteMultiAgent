import matplotlib.pyplot as plt

years = [2017, 2018, 2019, 2020, 2021]
gdp = [2871.23, 2871.23, 2851.41, 2697.81, 3141.51]

plt.plot(years, gdp, marker='o')
plt.title('UK GDP Over the Past 5 Years')
plt.xlabel('Year')
plt.ylabel('GDP in Billion $')
plt.grid(True)
plt.savefig('uk_gdp_plot.png')
plt.show()