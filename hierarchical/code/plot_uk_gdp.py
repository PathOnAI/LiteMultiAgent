import matplotlib.pyplot as plt

# Sample data for UK's GDP over the past 5 years (in billion USD)
years = [2018, 2019, 2020, 2021, 2022]
gdp = [2867, 2829, 2707, 3033, 3143]

# Plotting the line graph
plt.figure(figsize=(10, 5))
plt.plot(years, gdp, marker='o', linestyle='-', color='b')
plt.title("UK's GDP Over the Past 5 Years")
plt.xlabel('Year')
plt.ylabel('GDP in Billion USD')
plt.grid(True)
plt.savefig('uk_gdp_past_5_years.png')
plt.show()
