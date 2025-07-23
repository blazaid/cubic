from astral.sun import sun
from astral import Observer
from timezonefinder import TimezoneFinder
import zoneinfo
import datetime

def solar_info(latitude, longitude, aware_datetime):
    """Returns the solar event closest to the given timezone-aware datetime.

    :param latitude: Latitude of the location.
    :param longitude: Longitude of the location.
    :param aware_datetime: A timezone-aware datetime (any timezone).
    :return: Closest solar event as string (dawn, sunrise, noon, sunset, dusk).
    """
    if aware_datetime.tzinfo is None or aware_datetime.utcoffset() is None:
        raise ValueError("aware_datetime must be timezone-aware.")

    # Obtenemos la zona horaria de la localización ...
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lat=latitude, lng=longitude)
    if tz_name is None:
        raise ValueError("Could not determine time zone.")
    
    local_tz = zoneinfo.ZoneInfo(tz_name)
    
    # ... convertimos ese datetime a la zona local del lugar ...
    local_time = aware_datetime.astimezone(local_tz)
    local_date = local_time.date()

    # ... calculamos los eventos solares en esos lugar y fecha ...
    observer = Observer(latitude=latitude, longitude=longitude)
    solar = sun(observer, date=local_date, tzinfo=local_tz)

    # ... y eleginos el evento más cercano según la hora especificada
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
