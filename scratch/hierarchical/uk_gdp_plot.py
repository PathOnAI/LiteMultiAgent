import matplotlib.pyplot as plt

# Data
years = [2019, 2020, 2021, 2022, 2023]
gdp = [2851.41, 2697.81, 3141.51, 3088.84, 3340.03]

# Plotting the data
plt.figure(figsize=(10, 5))
plt.plot(years, gdp, marker='o')
plt.title('UK GDP Over the Past 5 Years')
plt.xlabel('Year')
plt.ylabel('GDP (Billion USD)')
plt.grid(True)
plt.savefig('uk_gdp_plot.png')
plt.show()