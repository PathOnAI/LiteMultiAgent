import matplotlib.pyplot as plt

# GDP data for the past 5 years
years = [2017, 2018, 2019, 2020, 2021]
gdp = [2850.95, 2870.53, 2851.41, 2697.81, 3141.51]

# Create a line plot
plt.figure(figsize=(10, 5))
plt.plot(years, gdp, marker='o', linestyle='-', color='b')

# Adding titles and labels
plt.title('UK GDP Over the Past 5 Years')
plt.xlabel('Year')
plt.ylabel('GDP (in billions of USD)')
plt.grid(True)
plt.xticks(years)
plt.tight_layout()

# Show the plot
plt.show()