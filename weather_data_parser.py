from weather_reading import WeatherReading


class WeatherDataParser:
    def __init__(self, file_paths):
        self.file_paths = file_paths

    def parse_weather_data(self):
        readings = []
        for file_path in self.file_paths:
            if file_path == 'weatherfiles/.DS_Store':
                continue
            with open(file_path, 'r') as file:
                lines = file.readlines()
                for line in lines[1:]:
                    line = line.strip().split(',')
                    date = line[0]
                    MaxTemperature = float(line[1]) if line[1] != '' else None
                    MinTemperature = float(line[2]) if line[2] != '' else None
                    MaxHumidity = float(line[3]) if line[3] != '' else None
                    MeanHumidity = float(line[4]) if line[4] != '' else None
                    reading = WeatherReading(
                        date,
                        MaxTemperature,
                        MinTemperature,
                        MaxHumidity,
                        MeanHumidity
                    )
                    readings.append(reading)
        return readings
