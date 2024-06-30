import matplotlib.pyplot as plt

years = [2021, 2020, 2019, 2018, 2017]
gdp = [3141.51, 2697.81, 2851.41, 2871.71, 2755.82]

plt.plot(years, gdp, marker='o')
plt.title('UK GDP Over the Last 5 Years')
plt.xlabel('Year')
plt.ylabel('GDP in Billions USD')
plt.grid(True)
plt.show()