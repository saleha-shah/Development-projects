from datetime import datetime


class WeatherReading:
    def __init__(self, date, MaxTemp, MinTemp, MaxHumidity, MeanHumidity):
        self.date = datetime.strptime(date, '%Y-%m-%d')
        self.maxtemp = MaxTemp
        self.mintemp = MinTemp
        self.maxhumid = MaxHumidity
        self.meanhumidity = MeanHumidity


