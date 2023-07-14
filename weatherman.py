import argparse
import calendar
import os

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


def parse_weather_data(file_paths):
    parser = WeatherDataParser(file_paths)
    readings = parser.parse_weather_data()
    weather_data = WeatherCalculations(readings)
    return weather_data


def generate_report(report_type, data, year, month=None):
    report = WeatherReport(data)

    func_name = f'generate_{report_type}'
    func = getattr(report, func_name, None)
    if func is not None:
        return func(year, month)


def main():
    parser = argparse.ArgumentParser(description='Weatherman')
    parser.add_argument('folder_path', type=str)
    parser.add_argument('-c', '--chart', type=str, help='Generate monthly chart')
    parser.add_argument('-a', '--average', type=str, help='Generate monthly average report')
    parser.add_argument('-e', '--extremes', type=int, help='Generate yearly extremes report')
    args = parser.parse_args()

    folder_path = args.folder_path

    if args.chart:
        year, month = map(int, args.chart.split('/'))
        file_paths = get_file_paths(folder_path, year, month)

        # Parse the weather data from the files
        weather_data = parse_weather_data(file_paths)
        daily_extremes = weather_data.calculate_daily_extremes()

        # Generate the monthly chart
        report = generate_report('chart', daily_extremes, year, month)

        # Print the monthly chart
        print(report, end='\n\n')

    if args.average:
        year, month = map(int, args.average.split('/'))
        file_paths = get_file_paths(folder_path, year, month)

        # Parse the weather data from the files
        weather_data = parse_weather_data(file_paths)
        averages = weather_data.calculate_monthly_means()

        # Generate the monthly report
        report = generate_report('averages', averages, year, month)

        # Print the monthly report
        print(report, end='\n\n')

    if args.extremes:
        year = args.extremes
        file_paths = get_file_paths(folder_path, year)

        # Parse the weather data from the files
        weather_data = parse_weather_data(file_paths)
        extremes = weather_data.calculate_yearly_extremes()

        # Generate the yearly report
        report = generate_report('extremes', extremes, year)

        # Print the yearly report
        print(report, end='\n\n')


if __name__ == '__main__':
    main()
