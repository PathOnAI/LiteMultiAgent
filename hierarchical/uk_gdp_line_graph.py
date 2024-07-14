import matplotlib.pyplot as plt

# Data for UK GDP over the past 5 years
years = [2018, 2019, 2020, 2021]
gdp = [2871.21, 2851.41, 2697.81, 3141.51]

# Create the line graph
plt.figure(figsize=(10, 6))
plt.plot(years, gdp, marker='o')
plt.title('UK GDP Over The Past 5 Years')
plt.xlabel('Year')
plt.ylabel('GDP in Billions (USD)')
plt.grid(True)
plt.savefig('uk_gdp_line_graph.png')
plt.show()