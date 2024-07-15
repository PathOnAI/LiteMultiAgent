import matplotlib.pyplot as plt

# Data
years = [2017, 2018, 2019, 2020, 2021]
gdp = [2871.61, 2851.41, 2697.81, 3141.51]  # in billions USD

# Create a line plot
plt.figure(figsize=(10, 5))
plt.plot(years, gdp, marker='o', linestyle='-', color='b')

# Add title and labels
plt.title("UK GDP Over the Past 5 Years")
plt.xlabel("Year")
plt.ylabel("GDP in Billion USD")

# Add grid
plt.grid(True)

# Save the plot as an image file
plt.savefig("UK_GDP_5_Years.png")

# Show the plot
plt.show()
