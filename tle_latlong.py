from sgp4.api import Satrec, jday
from math import degrees, radians, atan2, sqrt, sin, cos

def read_tle_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        tle_data = [line.strip() for line in lines if line.strip()]
    return tle_data

def parse_jday_from_tle(line1):
    epoch_year = int(line1[18:20])
    epoch_day = float(line1[20:32])
    
    if epoch_year < 57:
        year = 2000 + epoch_year
    else:
        year = 1900 + epoch_year
    
    jd, fr = jday(year, 1, 1, 0, 0, 0)
    jd += epoch_day - 1
    print(f"Epoch Year: {year}, Epoch Day: {epoch_day}, Julian Date: {jd}")
    return jd

def eci_to_lat_lon(position, jd):
    x, y, z = position
    
    # Constants
    a = 6378.137  # Earth's semi-major axis in km
    f = 1 / 298.257223563  # Earth's flattening factor
    e2 = f * (2 - f)  # Square of eccentricity
    omega = 7.2921150e-5  # Earth's rotation rate in rad/s
    
    # Calculate Greenwich Sidereal Time (GST)
    T = (jd - 2451545.0) / 36525.0
    GST = 280.46061837 + 360.98564736629 * (jd - 2451545.0) \
          + 0.000387933 * T**2 - (T**3) / 38710000.0
    GST = GST % 360.0
    GST = radians(GST)
    print(f"GST (radians): {GST}")
    
    # Rotate ECI coordinates to Earth-fixed coordinates
    theta = GST + omega * (jd - int(jd)) * 86400.0
    x_earth = x * cos(theta) + y * sin(theta)
    y_earth = -x * sin(theta) + y * cos(theta)
    z_earth = z
    print(f"Earth-fixed coordinates: x={x_earth}, y={y_earth}, z={z_earth}")
    
    # Calculate longitude
    lon = atan2(y_earth, x_earth)
    
    # Calculate latitude using iterative method
    r = sqrt(x_earth**2 + y_earth**2)
    E2 = a**2 - (a * (1 - f))**2
    lat = atan2(z_earth, r)
    for _ in range(5):
        C = a / sqrt(1 - e2 * sin(lat)**2)
        lat = atan2(z_earth + e2 * C * sin(lat), r)
    
    # Convert from radians to degrees
    lat = degrees(lat)
    lon = degrees(lon)
    
    # Normalize longitude to the range [-180, 180]
    if lon > 180:
        lon -= 360
    elif lon < -180:
        lon += 360
    
    print(f"Latitude: {lat}, Longitude: {lon}")
    return lat, lon

def tle_to_lat_lon(line1, line2, jd):
    satellite = Satrec.twoline2rv(line1, line2)
    jd_int = int(jd)
    fr = jd - jd_int
    error_code, position, _ = satellite.sgp4(jd_int, fr)
    
    if error_code != 0:
        raise RuntimeError(f"Error in propagation: {error_code}")
    
    print(f"Position (ECI): {position}")
    lat, lon = eci_to_lat_lon(position, jd)
    return lat, lon

def main():
    file_path = "C:\\Users\\HP\\Desktop\\Python Scripts\\spacetrack_TLE.txt"
    tle_data = read_tle_from_file(file_path)
    
    if len(tle_data) < 2:
        raise ValueError("Insufficient TLE data in the file")
    
    for i in range(0, len(tle_data), 3):
        if i + 2 < len(tle_data):
            sat_name = tle_data[i]
            line1 = tle_data[i + 1]
            line2 = tle_data[i + 2]
            jd = parse_jday_from_tle(line1)
            latitude, longitude = tle_to_lat_lon(line1, line2, jd)
            print(f"Satellite Name: {sat_name}")
            print(f"Latitude: {latitude:.6f}")
            print(f"Longitude: {longitude:.6f}")

if __name__ == "__main__":
    main()
