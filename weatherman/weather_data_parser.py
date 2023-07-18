import csv

from weather_reading import WeatherReading


class WeatherDataParser:
    def __init__(self, file_paths):
        self.file_paths = file_paths

    @staticmethod
    def clean_value(value):
        return float(value) if value != '' else None

    def parse_weather_data(self):
        readings = []
        for file_path in self.file_paths:
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)

                column_names = reader.fieldnames
                column_names[0] = 'date'

                for row in reader:
                    date = row['date']

                    max_temp = self.clean_value(row['Max TemperatureC'])
                    min_temp = self.clean_value(row['Min TemperatureC'])
                    max_humidity = self.clean_value(row['Max Humidity'])
                    mean_humidity = self.clean_value(row[' Mean Humidity'])

                    reading = WeatherReading(
                        date,
                        max_temp,
                        min_temp,
                        max_humidity,
                        mean_humidity
                    )
                    readings.append(reading)
        return readings
