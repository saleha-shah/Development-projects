from datetime import datetime


class WeatherReport:
    def __init__(self, results):
        self.results = results

    def generate_yearly_report(self):
        if self.results is None:
            return 'No data available.'
        report = (f"Yearly Report\n"
                  f"Highest: {int(self.results['highest_temp'])}C"
                  f" on {self.results['highest_temp_date']}\n"
                  f"Lowest: {int(self.results['lowest_temp'])}C"
                  f" on {self.results['lowest_temp_date']}\n"
                  f"Humidity: {int(self.results['highest_humidity'])}% "
                  f"on {self.results['highest_humidity_date']}")
        return report

    def generate_monthly_report(self, year, month):
        if self.results is None:
            return 'No data available.'

        report = (f"Monthly Report\n"
                  f"Highest Average: {int(self.results['highest_avg'])}C\n"
                  f"Lowest Average: {int(self.results['lowest_avg'])}C\n"
                  f"Average Mean Humidity:"
                  f"{abs(int(self.results['humid_avg']))}%")
        return report

    def generate_monthly_chart(self, year, month):
        if len(self.results) == 0:
            return 'No data available.'

        month_name = datetime(year=year, month=month, day=1).strftime('%B %Y')
        chart = f"{month_name}\n"

        for day, extremes in self.results.items():
            highest_temp = extremes['highest_temp']
            lowest_temp = extremes['lowest_temp']
            if lowest_temp >= 0:
                sign = '+'
            else:
                sign = '-'

            chart += f'{str(day).zfill(2)} '
            chart += '\033[91m+\033[0m' * int(highest_temp)
            chart += f'\033[94m{sign}\033[0m' * abs(int(lowest_temp))
            chart += f' {int(highest_temp)}C - {int(lowest_temp)}C\n'
        return chart
