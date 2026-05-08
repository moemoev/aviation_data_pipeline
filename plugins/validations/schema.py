import pandera.pandas as pa

from pandera import Column, Check

aviation_schema = pa.DataFrameSchema({
    "time": Column(int, checks=[
        Check.gt(0, element_wise=True, error="time must be greate than 0")]),
    "icao240": Column(str),
    "callsign": Column(str),
    "origin_country": Column(str),
    "time_position": Column(float),
    "last_contact": Column(int),
    "longitude": Column(float),
    "latitude": Column(float),
    "baro_altitude": Column(float),
    "on_ground":Column(bool),
    "velocity": Column(float),
    "true_track": Column(float),
    "vertical_rate": Column(float),
    "sensors": Column(str),
    "geo_altitude": Column(float),
    "squawk":Column(str),
    "spi":Column(bool),
    "position_source":Column(int),
})