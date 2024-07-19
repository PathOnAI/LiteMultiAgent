import matplotlib.pyplot as plt
import pandas as pd

# Define the data
data = {
    'Year': [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021],
    'GDP in Billion $': [2695.58, 2818.79, 3048.98, 2928.74, 2671.46, 2699.87, 2855.27, 2836.51, 2706.7, 3181.98]
}

df = pd.DataFrame(data)

# Create the plot
plt.figure(figsize=(10, 5))
plt.plot(df['Year'], df['GDP in Billion $'], marker='o')
plt.title('GDP Over Time in the UK')
plt.xlabel('Year')
plt.ylabel('GDP in Billion $')
plt.grid(True)

# Show the plot
plt.show()