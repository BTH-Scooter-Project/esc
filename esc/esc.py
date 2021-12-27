"""esc.

Electric scooter (esc) emulator
"""

import requests
from math import radians, cos, sin, asin, atan2, sqrt, degrees
from time import time
from random import randrange, uniform
from api import Api
# from colorama import Fore, Back

travel_points = 5


class ESCEmulator:
    """Define esc class for sec simulation."""

    EARTH_RADIUS = 6378100  # Mean radius of earth in kilometers
    POSITION_TOLERANCE = 1  # tolerance for calculating current position (gps)

    def __init__(self, _id, interval=10):
        """Init."""
        self.bike_id = _id
        self.api = None
        self.esc_properties = {}
        self.esc_state = {}
        self.system_properties = {}
        self.fetch_state(_id, interval)

        print(self.calc_distance(self.esc_state['current_position'], self.system_properties['destination']))
        # print(self.esc_state['current_position'], self.system_properties['path'])
        # print(self.system_properties['path_distances'])

    def fetch_state(self, _id, interval):
        """Fetch bike state."""
        self.api = Api(_id)
        self.esc_properties = {
            "id": _id,
            "battery_capacity": self.api.bike_state['battery_capacity'],  # in seconds
            "max_speed": self.api.bike_state['max_speed']  # max speed in km/h
        }
        self.esc_state = {
            "speed": 0,  # current speed in km/h
            "rent_time": 0.,  # total rent time
            "start_timestamp": time(),
            "battery_level": self.api.bike_state['battery_level'],  # battery level in seconds
            "current_position": [  # gps coordinates of the current position
                self.api.bike_state['gps_lat'],
                self.api.bike_state['gps_lon']
            ],
            "locked": False  # Boolean
        }
        destination = [  # gps coordinates of the destination (finish) position
            self.api.bike_state['dest_lat'],
            self.api.bike_state['dest_lon']
        ]
        self.system_properties = {
            "destination": destination,  # gps coordinates of the destination (finish) position
            "sleep_time": interval,  # in seconds
            "travel_points": travel_points,  # number of travel gps-coordinates along the path
            "allowed_area": [
                [self.api.bike_state['gps_left_lat'], self.api.bike_state['gps_left_lon']],
                [self.api.bike_state['gps_right_lat'], self.api.bike_state['gps_right_lon']]
            ],
            "path": self.generate_random_path(
                self.esc_state['current_position'],
                destination,
                travel_points
            )
        }

        # self.system_properties['path'].append(destination)
        self.system_properties['path_distances'] = self.calc_path_distances()
        print(f"Start position: {self.esc_state['current_position']}")
        print(f"Destination   : {destination}")

    def calc_path_distances(self):
        """Calculate path distances."""
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
        """Calculate distances between start and end."""
        # The math module contains a function named
        # radians which converts from degrees to radians.
        lat1 = radians(start[0])
        lat2 = radians(end[0])
        long1 = radians(start[1])
        long2 = radians(end[1])

        # Haversine formula
        dist_long = long2 - long1
        dist_lat = lat2 - lat1
        a = sin(dist_lat / 2)**2 + cos(lat1) * cos(lat2) * sin(dist_long / 2)**2

        c = 2 * asin(sqrt(a))

        # calculate the result distance
        return c * cls.EARTH_RADIUS

    @staticmethod
    def generate_random_path(start, end, travel_points):
        """Generate travel_points gps-coordinates between start and end."""
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
        path.append(end)
        return path

    @staticmethod
    def bearing(start, end):
        """Calculate bearing between two gps-coordinates.

        ... see https://www.lifewire.com/what-is-bearing-in-gps-1683320
        """
        lat1 = radians(start[0])
        lat2 = radians(end[0])
        long1 = radians(start[1])
        long2 = radians(end[1])
        delta_long = (long2 - long1)

        y = sin(delta_long) * cos(lat2)
        x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(delta_long)

        return atan2(y, x)
        # delta_long = end[1] - start[1]
        # x = cos(end[0]) * sin(delta_long)
        # y = cos(start[0]) * sin(end[0]) - sin(start[0]) * cos(end[0]) * cos(delta_long)
        # return atan2(x, y)

    @classmethod
    def destination_coordinates(cls, start, speed, travel_time, bearing):
        """Return the destination point from a given point.

        having travelled the given distance on the given initial bearing.
        see http://www.movable-type.co.uk/scripts/latlong.html
        """
        distance = speed * travel_time / cls.EARTH_RADIUS
        radial_bearing = radians(bearing)

        lat = radians(start[0])
        long = radians(start[1])

        # sinφ1*cosδ + cosφ1*sinδ*cosθ
        sin_phi2 = sin(lat) * cos(distance) + cos(lat) * sin(distance) * cos(radial_bearing)
        phi2 = asin(sin_phi2)
        y = sin(radial_bearing) * sin(distance) * cos(lat)
        x = cos(distance) - sin(lat) * sin_phi2
        lambda2 = long + atan2(y, x)

        new_lat = degrees(phi2)
        new_long = (degrees(lambda2) + 540) % 360 - 180   # normalise to −180..+180°

        # print(start)
        # print(new_lat, new_long)
        return [new_lat, new_long]

    def report_log(self, destination_reached, canceled=False):
        """Send log to the backend/API."""
        log_obj = {
            "battery_level": self.esc_state['battery_level'],
            "gps_lat": self.esc_state['current_position'][0],
            "gps_lon": self.esc_state['current_position'][1],
            "rent_time": self.esc_state['rent_time'],
            "canceled": 'true' if canceled or destination_reached or self.esc_state['battery_level'] == 0 else 'false',
            "destination_reached": 'true' if destination_reached else 'false'
        }
        # if destination_reached or self.esc_state['battery_level'] == 0:
        #     log_obj['canceled'] = True
        """ Uncomment if needed for indicating battery level by colour
        battery_percentage = self.esc_state['battery_level'] / self.esc_properties['battery_capacity']
        text_color_after = Fore.RESET + Back.RESET
         text_color = Fore.BLACK + Back.GREEN
        match battery_percentage:
            case battery_percentage if battery_percentage < 0.7:
                text_color = Fore.BLACK + Back.YELLOW
            case battery_percentage if battery_percentage < 0.1:
                text_color = Fore.BLACK + Back.RED
        """
        # print(text_color + json.dumps(log_obj) + text_color_after)
        log_url = self.api.config['BASE_URL'] + f'/v1/travel/bike/{self.bike_id}?apiKey=' + self.api.config['API_KEY']
        headers_obj = {
            'x-access-token': self.api.token,
        }
        req = requests.put(
            log_url,
            headers=headers_obj,
            data=log_obj
        )
        res_data = req.json()['data']
        if destination_reached:
            print("The ride is finished!")
            print(res_data)
        if log_obj['canceled'] == 'true' or res_data['canceled'] == 'true':
            print('Rent canceled by the customer, quiting ...')
            return True
        return False

    def ride_bike(self):
        """Move bike to the next position (gps coordinate)."""
        speed = randrange(5, self.esc_properties['max_speed']) * 1000. / 3600

        # traveled max distance in [m] for a time period and for battery level
        time_limited_max_distance = speed * self.system_properties['sleep_time']

        battery_limited_max_distance = speed * self.esc_state['battery_level']
        max_distance = min(time_limited_max_distance, battery_limited_max_distance)

        # calculate total used time (could be shorter then time_left due to low battery level)
        used_time = max_distance / speed

        finished = False
        destination_reached = False
        remaining_distance = max_distance
        current_position = self.esc_state['current_position']
        for path_distance in list(self.system_properties['path_distances']):
            # print(f'path_distance: {path_distance}, remaining_distance: {remaining_distance}')
            if remaining_distance <= path_distance:
                self.esc_state['current_position'] = self.system_properties['destination']
                break
            self.system_properties['path_distances'].pop(0)  # remove distance from the original path_distance list
            remaining_distance = remaining_distance - path_distance
            current_position = self.system_properties['path'].pop(0)

        if self.system_properties['path']:  # if not empty
            bearing_path_position = self.system_properties['path'].pop(0)
            # remove the current path_distance from the path distances array
            path_distance = self.system_properties['path_distances'].pop(0)
            remaining_travel_time = remaining_distance / speed  # in seconds
            self.esc_state['current_position'] = self.destination_coordinates(
                current_position,
                speed,
                remaining_travel_time,
                self.bearing(current_position, bearing_path_position)
            )
            if remaining_distance > 0:
                # ... and replace it with the remaining distance
                self.system_properties['path_distances'].insert(0, path_distance - remaining_distance)
                self.system_properties['path'].insert(0, bearing_path_position)  # put back last path position

        if remaining_distance > 0 and not self.system_properties['path']:
            used_time = used_time - remaining_distance / speed

        # discharge the battery for the whole traveled distance to be
        self.esc_state['battery_level'] = self.esc_state['battery_level'] - used_time

        # discount the rent_time too
        self.esc_state['rent_time'] = self.esc_state['rent_time'] + used_time

        if not self.system_properties['path']:
            # if path list is empty we've reached the destination
            destination_reached = True
        if destination_reached or self.esc_state['battery_level'] == 0:
            finished = True
        if destination_reached:
            self.esc_state['current_position'] = self.system_properties['destination']

        ret = {
            "finished": finished,
            "destination_reached": destination_reached,
            "canceled": self.report_log(destination_reached)
        }
        return ret
