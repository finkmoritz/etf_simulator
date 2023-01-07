import click
import matplotlib.pyplot as plt
import random

def simulate(annual_etf_gross_returns_average, annual_etf_gross_returns_sigma, annual_inflation_average, annual_inflation_sigma, capital_start, max_years, annual_savings_rate_start, annual_savigns_rate_increase):
    capital_per_year = []
    capital_per_year.append(capital_start)
    annual_savings_rate = annual_savings_rate_start
    
    for i in range(max_years):
        capital = capital_per_year[i]
        
        interest = random.gauss(annual_etf_gross_returns_average, annual_etf_gross_returns_sigma)
        capital *= 1.0 + interest
        
        inflation = random.gauss(annual_inflation_average, annual_inflation_sigma)
        capital /= 1.0 + inflation
        
        annual_savings_rate *= 1.0 + annual_savigns_rate_increase
        capital += annual_savings_rate
        
        capital_per_year.append(capital)
    
    return capital_per_year

@click.command()
@click.option('--annual_etf_gross_returns_average', default=0.0785, help='Relative average of the ETF\'s annual gross returns')
@click.option('--annual_etf_gross_returns_sigma', default=0.1452, help='Standard deviation of the relative average of the ETF\'s annual gross returns')
@click.option('--annual_inflation_average', default=0.0245, help='Relative average of inflation')
@click.option('--annual_inflation_sigma', default=0.011343, help='Standard deviation of the relative average of inflation')
@click.option('--number_of_simulations', default=1000, help='Number of simulations')
@click.option('--capital_start', default=40000, help='Capital at the start of each simulation')
@click.option('--max_years', default=25, help='Number of years to be simulated')
@click.option('--annual_savings_rate_start', default=12 * 1700, help='Annual savings at the start of each simulation. This amount will be added to the portfolio at the end of each year')
@click.option('--annual_savigns_rate_increase', default=0.0245, help='Relative increase of the annual savings. E.g. a value of 0.01 increases the annual savings by 1 percent each year')
def main(annual_etf_gross_returns_average, annual_etf_gross_returns_sigma, annual_inflation_average, annual_inflation_sigma, number_of_simulations, capital_start, max_years, annual_savings_rate_start, annual_savigns_rate_increase):
    capital_per_year_per_simulation = []
    for i in range(number_of_simulations):
        capital_per_year = simulate(annual_etf_gross_returns_average, annual_etf_gross_returns_sigma, annual_inflation_average, annual_inflation_sigma, capital_start, max_years, annual_savings_rate_start, annual_savigns_rate_increase)
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

if __name__ == '__main__':
    main()
    