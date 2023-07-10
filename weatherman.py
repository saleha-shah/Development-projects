import os
import sys
from weather_calculations import WeatherCalculations
from weather_data_parser import WeatherDataParser
from weather_report import WeatherReport


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
            create_report = WeatherReport(daily_extremes)
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
            report_generator = WeatherReport(averages)
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
            report_generator = WeatherReport(extremes)
            yearly_report = report_generator.generate_yearly_report()

            # Print the yearly report
            print(yearly_report)
            print()

        else:
            print(f"Invalid flag: {flag}")


if __name__ == '__main__':
    main()
