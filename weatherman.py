import argparse
import calendar
import os

from weather_calculations import WeatherCalculations
from weather_data_parser import WeatherDataParser
from weather_report import WeatherReport


def main():
    parser = argparse.ArgumentParser(description='Weatherman')
    parser.add_argument('folder_path', type=str)
    parser.add_argument('-c', '--chart', type=str, help='Generate monthly chart')
    parser.add_argument('-a', '--average', type=str, help='Generate monthly average report')
    parser.add_argument('-e', '--extremes', type=int, help='Generate yearly extremes report')
    args = parser.parse_args()

    folder_path = args.folder_path

    if args.chart:
        file_paths = []
        year, month = map(int, args.chart.split('/'))
        file_name = f'Murree_weather_{year}_{calendar.month_abbr[month]}.txt'
        file_path = os.path.join(folder_path, file_name)
        if os.path.exists(file_path):
            file_paths.append(file_path)
        print(file_paths)

        # Parse the weather data from the files
        parser = WeatherDataParser(file_paths)
        readings = parser.parse_weather_data()

        # Calculate the daily extremes
        weather_calculation = WeatherCalculations(readings)
        daily_extremes = weather_calculation.calculate_daily_extremes()

        # Generate the monthly chart
        report = WeatherReport(daily_extremes)
        monthly_chart = report.generate_monthly_chart(year, month)

        # Print the monthly chart
        print(monthly_chart, end='\n\n')

    if args.average:
        file_paths = []
        year, month = map(int, args.average.split('/'))
        file_name = f'Murree_weather_{year}_{calendar.month_abbr[month]}.txt'
        file_path = os.path.join(folder_path, file_name)
        if os.path.exists(file_path):
            file_paths.append(file_path)

        # Parse the weather data from the files
        parser = WeatherDataParser(file_paths)
        readings = parser.parse_weather_data()

        # Calculate the monthly averages
        weather_calculation = WeatherCalculations(readings)
        averages = weather_calculation.calculate_monthly_means()
        # Generate the monthly report
        report = WeatherReport(averages)
        monthly_report = report.generate_monthly_report(year, month)

        # Print the monthly report
        print(monthly_report, end='\n\n')

    if args.extremes:
        file_paths = []
        year = args.extremes
        file_names = [f'Murree_weather_{year}_{month}.txt'
                      for month in calendar.month_abbr[1:]]
        for file in file_names:
            path = os.path.join(folder_path, file)
            if os.path.exists(path):
                file_paths.append(path)

        # Parse the weather data from the files
        parser = WeatherDataParser(file_paths)
        readings = parser.parse_weather_data()

        # Calculate the yearly extremes
        weather_calculation = WeatherCalculations(readings)
        extremes = weather_calculation.calculate_yearly_extremes()

        # Generate the yearly report
        report = WeatherReport(extremes)
        yearly_report = report.generate_yearly_report()

        # Print the yearly report
        print(yearly_report, end='\n\n')


if __name__ == '__main__':
    main()
