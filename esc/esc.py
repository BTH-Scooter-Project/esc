"""
    esc.py
    Electric scooter (esc) emulator
"""
from math import radians, cos, sin, asin, atan2, sqrt, pi
from time import time


class ESCEmulator:
    """Define esc class for sec simulation"""
    earth_radius = 6371  # Mean radius of earth in kilometers
    position_tolerance = 1  # tolerance for calculating current position (gps)

    def __init__(self, _id, battery_capacity, battery_level,
                 current_position, destination, allowed_area, max_speed=30, locked=True **kwargs):
        self._id = _id
        self.battery_capacity = battery_capacity  # in seconds
        self.battery_level = battery_level  # battery level in seconds
        self.current_position = current_position  # gps coordinates of the current position
        self.destination = destination  # gps coordinates of the destination (finish) position
        self.allowed_area = allowed_area
        self.path = []
        self.max_speed = max_speed  # max speed in km/h
        self.speed = 0  # current speed in km/h
        self.total_time = 0
        self.total_distance = 0  # accumulated distance
        self.locked = locked
        self.start_ts = time()

    @classmethod
    def distance(cls, lat1, lat2, lon1, lon2):
        # The math module contains a function named
        # radians which converts from degrees to radians.
        lon1 = radians(lon1)
        lon2 = radians(lon2)
        lat1 = radians(lat1)
        lat2 = radians(lat2)

        # Haversine formula
        dist_lon = lon2 - lon1
        dist_lat = lat2 - lat1
        a = sin(dist_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dist_lon / 2) ** 2

        c = 2 * asin(sqrt(a))

        # calculate the result distance
        return c * cls.earth_radius

    @staticmethod
    def to_radians(v):
        return v * pi / 180

    @staticmethod
    def to_degrees(v):
        return v * 180 / pi

    @classmethod
    def destination_coordinates(cls, lat, long, speed, time, bearing):
        """
            Returns the destination point from a given point,
            having travelled the given distance on the given initial bearing.
        """
        distance = speed * time

        # sinφ2 = sinφ1·cosδ + cosφ1·sinδ·cosθ
        # tanΔλ = sinθ·sinδ·cosφ1 / cosδ−sinφ1·sinφ2
        # see http://mathforum.org/library/drmath/view/52049.html for derivation

        delta = distance / cls.earth_radius
        theta = cls.to_radians(bearing)

        phi1 = cls.to_radians(lat)
        lambda1 = cls.to_radians(long)

        sin_phi1 = sin(phi1)
        cos_phi1 = cos(phi1)

        sin_delta = sin(delta)
        cos_delta = cos(delta)

        sin_theta = sin(theta)
        cos_theta = cos(theta)

        # sinφ1*cosδ + cosφ1*sinδ*cosθ
        sin_phi2 = sin_phi1 * cos_delta + cos_phi1 * sin_delta * cos_theta
        phi2 = asin(sin_phi2)
        y = sin_theta * sin_delta * cos_phi1
        x = cos_delta - sin_phi1 * sin_phi2
        lambda2 = lambda1 + atan2(y, x)

        new_lat = cls.to_degrees(phi2)
        new_long = (cls.to_degrees(lambda2) + 540) % 360 - 180   # normalise to −180..+180°

        return [new_lat, new_long]

    def random_path_generator(self, nr_of_positions=15):
        """Generate random path withing allowed city area"""
