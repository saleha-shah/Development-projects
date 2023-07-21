class WeatherCalculations:
    def __init__(self, readings):
        self.readings = readings

    def calculate_yearly_extremes(self):

        max_temp_reading = max(self.readings, key=lambda r: r.max_temp
                               if r.max_temp is not None else float('-inf'))
        min_temp_reading = min(self.readings, key=lambda r: r.min_temp
                               if r.min_temp is not None else float('inf'))
        max_humid_reading = max(self.readings, key=lambda r: r.max_humid
                                if r.max_humid is not None else float('-inf'))

        return {
            'highest_temp': max_temp_reading.max_temp,
            'highest_temp_date': max_temp_reading.date.strftime('%B %d'),
            'lowest_temp': min_temp_reading.min_temp,
            'lowest_temp_date': min_temp_reading.date.strftime('%B %d'),
            'highest_humidity': max_humid_reading.max_humid,
            'highest_humidity_date': max_humid_reading.date.strftime('%B %d')
        }

    def calculate_monthly_means(self):
        maxtemps = [reading.max_temp for reading in self.readings
                    if reading.max_temp is not None]
        mintemps = [reading.min_temp for reading in self.readings
                    if reading.min_temp is not None]
        humidity = [reading.mean_humidity for reading
                    in self.readings if reading.mean_humidity is not None]

        highest_avg = sum(maxtemps) / len(maxtemps)
        lowest_avg = sum(mintemps) / len(mintemps)
        humidity_avg = sum(humidity) / len(humidity)

        return {
            'highest_avg': highest_avg,
            'lowest_avg': lowest_avg,
            'humid_avg': humidity_avg
        }

    def calculate_daily_extremes(self):
        daily_extremes = {}
        for reading in self.readings:
            day = reading.date.day

            if reading.max_temp is not None and reading.min_temp is not None:
                daily_extremes[day] = {'highest_temp': reading.max_temp,
                                       'lowest_temp': reading.min_temp}

        return daily_extremes
