#!/usr/bin/python3
"""Generate stations within allowed area boundaries"""
from random import choices, uniform, randint

station_capacity = 20
nr_of_stations = 100
nr_of_bikes = station_capacity * nr_of_stations
allowed_area = [[59.351495, 18.023087], [59.305341, 18.168215]]


def generate_random_gps(start, end):
    start_lat = start[0]
    end_lat = end[0]
    start_long = start[1]
    end_long = end[1]

    lat = start_lat + (end_lat - start_lat) * uniform(.05, .95)
    long = start_long + (end_long - start_long) * uniform(.05, .95)
    return [lat, long]


def generate_random_stations(start, end, nr_of_stations=100):
    # Generate nr_of_stations gps-coordinates within an area
    stations = []

    for i in range(nr_of_stations):
        stations.append(generate_random_gps(start, end))
    return stations


def pick_rnd_station(stations):
    station_index = randint(0, len(stations)-1)
    return station_index, stations[station_index]


def generate_insert_bikes_statements(start, end, stations, nr_of_bikes=1000):
    insert_command = """INSERT INTO "bike" ("bikeid",
                                            "name",
                                            "image",
                                            "description",
                                            "max_speed",
                                            "battery_capacity",
                                            "status",
                                            "battery_level",
                                            "gps_lat",
                                            "gps_lon",
                                            "dest_lat",
                                            "dest_lon",
                                            "stationid",
                                            "cityid")
                        VALUES"""
    with open("bikes.sql", 'w', encoding='utf-8') as f:
        f.write(insert_command)
        my_choices = [True, False]  # True is station, False is random gps from the allowed area
        distribution = (90, 10)
        bike_id = 101
        presiding_comma = '\n'
        bat_cap = 9000
        bat_level = 9000
        for _ in range(nr_of_bikes):
            random_choice = choices(my_choices, distribution)[0]
            (station_id, gps) = pick_rnd_station(stations) if random_choice else (-1, generate_random_gps(start, end))
            random_choice = choices(my_choices, distribution)[0]
            (_, dest) = pick_rnd_station(stations) if random_choice else (_, generate_random_gps(start, end))

            values = f"""{presiding_comma}({bike_id},'bike{bike_id}.jpg','bike{bike_id}',30,{bat_cap},'vacant',
            {bat_level},{gps[0]},{gps[1]},{dest[0]},{dest[1]},{station_id},2)
"""
            f.write(values)
            presiding_comma = ','
            bike_id = bike_id + 1
        f.write(';')


def generate_insert_stations_statements(stations):
    insert_command = 'INSERT INTO "station" ("stationid","type","address","cityid","gps_lat","gps_lon") VALUES'
    with open("stations.sql", 'w', encoding='utf-8') as f:
        f.write(insert_command)
        station_id = 101
        presiding_comma = '\n'
        for station in stations:
            values = f"{presiding_comma}({station_id},'parking','Adress {station_id}',2,{station[0]},{station[1]})\n"
            f.write(values)
            presiding_comma = ','
            station_id = station_id + 1
        f.write(';')


def main():
    stations = generate_random_stations(allowed_area[0], allowed_area[1], nr_of_stations)
    generate_insert_stations_statements(stations)
    generate_insert_bikes_statements(allowed_area[0], allowed_area[1], stations, nr_of_bikes)


if __name__ == '__main__':
    main()
