import pandera.pandas as pa
import time
from pandera import Column, Check


aviation_schema = pa.DataFrameSchema({
    "time": Column(int, checks=[
        Check.gt(0),
        Check(lambda x: x <= int(time.time()) + 60, error="time is in the future")
    ]),
    "icao24": Column(str, checks=[
        Check.str_matches(r"^[a-z0-9]{6}$"), #note: check adjusted to match data(lowercase), could/should be lowercase maybe inside DB or at time of transformation alrdy
    ]),
    "callsign": Column(str, checks=[
        Check.str_length(8)
    ]),
    "origin_country": Column(str, checks=[
        Check(lambda s: s.str.strip().str.len() > 0 )
    ]),
    "time_position": Column(int, nullable=True, checks=[
        Check.gt(0)
    ]),
    "last_contact": Column(int, checks=[
        Check.gt(0),
    ]),
    "longitude": Column(float,nullable=True,checks=[
        Check.in_range(-180., 180.0)
    ]),
    "latitude": Column(float,nullable=True,checks=[
        Check.in_range(-90., 90.0)
    ]),
    "baro_altitude": Column(float, nullable=True, checks=[
        Check.in_range(-1500, 15000)
    ]),
    "on_ground":Column(bool),
    "velocity": Column(float, nullable=True, checks=[
        Check.in_range(0, 600)
    ]),
    "true_track": Column(float, nullable=True, checks=[
        Check.in_range(0, 360, include_max=False)
    ]),
    "vertical_rate": Column(float, nullable=True, checks=[
        Check.in_range(-40, 25)
    ]),
    "sensors": Column(list[int], nullable=True),
    "geo_altitude": Column(float, nullable=True, checks=[
        Check.in_range(-500, 16000)
    ]),
    "squawk":Column(str, nullable=True, checks=[
        Check.str_matches(r"^[0-7]{4}$"),
    ]),
    "spi":Column(bool),
    "position_source":Column(int, checks=[
        Check.in_range(0, 3),
    ]),
})