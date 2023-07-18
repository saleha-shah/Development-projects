from datetime import datetime


class WeatherReading:
    def __init__(self, date, max_temp, min_temp, max_humidity, mean_humidity):
        self.date = datetime.strptime(date, '%Y-%m-%d')
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.max_humid = max_humidity
        self.mean_humidity = mean_humidity


