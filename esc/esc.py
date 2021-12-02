"""
    esc.py
    Electric scooter (esc) emulator
"""
from math import radians, cos, sin, asin, atan2, sqrt, pi
from time import time
from random import random, randrange, uniform

interval = 5  # sleep interval


class ESCEmulator:
    """Define esc class for sec simulation"""
    EARTH_RADIUS = 6371000  # Mean radius of earth in kilometers
    POSITION_TOLERANCE = 1  # tolerance for calculating current position (gps)

    def __init__(self, _id):
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
        self.esc_properties = {}
        self.esc_state = {}
        self.system_properties = {}
        self.fetch_state(id)

        print(self.calc_distance(self.esc_state['current_position'], self.system_properties['destination']))
        # print(self.esc_state['current_position'], self.system_properties['path'])
        # print(self.system_properties['path_distances'])

    def fetch_state(self, _id):
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
        esc_properties = dict(
            battery_capacity=10000,  # in seconds
            max_speed=40  # max speed in km/h
        )
        esc_state = dict(
            battery_level=800,  # battery level in seconds
            current_position=[59.347561, 18.025832],  # gps coordinates of the current position
            locked=False  # Boolean
        )
        system_properties = dict(
            destination=[59.324783, 18.073070],  # gps coordinates of the destination (finish) position
            sleep_time=interval * 10,  # in seconds
            travel_points=1,  # number of travel gps-coordinates along the path
            allowed_area=[[59.351495, 18.023087], [59.305341, 18.168215]]  # Boolean
        )
        self.esc_properties = dict(
            id=_id,
            battery_capacity=esc_properties['battery_capacity'],  # in seconds
            max_speed=esc_properties['max_speed']  # max speed in km/h
        )
        self.esc_state = dict(
            speed=0,  # current speed in km/h
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
            )
        )

        self.system_properties['path'].append(system_properties['destination'])
        self.system_properties['path_distances'] = self.calc_path_distances()
        print(f"Start position: {esc_state['current_position']}")
        print(f"Destination   : {system_properties['destination']}")

    def calc_path_distances(self):
        if not self.system_properties['path']:
            raise IndexError("path needs to have at least 1 coordinate!")
        path_distances = []
        start_point = self.esc_state['current_position']
        for gps in self.system_properties['path']:
            distance = ESCEmulator.calc_distance(start_point, gps)
            path_distances.append(distance)
            start_point = gps
        return path_distances

    @classmethod
    def calc_distance(cls, start, end):
        # The math module contains a function named
        # radians which converts from degrees to radians.
        lat1 = start[0]
        lat2 = end[0]
        long1 = start[1]
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
        next_long = start[1]
        end_long = end[1]
        for i in range(travel_points+1, 0, -1):
            interval = 1. / i
            next_lat = next_lat + (end_lat - next_lat) * uniform(interval*.7, interval)
            next_long = next_long + (end_long - next_long) * uniform(interval*.7, interval)
            path.append([next_lat, next_long])
        # path.append(end)
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

    def fetch_properties(self):
        """ Fetch properties from backend/API """

    def report_log(self, destination_reached):
        """ Send log to the backend/API """
        print('Current position: {}, battery_level: {}'
              .format(self.esc_state['current_position'], self.esc_state['battery_level']))
        if destination_reached:
            print("The ride is finished!")

    def ride_bike(self):
        """ move bike to the next position (gps coordinate)
        """
        speed = randrange(5, self.esc_properties['max_speed']) * 1000. / 3600

        # traveled max distance in [m] for a time period and for battery level
        time_limited_max_distance = speed * self.system_properties['sleep_time']

        battery_limited_max_distance = speed * self.esc_state['battery_level']
        max_distance = min(time_limited_max_distance, battery_limited_max_distance)

        # calculate total used time (could be shorter then time_left due to low battery level)
        used_time = max_distance / speed

        remaining_distance = max_distance
        current_position = self.esc_state['current_position']
        for path_distance in list(self.system_properties['path_distances']):
            if remaining_distance <= path_distance:
                break
            self.system_properties['path_distances'].pop(0)  # remove distance from the original path_distance list
            remaining_distance = remaining_distance - path_distance
            current_position = self.system_properties['path'].pop(0)

        next_path_position = current_position
        if self.system_properties['path']:  # if not empty
            next_path_position = self.system_properties['path'].pop(0)
            # remove the current path_distance from the path distances array
            removed_path_distance = self.system_properties['path_distances'].pop(0)
        remaining_travel_time = remaining_distance / speed  # in seconds
        self.esc_state['current_position'] = self.destination_coordinates(
            current_position,
            speed,
            remaining_travel_time,
            self.bearing(current_position, next_path_position)
        )

        if remaining_distance > 0 and self.system_properties['path']:
            # ... and replace it with the remaining distance
            self.system_properties['path_distances'].insert(0, removed_path_distance - remaining_distance)
            self.system_properties['path'].insert(0, next_path_position)  # put back last path position

        if remaining_distance > 0 and not self.system_properties['path']:
            used_time = used_time - remaining_distance / speed

        # discharge the battery for the whole traveled distance to be
        self.esc_state['battery_level'] = self.esc_state['battery_level'] - used_time

        # discount the rent_time too
        self.esc_state['rent_time'] = self.esc_state['rent_time'] + used_time

        finished = False
        destination_reached = False
        if not self.system_properties['path']:
            # if path list is empty we've reached the destination
            destination_reached = True
        if destination_reached or self.esc_state['battery_level'] == 0:
            finished = True

        ret = dict(
            finished=finished,
            destination_reached=destination_reached
        )
        self.report_log(destination_reached)
        return ret
