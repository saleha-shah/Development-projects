import argparse
import calendar
import os
from datetime import datetime

from weather_calculations import WeatherCalculations
from weather_data_parser import WeatherDataParser
from weather_report import WeatherReport


def get_file_paths(folder_path, year, month=None):
    file_paths = []

    if not month:
        file_names = [f'Murree_weather_{year}_{mon}.txt'
                      for mon in calendar.month_abbr[1:]]
    else:
        file_names = [f'Murree_weather_{year}_{calendar.month_abbr[month]}.txt']

    for file in file_names:
        path = os.path.join(folder_path, file)
        if os.path.exists(path):
            file_paths.append(path)

    return file_paths


def parse_data(file_paths):
    parser = WeatherDataParser(file_paths)
    readings = parser.parse_weather_data()
    weather_data = WeatherCalculations(readings)

    return weather_data


def parse_date_argument(date_str):
    try:
        date = datetime.strptime(date_str, '%Y/%m')
        return date.year, date.month
    except ValueError:
        raise argparse.ArgumentTypeError('Invalid date format. Please use YYYY/MM.')


def main():
    parser = argparse.ArgumentParser(description='Weatherman')
    parser.add_argument('folder_path', type=str)
    parser.add_argument('-c', '--chart', type=parse_date_argument, help='Generate monthly chart')
    parser.add_argument('-a', '--average', type=parse_date_argument, help='Generate monthly report')
    parser.add_argument('-e', '--extremes', type=int, help='Generate yearly extremes report')
    args = parser.parse_args()

    folder_path = args.folder_path

    if args.chart:
        year, month = args.chart
        file_paths = get_file_paths(folder_path, year, month)

        weather_data = parse_data(file_paths)
        daily_extremes = weather_data.calculate_daily_extremes()

        report = WeatherReport(daily_extremes)
        monthly_chart = report.generate_monthly_chart(year, month)
        print(monthly_chart, end='\n\n')

    if args.average:
        year, month = args.average
        file_paths = get_file_paths(folder_path, year, month)

        weather_data = parse_data(file_paths)
        averages = weather_data.calculate_monthly_means()

        report = WeatherReport(averages)
        monthly_report = report.generate_monthly_averages(year, month)

        print(monthly_report, end='\n\n')

    if args.extremes:
        year = args.extremes
        file_paths = get_file_paths(folder_path, year)

        weather_data = parse_data(file_paths)
        extremes = weather_data.calculate_yearly_extremes()

        report = WeatherReport(extremes)
        yearly_report = report.generate_yearly_extremes()

        print(yearly_report, end='\n\n')


if __name__ == '__main__':
    main()
