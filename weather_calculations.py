class WeatherCalculations:
    def __init__(self, readings):
        self.readings = readings

    def calculate_yearly_extremes(self, year):
        filtered_readings = []
        for reading in self.readings:
            if reading.date.year == year:
                filtered_readings.append(reading)
        if not filtered_readings:
            return None

        max_temp_reading = max(filtered_readings, key=lambda r: r.maxtemp
                               if r.maxtemp is not None else float('-inf'))
        min_temp_reading = min(filtered_readings, key=lambda r: r.mintemp
                               if r.mintemp is not None else float('inf'))
        max_humid_reading = max(filtered_readings, key=lambda r: r.maxhumid
                                if r.maxhumid is not None else float('-inf'))
        return {
            'highest_temp': max_temp_reading.maxtemp,
            'highest_temp_date': max_temp_reading.date.strftime('%B %d'),
            'lowest_temp': min_temp_reading.mintemp,
            'lowest_temp_date': min_temp_reading.date.strftime('%B %d'),
            'highest_humidity': max_humid_reading.maxhumid,
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
                             if reading.maxtemp is not None]
        filtered_mintemps = [reading.mintemp for reading in filtered_readings
                             if reading.mintemp is not None]
        filtered_humidity = [reading.meanhumidity for reading
                             in filtered_readings
                             if reading.meanhumidity is not None]
        if not all([filtered_maxtemps, filtered_mintemps, filtered_humidity]):
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
            if reading.maxtemp and reading.mintemp:
                maxtemperature = reading.maxtemp
                mintemperature = reading.mintemp
                if day not in daily_extremes:
                    daily_extremes[day] = {'highest_temp': float('-inf'),
                                           'lowest_temp': float('inf')}
                if mintemperature is not None and maxtemperature is not None:
                    if maxtemperature > daily_extremes[day]['highest_temp']:
                        daily_extremes[day]['highest_temp'] = maxtemperature
                    if mintemperature < daily_extremes[day]['lowest_temp']:
                        daily_extremes[day]['lowest_temp'] = mintemperature
        return daily_extremes
