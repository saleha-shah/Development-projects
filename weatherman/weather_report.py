from datetime import datetime

RED = '\033[91m'
BLUE = '\033[94m'
DEFAULT = '\033[0m'


class WeatherReport:

    def __init__(self, results):
        self.results = results

    def generate_yearly_extremes(self):
        if not self.results:
            return 'No data available.'

        report = (f'Yearly Report\n'
                  f'Highest: {int(self.results["highest_temp"])}C'
                  f' on {self.results["highest_temp_date"]}\n'
                  f'Lowest: {int(self.results["lowest_temp"])}C'
                  f' on {self.results["lowest_temp_date"]}\n'
                  f'Humidity: {int(self.results["highest_humidity"])}% '
                  f'on {self.results["highest_humidity_date"]}')

        return report

    def generate_monthly_averages(self, year, month):
        if not self.results:
            return 'No data available.'

        report = (f'Monthly Report\n'
                  f'Highest Average: {int(self.results["highest_avg"])}C\n'
                  f'Lowest Average: {int(self.results["lowest_avg"])}C\n'
                  f'Average Mean Humidity:'
                  f'{abs(int(self.results["humid_avg"]))}%')

        return report

    def generate_monthly_chart(self, year, month):
        if not self.results:
            return 'No data available.'

        month_name = datetime(year=year, month=month, day=1).strftime('%B %Y')
        chart = f'{month_name}\n'

        for day, extremes in self.results.items():
            highest_temp = extremes['highest_temp']
            lowest_temp = extremes['lowest_temp']
            if lowest_temp >= 0:
                sign = '+'
            else:
                sign = '-'

            chart += (f'{str(day).zfill(2)} '
                      f'{RED + "+" * int(highest_temp)}'
                      f'{BLUE + sign * abs(int(lowest_temp))}{DEFAULT}'
                      f' {int(highest_temp)}C - {int(lowest_temp)}C\n')
        return chart
