import matplotlib.pyplot as plt

# Data for UK GDP over the past 5 years (in billions GBP)
# Example data, you should replace it with actual data
years = ['2018', '2019', '2020', '2021', '2022']
gdp = [2100, 2180, 1900, 2000, 2200]

# Create a line graph
plt.figure(figsize=(10, 5))
plt.plot(years, gdp, marker='o', linestyle='-', color='b', label='UK GDP')

# Add titles and labels
plt.title('UK GDP Over the Past 5 Years')
plt.xlabel('Year')
plt.ylabel('GDP in Billions GBP')
plt.legend()

# Save the figure
plt.savefig('uk_gdp_past_5_years.png')

# Show the plot (optional, can be commented out if running script in headless mode)
# plt.show()