import math
import time
import threading
from gps_controller import get_gps_location, gps_data_refresh_rate_sec
from rf_transmission import broadcast_self_location, receive_other_drone_location

EARTH_RADIUS_METER = 6378137
SAFETY_DISTANCE_METER = 18.0


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Distance between 2 points in 2d space accounting for earth's curvature

    :param lat1:
    :param lon1:
    :param lat2:
    :param lon2:
    :return: Radius * C
    """

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return EARTH_RADIUS_METER * c


def destination_point(lat, lon, speed_mps, bearing_deg, duration_sec):
    """
    New Latitude and Longitude are calculated for destination point with
    given speed and bearing.
    :param lat:
    :param lon:
    :param speed_mps:
    :param bearing_deg:
    :param duration_sec:
    :return: Lat2, Lon2
    """
    distance = speed_mps * duration_sec
    bearing = math.radians(bearing_deg)
    lat1 = math.radians(lat)
    lon1 = math.radians(lon)

    lat2 = math.asin(math.sin(lat1) * math.cos(distance / EARTH_RADIUS_METER) +
                     math.cos(lat1) * math.sin(distance / EARTH_RADIUS_METER) * math.cos(bearing))

    lon2 = lon1 + math.atan2(math.sin(bearing) * math.sin(distance / EARTH_RADIUS_METER) * math.cos(lat1),
                             math.cos(distance / EARTH_RADIUS_METER) - math.sin(lat1) * math.sin(lat2))

    return math.degrees(lat2), math.degrees(lon2)


def check_potential_collision_3d(drone_self, drone_other, time_till_crash=30, time_step=1):
    """
    Calculates potential collision between two drones, and time and
    distance till potential collision.
    :param drone_self:
    :param drone_other:
    :param time_till_crash:
    :param time_step:
    :return:
    """
    for future_time in range(0, time_till_crash + 1, time_step):
        lat1, lon1 = destination_point(drone_self['lat'], drone_self['lon'], drone_self['speed'], drone_self['track'], future_time)
        lat2, lon2 = destination_point(drone_other['lat'], drone_other['lon'], drone_other['speed'], drone_other['track'], future_time)

        alt1 = drone_self['alt'] + drone_self['climb_rate'] * future_time
        alt2 = drone_other['alt'] + drone_other['climb_rate'] * future_time

        dist_2d = haversine_distance(lat1, lon1, lat2, lon2)

        delta_alt = alt2 - alt1
        dist_3d = math.sqrt(dist_2d ** 2 + delta_alt ** 2)

        # print(f"t={future_time:2d}s | dist_3d={dist_3d:.2f} m | alt1={alt1:.1f} m | alt2={alt2:.1f} m")

        if dist_3d <= SAFETY_DISTANCE_METER:
            print(f"Collision risk at t={future_time}s! 3D distance: {dist_3d:.2f} meters")
            return True

    print(f"No collision detected in the future {time_till_crash * time_step} s")
    return False


# Global variable to share data between threads
DRONE_SELF = {}


def self_location_loop():
    global DRONE_SELF
    while True:
        try:
            DRONE_SELF = get_gps_location()
            if DRONE_SELF:
                broadcast_self_location(DRONE_SELF)
            time.sleep(gps_data_refresh_rate_sec)

        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            break


DRONE_OTHER = {}


def other_location_loop():
    global DRONE_OTHER
    while True:
        try:
            DRONE_OTHER = receive_other_drone_location()
            if not DRONE_SELF or not DRONE_OTHER:
                time.sleep(0.5)
                continue
            else:
                check_potential_collision_3d(DRONE_SELF, DRONE_OTHER)
                time.sleep(1)
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    thread_1 = threading.Thread(target=self_location_loop)
    thread_2 = threading.Thread(target=other_location_loop)
    thread_1.start()
    thread_2.start()
