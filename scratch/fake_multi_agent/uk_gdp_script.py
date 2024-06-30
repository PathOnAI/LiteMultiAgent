import matplotlib.pyplot as plt

# Data for UK's GDP over the past 5 years
years = [2017, 2018, 2019, 2020, 2021]
gdp = [2855.74, 2871.51, 2851.41, 2697.81, 3141.51]

# Create the line graph
plt.figure(figsize=(10, 5))
plt.plot(years, gdp, marker='o', linestyle='-', color='b')
plt.title("UK's GDP Over the Past 5 Years")
plt.xlabel("Year")
plt.ylabel("GDP in Billion USD")
plt.grid(True)

# Save the plot as an image
plt.savefig("./uk_gdp.png")
plt.close()