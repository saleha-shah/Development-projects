import pandas as pd
import os
from datetime import datetime
import sys


class WeatherReading:
    def __init__(self, date, MaxTemp, MinTemp, MaxHumidity, MeanHumidity):
        self.date = datetime.strptime(date, '%Y-%m-%d')
        self.maxtemp = MaxTemp
        self.mintemp = MinTemp
        self.maxhumidity = MaxHumidity
        self.meanhumidity = MeanHumidity


class WeatherDataParser:
    def __init__(self, file_paths):
        self.file_paths = file_paths

    def parse_weather_data(self):
        readings = []
        for file_path in self.file_paths:
            if file_path == 'weatherfiles/.DS_Store':
                continue
            df = pd.read_csv(file_path)
            df.rename(columns={df.columns[0]: "date"}, inplace=True)
            for index, row in df.iterrows():
                date = row["date"]
                MaxTemperature = float(row["Max TemperatureC"])
                MinTemperature = float(row["Min TemperatureC"])
                MaxHumidity = float(row["Max Humidity"])
                MeanHumidity = float(row[" Mean Humidity"])
                reading = WeatherReading(
                    date,
                    MaxTemperature,
                    MinTemperature,
                    MaxHumidity,
                    MeanHumidity
                    )
                readings.append(reading)
        return readings


def max_temp(reading):
    return reading.maxtemp


def min_temp(reading):
    return reading.mintemp


def max_humid(reading):
    return reading.maxhumidity


class WeatherCalculations:
    def __init__(self, readings):
        self.readings = readings

    def calculate_yearly_extremes(self, year):
        filtered_readings = []
        for reading in self.readings:
            if reading.date.year == year:
                filtered_readings.append(reading)
        if not filtered_readings:
            print("This runs")
            return None

        max_temp_reading = max(filtered_readings, key=max_temp)
        min_temp_reading = min(filtered_readings, key=min_temp)
        max_humid_reading = max(filtered_readings, key=max_humid)
        return {
            'highest_temp': max_temp_reading.maxtemp,
            'highest_temp_date': max_temp_reading.date.strftime('%B %d'),
            'lowest_temp': min_temp_reading.mintemp,
            'lowest_temp_date': min_temp_reading.date.strftime('%B %d'),
            'highest_humidity': max_humid_reading.maxhumidity,
            'highest_humidity_date': max_humid_reading.date.strftime('%B %d')
        }

    def calculate_monthly_means(self, year, month):
        filtered_readings = []
        for reading in self.readings:
            if reading.date.year == year and reading.date.month == month:
                filtered_readings.append(reading)
        if not filtered_readings:
            return None

        filtered_maxtemps = [reading.maxtemp for reading in filtered_readings
                             if pd.notnull(reading.maxtemp)]
        filtered_mintemps = [reading.mintemp for reading in filtered_readings
                             if pd.notnull(reading.mintemp)]
        filtered_humidity = [reading.meanhumidity for reading
                             in filtered_readings
                             if pd.notnull(reading.meanhumidity)]
        if not (filtered_maxtemps or filtered_mintemps or filtered_humidity):
            return None
        highest_avg = sum(filtered_maxtemps) / len(filtered_maxtemps)
        lowest_avg = sum(filtered_mintemps) / len(filtered_mintemps)
        humidity_avg = sum(filtered_humidity) / len(filtered_humidity)
        return {
            'highest_avg': highest_avg,
            'lowest_avg': lowest_avg,
            'humid_avg': humidity_avg
        }

    def calculate_daily_extremes(self, year, month):
        filtered_readings = []
        for reading in self.readings:
            if reading.date.year == year and reading.date.month == month:
                filtered_readings.append(reading)
        if not filtered_readings:
            return None
        daily_extremes = {}
        for reading in filtered_readings:
            day = reading.date.day
            if pd.notnull(reading.maxtemp) and pd.notnull(reading.mintemp):
                maxtemperature = reading.maxtemp
                mintemperature = reading.mintemp
                if day not in daily_extremes:
                    daily_extremes[day] = {'highest_temp': float('-inf'),
                                           'lowest_temp': float('inf')}
                if pd.notnull(mintemperature) and pd.notnull(maxtemperature):
                    if maxtemperature > daily_extremes[day]['highest_temp']:
                        daily_extremes[day]['highest_temp'] = maxtemperature
                    if mintemperature < daily_extremes[day]['lowest_temp']:
                        daily_extremes[day]['lowest_temp'] = mintemperature
        return daily_extremes


class WeatherReports:
    def __init__(self, results):
        self.results = results

    def generate_yearly_report(self):
        if self.results is None:
            return "No data available."
        report = f"Highest: {int(self.results['highest_temp'])}C "
        report += f"on {self.results['highest_temp_date']}\n"
        report += f"Lowest: {int(self.results['lowest_temp'])}C "
        report += f"on {self.results['lowest_temp_date']}\n"
        report += f"Humidity: {int(self.results['highest_humidity'])}%"
        report += f" on {self.results['highest_humidity_date']}"
        return report

    def generate_monthly_report(self):
        if self.results is None:
            return "No data available."
        report = f"Highest Average: {int(self.results['highest_avg'])}C\n"
        report += f"Lowest Average: {int(self.results['lowest_avg'])}C\n"
        report += f"Average Mean Humidity: {int(self.results['humid_avg'])}%"
        return report

    def generate_monthly_chart(self, year, month):
        if self.results is None:
            return "No data available."

        month_name = pd.Timestamp(year=year, month=month, day=1)
        month_name = month_name.strftime('%B %Y')
        chart = f"{month_name}\n"

        for day, extremes in self.results.items():
            highest_temp = extremes['highest_temp']
            lowest_temp = extremes['lowest_temp']
            if lowest_temp >= 0:
                sign = "+"
            else:
                sign = "-"

            chart += f"{str(day).zfill(2)} "
            chart += "\033[91m+\033[0m" * int(highest_temp)
            chart += f"\033[96m{sign}\033[0m" * abs(int(lowest_temp))
            chart += f" {int(highest_temp)}C - {int(lowest_temp)}C\n"
        return chart


def main():
    folder_path = sys.argv[1]
    # Get all the file paths within the folder
    file_paths = []
    for file_name in os.listdir(folder_path):
        file_paths.append(os.path.join(folder_path, file_name))
    # Parse the weather data from the files
    parser = WeatherDataParser(file_paths)
    readings = parser.parse_weather_data()

    if len(sys.argv) < 4:
        print("Please provide a valid command.")
        return
    commands = sys.argv[2:]
    for index in range(0, len(commands), 2):
        flag = commands[index]
        year_month = commands[index+1]

        if flag == '-c':
            year, month = map(int, year_month.split('/'))

            # Calculate the daily extremes
            calculator = WeatherCalculations(readings)
            daily_extremes = calculator.calculate_daily_extremes(year, month)

            # Generate the monthly chart
            create_report = WeatherReports(daily_extremes)
            monthly_chart = create_report.generate_monthly_chart(year, month)

            # Print the monthly chart
            print(monthly_chart)
            print()

        elif flag == '-a':
            year, month = map(int, year_month.split('/'))

            # Calculate the monthly averages
            calculator = WeatherCalculations(readings)
            averages = calculator.calculate_monthly_means(year, month)

            # Generate the monthly report
            report_generator = WeatherReports(averages)
            monthly_report = report_generator.generate_monthly_report()

            # Print the monthly report
            print(monthly_report)
            print()

        elif flag == '-e':
            year = int(year_month)

            # Calculate the yearly extremes
            calculator = WeatherCalculations(readings)
            extremes = calculator.calculate_yearly_extremes(year)

            # Generate the yearly report
            report_generator = WeatherReports(extremes)
            yearly_report = report_generator.generate_yearly_report()

            # Print the yearly report
            print(yearly_report)
            print()

        else:
            print(f"Invalid flag: {flag}")


if __name__ == '__main__':
    main()
