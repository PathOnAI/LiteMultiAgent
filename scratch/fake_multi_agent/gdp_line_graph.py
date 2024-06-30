import matplotlib.pyplot as plt

# Data
years = [2017, 2018, 2019, 2020, 2021]
gdp_values = [2644.81, 2871.71, 2851.41, 2697.81, 3141.51]

# Plotting the data
plt.figure(figsize=(10,5))
plt.plot(years, gdp_values, marker='o')
plt.title('UK GDP Over the Past 5 Years')
plt.xlabel('Year')
plt.ylabel('GDP (in Billion $)')
plt.grid(True)

# Save the plot
plt.savefig('uk_gdp_past_5_years.png')
plt.show()