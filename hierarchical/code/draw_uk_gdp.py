import matplotlib.pyplot as plt

# Data for the UK's GDP over the past 5 years (in trillions USD)
years = ['2018', '2019', '2020', '2021', '2022']
gdp = [2.86, 2.86, 2.70, 3.11, 3.19]  # Example data

# Create a line graph
plt.figure(figsize=(10, 5))
plt.plot(years, gdp, marker='o', linestyle='-', color='b')

# Add title and labels
plt.title('UK GDP Over the Past 5 Years')
plt.xlabel('Year')
plt.ylabel('GDP in Trillions of USD')

# Save the graph to an image file
plt.savefig('uk_gdp_line_graph.png')

# Show the graph
plt.show()
