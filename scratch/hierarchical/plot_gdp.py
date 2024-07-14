import matplotlib.pyplot as plt

years = ['2017', '2018', '2019', '2020', '2021']
gdp_values = [2.855, 2.861, 2.851, 2.697, 3.141]

plt.figure(figsize=(10, 5))
plt.plot(years, gdp_values, marker='o')
plt.title('UK GDP Over the Past 5 Years')
plt.xlabel('Year')
plt.ylabel('GDP in Trillion USD')
plt.grid(True)
plt.savefig('UK_GDP_Last_5_Years.png')
plt.show()