import matplotlib.pyplot as plt

# UK GDP data for the past 5 years (in billion USD)
gdp_years = [2021, 2020, 2019, 2018, 2017]
gdp_values = [3141.51, 2697.81, 2851.41, 2871.51, 2686.83]

def plot_gdp(years, values):
    plt.figure(figsize=(10, 5))
    plt.plot(years, values, marker='o')
    plt.title('UK GDP Over the Past 5 Years')
    plt.xlabel('Year')
    plt.ylabel('GDP in Billion USD')
    plt.grid(True)
    plt.savefig('uk_gdp.png')
    plt.show()

if __name__ == '__main__':
    plot_gdp(gdp_years, gdp_values)
