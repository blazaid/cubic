from astral.sun import sun
from astral import Observer
from timezonefinder import TimezoneFinder
import zoneinfo
import datetime

class SolarInfo:
    def __init__(self, latitude, longitude):
        """Initializes this object.

        :param latitude: Latitude of the location.
        :param longitude: Longitude of the location.
        :raise ValueError: If the timezone for the geoposition cannot be
            determined.
        """
        self.latitude = latitude
        self.longitude = longitude

        # Obtenemos la zona horaria de esta localización...
        tf = TimezoneFinder()
        tz_name = tf.timezone_at(lat=latitude, lng=longitude)
        if tz_name is None:
            raise ValueError("Could not determine time zone.")
        self.local_tz = zoneinfo.ZoneInfo(tz_name)

        # Y el «observador» de la misma
        self.observer = Observer(latitude=self.latitude, longitude=self.longitude)
        

    def closest_event(self, aware_datetime):
        """Returns the solar event closest to the given timezone-aware datetime.
    
        :param aware_datetime: A timezone-aware datetime (any timezone).
        :return: Closest solar event as string (dawn, sunrise, noon, sunset, dusk).
        """
        if aware_datetime.tzinfo is None or aware_datetime.utcoffset() is None:
            raise ValueError("aware_datetime must be timezone-aware.")

        # Convertimos ese datetime a la zona local del lugar ...
        local_time = aware_datetime.astimezone(self.local_tz)
        local_date = local_time.date()
    
        # ... calculamos los eventos solares en esos lugar y fecha ...
        solar = sun(self.observer, date=local_date, tzinfo=self.local_tz)
    
        # ... y elegimos el evento más cercano según la hora especificada
        events = {
            'dawn': solar['dawn'],
            'sunrise': solar['sunrise'],
            'noon': solar['noon'],
            'sunset': solar['sunset'],
            'dusk': solar['dusk']
        }
    
        closest_event = min(
            events.items(),
            key=lambda x: abs((local_time - x[1]).total_seconds())
        )
    
        return closest_event[0]
