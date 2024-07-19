import matplotlib.pyplot as plt

# UK GDP data for the past 5 years (in billion pounds)
years = [2018, 2019, 2020, 2021, 2022]
gdp = [2221.0, 2273.1, 2009.1, 2170.1, 2331.2]

# Create the line plot
plt.figure(figsize=(10, 6))
plt.plot(years, gdp, marker='o', linestyle='-', color='b')

# Adding the title and labels
plt.title('UK GDP Over the Past 5 Years')
plt.xlabel('Year')
plt.ylabel('GDP (in billion pounds)')

# Save the plot as an image file
plt.savefig('uk_gdp_line_graph.png')

# Show the plot
plt.show()
