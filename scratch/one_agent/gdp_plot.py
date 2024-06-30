import matplotlib.pyplot as plt

years = [2017, 2018, 2019, 2020, 2021]
gdp = [2870.12, 2851.41, 2697.81, 3141.51]

plt.figure(figsize=(10, 5))
plt.plot(years, gdp, marker='o')
plt.title('UK GDP Over the Past 5 Years')
plt.xlabel('Year')
plt.ylabel('GDP in Billion USD')
plt.grid(True)
plt.savefig('UK_GDP.png')
plt.show()