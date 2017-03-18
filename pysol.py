#!/usr/bin/env python3

"""
A little app that show sun rise/set and twilight times.
"""

import argparse
import math
import datetime

import ephem
import ephem.cities


def query(city, **kwargs):
    result = ""

    try:
        obs = ephem.cities.lookup(city)
    except ValueError as ve:
        return ve
    except Exception as ee: # pylint:disable=broad-except
        return ee

    lat_str = str(math.degrees(obs.lat))
    lon_str = str(math.degrees(obs.lon))

    if "short" not in kwargs:
        result += obs.name + "\n" + "Latitude:  " + lat_str + "\n" + "Longtitude: " + lon_str
    else:
        result = lat_str + ":" + lon_str

    return result

def calc(lat_str, lon_str):
    def noon_utc_today():
        now_local = datetime.datetime.now()
        noon_local = datetime.datetime(now_local.year, now_local.month, now_local.day, 12)
        noon_local_ts = noon_local.timestamp()
        noon_utc = datetime.datetime.utcfromtimestamp(noon_local_ts)
        return noon_utc

    def calc_up_down(sun, obs, horizon):
        obs.horizon = horizon
        use_center = False if horizon == "0" else True
        up = None
        down = None

        try:
            up = ephem.localtime(obs.previous_rising(sun, use_center=use_center))
        except (ephem.NeverUpError, ephem.AlwaysUpError):
            pass

        try:
            down = ephem.localtime(obs.next_setting(sun, use_center=use_center))
        except (ephem.NeverUpError, ephem.AlwaysUpError):
            pass

        return (up, down)

    times = []

    lat = math.radians(float(lat_str))
    lon = math.radians(float(lon_str))

    noon = noon_utc_today()
    obs = ephem.Observer()
    obs.date = noon
    obs.lat = lat
    obs.lon = lon
    sun = ephem.Sun()

    times.append(calc_up_down(sun, obs, "0"))
    times.append(calc_up_down(sun, obs, "-6"))
    times.append(calc_up_down(sun, obs, "-12"))
    times.append(calc_up_down(sun, obs, "-18"))

    return times

def report(times):
    response = \
        "Sun rise:           %s    Sun set:          %s\n" \
        "Civil begin:        %s    Civil end:        %s\n" \
        "Nautical begin:     %s    Nautical end:     %s\n" \
        "Astronomical begin: %s    Astronomical end: %s\n" % ( \
        format_time(times[0][0]), format_time(times[0][1]), \
        format_time(times[1][0]), format_time(times[1][1]), \
        format_time(times[2][0]), format_time(times[2][1]), \
        format_time(times[3][0]), format_time(times[3][1]))

    return response


def format_time(dtime, **kwargs):
    if dtime is None:
        return "-"
    if "at_format" in kwargs and kwargs["at_format"]:
        return dtime.strftime("%H%M %b %d, %Y")
    return dtime.strftime("%Y-%m-%d %H:%M:%S")

def handle_args():
    parser = argparse.ArgumentParser(description="A little app that calculates sun rise/set and twilight times")
    subparsers = parser.add_subparsers(help='commands')

    # Ensure that a command is present (weird!).
    subparsers.required = True
    subparsers.dest = "command"

    calc_parser = subparsers.add_parser("calc", help="Calculate solar rise/set times")
    calc_parser.add_argument("--lat", action="store", type=float, required=True, help="Location latitude> (degrees)")
    calc_parser.add_argument("--lon", action="store", type=float, required=True, help="Location longitude> (degrees)")
    calc_parser.add_argument("--rise", action="store_true", default=False, help="Output sun rise time")
    calc_parser.add_argument("--set", action="store_true", default=False, help="Output sun set time")
    calc_parser.add_argument("--civil-begin", action="store_true", default=False, help="Output civil twilight begin time")
    calc_parser.add_argument("--civil-end", action="store_true", default=False, help="Output civle twilight end time")
    calc_parser.add_argument("--nautical-begin", action="store_true", default=False, help="Output nautical twilight begin time")
    calc_parser.add_argument("--nautical-end", action="store_true", default=False, help="Output nautical twilight end time")
    calc_parser.add_argument("--astronomical-begin", action="store_true", default=False, help="Output astronomical twilight begin time")
    calc_parser.add_argument("--astronomical-end", action="store_true", default=False, help="Output astronomical twilight end time")
    calc_parser.add_argument("--at-format", action="store_true", default=False, help="Output times in `at(1)' format")

    query_parser = subparsers.add_parser("query", help="Query city database")
    query_parser.add_argument("city", type=str, help="City to search for (Internet connection required)")

    parsed_args = parser.parse_args()

    if hasattr(parsed_args, "city"):
        print(query(parsed_args.city))

    elif hasattr(parsed_args, "lat"):
        times = calc(parsed_args.lat, parsed_args.lon)
        show_report = True
        at_format = parsed_args.at_format

        if parsed_args.rise:
            print(format_time(times[0][0], at_format=at_format))
            show_report = False
        if parsed_args.set:
            print(format_time(times[0][1], at_format=at_format))
            show_report = False
        if parsed_args.civil_begin:
            print(format_time(times[1][0], at_format=at_format))
            show_report = False
        if parsed_args.civil_end:
            print(format_time(times[1][1], at_format=at_format))
            show_report = False
        if parsed_args.nautical_begin:
            print(format_time(times[2][0], at_format=at_format))
            show_report = False
        if parsed_args.nautical_end:
            print(format_time(times[2][1], at_format=at_format))
            show_report = False
        if parsed_args.astronomical_begin:
            print(format_time(times[3][0], at_format=at_format))
            show_report = False
        if parsed_args.astronomical_end:
            print(format_time(times[3][1], at_format=at_format))
            show_report = False

        if show_report:
            print(report(times))

    else:
        assert False


if __name__ == "__main__": #pragma: no cover

    # Now start app.
    try:
        _ = handle_args()

    finally:
        pass


