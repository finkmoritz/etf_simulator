import matplotlib.pyplot as plt
import random

def simulate(annual_msci_gross_returns_average, annual_msci_gross_returns_sigma, annual_inflation_average, annual_inflation_sigma, capital_start, max_years, annual_savings_rate_start, annual_savigns_rate_increase):
    capital_per_year = []
    capital_per_year.append(capital_start)
    annual_savings_rate = annual_savings_rate_start
    
    for i in range(max_years):
        capital = capital_per_year[i]
        
        interest = random.gauss(annual_msci_gross_returns_average, annual_msci_gross_returns_sigma)
        capital *= 1.0 + interest
        
        inflation = random.gauss(annual_inflation_average, annual_inflation_sigma)
        capital /= 1.0 + inflation
        
        annual_savings_rate *= 1.0 + annual_savigns_rate_increase
        capital += annual_savings_rate
        
        capital_per_year.append(capital)
    
    return capital_per_year

if __name__ == '__main__':
    
    annual_msci_gross_returns_average = 0.0785
    annual_msci_gross_returns_sigma = 0.1452
    
    annual_inflation_average = 0.0245
    annual_inflation_sigma = 0.011343
    
    number_of_simulations = 1000
    capital_start = 40000
    max_years = 25
    annual_savings_rate_start = 12 * 1700
    annual_savigns_rate_increase = 0.0245
    
    capital_per_year_per_simulation = []
    for i in range(number_of_simulations):
        capital_per_year = simulate(annual_msci_gross_returns_average, annual_msci_gross_returns_sigma, annual_inflation_average, annual_inflation_sigma, capital_start, max_years, annual_savings_rate_start, annual_savigns_rate_increase)
        capital_per_year_per_simulation.append(capital_per_year)
        
    capital_per_year_per_simulation.sort(key=lambda x:x[max_years])
    
    for i in range(number_of_simulations):
        plt.plot(range(max_years + 1), capital_per_year_per_simulation[i], color = "lightgrey", linestyle = ":")
    
    plt.plot(range(max_years + 1), capital_per_year_per_simulation[number_of_simulations - 1], color = "green", linestyle = "--", label = "Best case (" + "{:,}".format(int(capital_per_year_per_simulation[number_of_simulations - 1][max_years])) + ")")
    plt.plot(range(max_years + 1), capital_per_year_per_simulation[int(number_of_simulations / 2)], color = "orange", linestyle = "-", label = "Median case (" + "{:,}".format(int(capital_per_year_per_simulation[int(number_of_simulations / 2)][max_years])) + ")")
    plt.plot(range(max_years + 1), capital_per_year_per_simulation[0], color = "red", linestyle = "--", label = "Worst case (" + "{:,}".format(int(capital_per_year_per_simulation[0][max_years])) + ")")
    
    invested_capital_per_year = [(capital_start + i * annual_savings_rate_start * pow(1.0 + annual_savigns_rate_increase, i)) * pow(1.0 - annual_inflation_average, i) for i in range(max_years + 1)]
    plt.plot(range(max_years + 1), invested_capital_per_year, color = "blue", linestyle = "-.", label = "Invested (" + "{:,}".format(int(invested_capital_per_year[max_years])) + ")")
    
    plt.title("ETF")
    plt.xlabel("Years")
    plt.ylabel("Capital (after inflation)")
    plt.legend()
    
    plt.show()
    