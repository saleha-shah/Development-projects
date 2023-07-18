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
                weather_entries = file.readlines()
                for entry in weather_entries[1:]:
                    entry = entry.strip().split(',')
                    date = entry[0]

                    max_temp = self.clean_value(entry[1])
                    min_temp = self.clean_value(entry[3])
                    max_humidity = self.clean_value(entry[7])
                    mean_humidity = self.clean_value(entry[8])

                    reading = WeatherReading(
                        date,
                        max_temp,
                        min_temp,
                        max_humidity,
                        mean_humidity
                    )
                    readings.append(reading)
        return readings
