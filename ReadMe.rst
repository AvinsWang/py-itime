`py-itime` --- Time package supporting chain call
==================================================

py-itime is a time package supporting chain call.

install and use:

::

    pip install py-itime
    from itime import iTime


Example
-------

::

    # get datetime str of previous day with specified hours
    >>> iTime(f'{iTime.now().delta(days=-1).date_str()} 10:00:00').time_str()
    '2021-07-20 10:00:00'

    # get unix timestamp of previous day
    >>> iTime.now().delta(days=-1).uts(is_ms=True)
    1627211818635

    # get corresponding unix timestamp with specified datetime str
    >>> iTime('2021-07-20 10:00:00').uts()
    1626746400

    # get datetime str of UTC time which is converted and down sampled by local time
    >>> iTime.now().delta(hours=-8).ds(minutes=5).datetime_str()
    '2021-08-02 08:20:00'

Initialize
----------
There are 5 ways to initialize an iTime object.
::

    # 1. init with time str, format '%Y{}%m{}%d', '%Y{}%m{}%d %H{}%M{}%S' date_sep could be '','-','/', time_sep could be '',':'.
    >>> iTime('20210701')
    >>> iTime('2021-07-01 00:00:01')
    >>> iTime('2021/07/01 00:00:01')

    # 2. init with unix timestamp, support second and milliseconds, default as second
    >>> iTime(1625068800)
    >>> iTime(1625068800000, is_ms=True)    # if is milliseconds, is_ms=True
    >>> iTime(1625068800.123)               # float is also supported

    # 3. init with custom datetime str, use iTime.strp(time: str, fmt: str)
    >>> iTime('2021-07-01 12:05', fmt='%Y-%m-%d %H:%M')

    # 4. init datetime.datetime object
    >>> dt = datetime.datetime.now()
    >>> iTime(dt)

    # 5. init with timetuple
    >>> iTime((2021, 7, 1, 0, 0, 1))
    >>> iTime(['2021', '07', '01', '00', '00', '01'])


class iTime
---------------


* iTime.now() -> iTime
    get current local time.
* iTime.today() -> iTime
    get current date, hour minute second is 00:00:00.
* iTime.strp(time: str, fmt: str) -> iTime
    init iTime from custom time str format.
* iTime.uts(is_ms=False) -> int
    get unix timestamp, if is_ms=True, get milliseconds.
* iTime.date_str(date_sep='-') -> str
    get date str, sep include '', '-', '/'.
* time_str(time_sep=':') -> str
    get time str, 'time_sep' is sep include '', ':'.
* datetime_str(date_sep='-', time_sep=':') -> str
    get datetime str, date_sep and time_sep same to above.
* join(datetime_str: str, fmt: str) -> iTime
    join iTime self with given time str.
    Notice: There is no date or time range checking, be careful

::

    >>> iTime('2021-08-01 12:12:00').join('10:00:00')
    iTime('2021-08-01 10:00:00')
    >>> iTime('2021-08-01 12:12:00').join('09', '%m')
    iTime('2021-09-01 10:00:00')

* strf(fmt) -> str
    get custom time str with given fmt.
* pop() -> datetime.datetime
    get datetime.datetime object from iTime instance
* delta(days=0, seconds=0, minutes=0, hours=0) -> iTime
    get offset time.
* ds(hours=None, minutes=None, seconds=None) -> iTime
    down sample time, example as follows.

::

    >>> it = iTime('2021-07-21 23:23:12')
    >>> it.ds(hours=5)
        '2021-07-21 20:00:00'

    >>> it.ds(hours=23)
        '2021-07-21 23:00:00'

    >>> it.ds(minutes=5)
        '2021-07-21 23:20:00'

    >>> it.ds(seconds=t)
        '2021-07-21 23:23:10'

