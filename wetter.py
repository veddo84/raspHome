import pyowm
import datetime
from datetime import timedelta
from datetime import date
today = date.today()
owm = pyowm.OWM('18623fdb375d1a3bde283a98f69bbd59')
class Weather():

    def getTemp(self,city):
        observation = owm.weather_at_place(city)
        w = observation.get_weather()
        temp=w.get_temperature('celsius')

        return temp

    def forecast(self, city):
        forecast = owm.daily_forecast(city)
        tomorrow = pyowm.timeutils.tomorrow()
        print forecast.will_have_sun()

w= Weather()

