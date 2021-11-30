"""
    esc.py
    Electric scooter (esc) emulator
"""
from math import radians, cos, sin, asin, atan2, sqrt, pi
from time import time
from random import random, randrange


class ESCEmulator:
    """Define esc class for sec simulation"""
    EARTH_RADIUS = 6371  # Mean radius of earth in kilometers
    POSITION_TOLERANCE = 1  # tolerance for calculating current position (gps)

    def __init__(self, esc_properties, esc_state, system_properties):
        """ esc_properties: id,
                            battery_capacity,
                            max_speed=30
            esc_state:  battery_level,
                        current_position,
                        locked
            system_properties:  destination,
                                sleep_time,
                                travel_points=5,
                                allowed_area=[[59.351495, 18.023087], [59.305341, 18.168215]]
        """
        self.esc_properties = dict(
            id=esc_properties['id'],
            battery_capacity=esc_properties['battery_capacity'],  # in seconds
            max_speed=esc_properties['max_speed']  # max speed in km/h
        )
        self.esc_state = dict(
            speed=0,  # current speed in km/h
            total_time=0.,
            rent_time=0.,  # total rent time
            start_timestamp=time(),
            battery_level=esc_state['battery_level'],  # battery level in seconds
            current_position=esc_state['current_position'],  # gps coordinates of the current position
            locked=esc_state['locked']  # Boolean
        )
        self.system_properties = dict(
            destination=system_properties['destination'],  # gps coordinates of the destination (finish) position
            sleep_time=system_properties['sleep_time'],  # in seconds
            travel_points=system_properties['travel_points'],  # number of travel gps-coordinates along the path
            allowed_area=system_properties['allowed_area'],  # Boolean
            path=self.generate_random_path(
                esc_state['current_position'],
                system_properties['destination'],
                system_properties['travel_points']
            ),
            path_distances=self.calc_path_distances(self.system_properties['path'])
        )

        self.sim_properties['path'].append(system_properties['destination'])

    @staticmethod
    def calc_path_distances(path):
        if path.length < 2:
            raise IndexError("path needs to have at least 2 coordinates!")
        path_distances = []
        start_point = path[0]
        for gps in path[1:]:
            distance = ESCEmulator.calc_distance(start_point, gps)
            path_distances.append(distance)
            start_point = gps
        return path_distances

    @classmethod
    def calc_distance(cls, start, end):
        # The math module contains a function named
        # radians which converts from degrees to radians.
        lat1 = start[0]
        long1 = start[1]
        lat2 = end[0]
        long2 = end[1]

        long1 = radians(long1)
        long2 = radians(long2)
        lat1 = radians(lat1)
        lat2 = radians(lat2)

        # Haversine formula
        dist_long = long2 - long1
        dist_lat = lat2 - lat1
        a = sin(dist_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dist_long / 2) ** 2

        c = 2 * asin(sqrt(a))

        # calculate the result distance
        return c * cls.EARTH_RADIUS

    @staticmethod
    def generate_random_path(start, end, travel_points):
        # Generate nr_points gps-coordinates between start and end
        path = []
        next_lat = start[0]
        end_lat = end[0]
        next_long = start[0]
        end_long = end[0]
        for i in range(travel_points):
            next_lat = next_lat + (end_lat - next_lat) * random()
            next_long = next_long + (end_long - next_long) * random()
            path.append([next_lat, next_long])
        return path

    @staticmethod
    def to_radians(v):
        return v * pi / 180

    @staticmethod
    def to_degrees(v):
        return v * 180 / pi

    @staticmethod
    def bearing(start, end):
        # calculate bearing between two gps-coordinates
        # see https://www.lifewire.com/what-is-bearing-in-gps-1683320
        delta_long = abs(end[1] - start[1])
        x = cos(end[0]) * sin(delta_long)
        y = cos(start[0]) * sin(end[0]) - sin(start[0]) * cos(end[0]) * cos(delta_long)
        return atan2(x, y)

    @classmethod
    def destination_coordinates(cls, start, speed, travel_time, bearing):
        """
            Returns the destination point from a given point,
            having travelled the given distance on the given initial bearing.
            see http://www.movable-type.co.uk/scripts/latlong.html
        """
        lat = start[0]
        long = start[1]

        distance = speed * travel_time

        # sinφ2 = sinφ1·cosδ + cosφ1·sinδ·cosθ
        # tanΔλ = sinθ·sinδ·cosφ1 / cosδ−sinφ1·sinφ2
        # see http://mathforum.org/library/drmath/view/52049.html for derivation

        delta = distance / cls.EARTH_RADIUS
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

    def report_log(self):
        """ Send log"""

    def ride_bike(self):
        """ move bike to next position
        """
        time_left = self.system_properties['sleep_time']
        speed = randrange(5, self.esc_properties['max_speed'])
        # traveled max distance in [m] for a time period and for battery level
        time_limited_max_distance = speed * time_left * 1000. / 3600
        battery_limited_max_distance = speed * self.esc_state['battery_level'] * 1000. / 3600
        max_distance = min(time_limited_max_distance, battery_limited_max_distance)
        battery_left = True
        if time_limited_max_distance >= battery_limited_max_distance:
            battery_left = False
        destination_reached = False
        remaining_distance = max_distance
        for ix, path_distance in enumerate(self.esc_properties['path_distances']):
            if remaining_distance < path_distance:
                break
            remaining_distance = remaining_distance - path_distance

            destination = self.system_properties['path'].pop(0)
            traveled_distance = self.calc_distance(self.esc_state['current_position'], destination)
            traveled_time = traveled_distance / speed / 3600  # in seconds
            self.esc_state['current_position'] = self.destination_coordinates(
                self.esc_state['current_position'],
                speed,
                traveled_time,
                self.bearing(self.esc_state['current_position'], destination)
            )
            if traveled_time <= self.system_properties['sleep_time']:
                self.esc_state['current_position'] = destination
                self.esc_state['rent_time'] = self.esc_state['rent_time'] + traveled_time
                self.system_properties['sleep_time'].insert(0, destination)
            time_left = time_left - traveled_time
        self.report_log()
