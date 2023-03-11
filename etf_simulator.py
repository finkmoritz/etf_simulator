import click
import matplotlib.pyplot as plt
import numpy as np
import random

def simulate(annual_etf_gross_returns_average, annual_etf_gross_returns_sigma, annual_etf_ter, annual_inflation_average, annual_inflation_sigma, capital_start, max_years, annual_savings_rate_start, annual_savings_rate_increase):
    capital_per_year = []
    capital_absolute = capital_start
    annual_savings_rate = annual_savings_rate_start
    inflation_total = 1.0
    
    capital_per_year.append(capital_absolute)
    
    for i in range(max_years):
        interest = random.gauss(annual_etf_gross_returns_average, annual_etf_gross_returns_sigma)
        capital_absolute *= 1.0 + interest - annual_etf_ter
        
        annual_savings_rate *= 1.0 + annual_savings_rate_increase
        capital_absolute += annual_savings_rate
        
        inflation_total *= (1.0 - random.gauss(annual_inflation_average, annual_inflation_sigma))
        
        capital_per_year.append(capital_absolute * inflation_total)
    
    return capital_per_year

@click.command()
@click.option('--annual_etf_gross_returns_average', default=0.0785, help='Relative average of the ETF\'s annual gross returns')
@click.option('--annual_etf_gross_returns_sigma', default=0.1452, help='Standard deviation of the relative average of the ETF\'s annual gross returns')
@click.option('--annual_etf_ter', default=0.002, help='TER (Total expense ratio) of the ETF')
@click.option('--annual_inflation_average', default=0.0245, help='Relative average of inflation')
@click.option('--annual_inflation_sigma', default=0.011343, help='Standard deviation of the relative average of inflation')
@click.option('--number_of_simulations', default=100, help='Number of simulations')
@click.option('--capital_start', default=40000, help='Capital at the start of each simulation')
@click.option('--max_years', default=25, help='Number of years to be simulated')
@click.option('--annual_savings_rate_start', default=12 * 1700, help='Annual savings at the start of each simulation. This amount will be added to the portfolio at the end of each year')
@click.option('--annual_savings_rate_increase', default=0.0245, help='Relative increase of the annual savings. E.g. a value of 0.01 increases the annual savings by 1 percent each year')
def main(annual_etf_gross_returns_average, annual_etf_gross_returns_sigma, annual_etf_ter, annual_inflation_average, annual_inflation_sigma, number_of_simulations, capital_start, max_years, annual_savings_rate_start, annual_savings_rate_increase):
    capital_per_year_per_simulation = []
    for i in range(number_of_simulations):
        capital_per_year = simulate(annual_etf_gross_returns_average, annual_etf_gross_returns_sigma, annual_etf_ter, annual_inflation_average, annual_inflation_sigma, capital_start, max_years, annual_savings_rate_start, annual_savings_rate_increase)
        capital_per_year_per_simulation.append(capital_per_year)
        
    capital_per_year_per_simulation.sort(key=lambda x:x[max_years])
    
    fig, plots = plt.subplots(2, constrained_layout=True)
    
    for i in range(number_of_simulations):
        plots[0].plot(range(max_years + 1), capital_per_year_per_simulation[i], color = "lightgrey", linestyle = ":")
    
    plots[0].plot(range(max_years + 1), capital_per_year_per_simulation[number_of_simulations - 1], color = "green", linestyle = "--", label = "Best case (" + "{:,}".format(int(capital_per_year_per_simulation[number_of_simulations - 1][max_years])) + ")")
    plots[0].plot(range(max_years + 1), capital_per_year_per_simulation[int(number_of_simulations / 2)], color = "orange", linestyle = "-", label = "Median case (" + "{:,}".format(int(capital_per_year_per_simulation[int(number_of_simulations / 2)][max_years])) + ")")
    plots[0].plot(range(max_years + 1), capital_per_year_per_simulation[0], color = "red", linestyle = "--", label = "Worst case (" + "{:,}".format(int(capital_per_year_per_simulation[0][max_years])) + ")")
    
    invested_capital_per_year = [(capital_start + i * annual_savings_rate_start * pow(1.0 + annual_savings_rate_increase, i)) * pow(1.0 - annual_inflation_average, i) for i in range(max_years + 1)]
    plots[0].plot(range(max_years + 1), invested_capital_per_year, color = "blue", linestyle = "-.", label = "Invested (" + "{:,}".format(int(invested_capital_per_year[max_years])) + ")")
    
    plots[0].set_title("Portfolio development")
    plots[0].set(xlabel = "Years", ylabel="Capital (after inflation)")
    plots[0].legend()
    
    counts, bins = np.histogram([capital_per_year_per_simulation[i][max_years] for i in range(number_of_simulations)], bins=int(0.1 * number_of_simulations))
    plots[1].stairs(counts, bins)
    plots[1].set_title("Final capital")
    plots[1].set(xlabel = "Capital (after inflation)", ylabel="Number of simulations")
    
    plt.show()

if __name__ == '__main__':
    main()
    