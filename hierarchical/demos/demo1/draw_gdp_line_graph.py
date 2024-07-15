import matplotlib.pyplot as plt

# Data for the past 5 years
years = [2017, 2018, 2019, 2020, 2021]
gdp = [2851.40, 2871.30, 2851.41, 2697.81, 3141.51]

# Create a line graph
plt.figure(figsize=(10,5))
plt.plot(years, gdp, marker='o')
plt.title('UK GDP Over the Past 5 Years')
plt.xlabel('Year')
plt.ylabel('GDP in Billions (USD)')
plt.grid(True)
plt.savefig('UK_GDP_Line_Graph.png')
plt.show()