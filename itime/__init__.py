import warnings
from datetime import datetime, timedelta


def _get_fmt_dict(delimiters=['', '-', '/']):
    """init & construct time format"""
    date_fmt_tmpl = "%Y{}%m{}%d"
    time_fmt_tmpl = date_fmt_tmpl + " %H:%M:%S"

    fmt_dict = {}
    for deli in delimiters:
        fmt_dict.update({f'date{deli}': date_fmt_tmpl.format(deli, deli)})
        fmt_dict.update({f'time{deli}': time_fmt_tmpl.format(deli, deli)})
    return fmt_dict


class iTime:
    def __init__(self, data, is_ms=False):
        """
        beijing time, tz = 8, utc time, tz = 0
        :param data: input time, support str, uts, and datetime;
         if custom format use strip to init.
        :param is_ms: Valid only if data is uts.
        """
        self._TIME_FMT_DICT = _get_fmt_dict()
        self.dt = None
        if isinstance(data, str):
            self._from_str(data)
        elif isinstance(data, int) or isinstance(data, float):
            self._from_uts(data, is_ms)
        elif isinstance(data, datetime):
            self._from_dt(data)
        else:
            raise NotImplementedError(f'iTime init failed, expected types: '
                                      f'[str, int, float, datetime], got: {type(data)}.')

    def _from_str(self, str_):
        """Init from str, only can init from predefined formats, e.g.
        "%Y{}%m{}%d", "%Y{}%m{}%d %H:%M:%S" delimiters is ['','-','/'],
        other formats for example %Y-%m, %Y-%m-%d %H:%M etc should be
        inited with staticmethod iTime.strp()
        """
        _dt = None
        fmt_list = list(self._TIME_FMT_DICT.values())
        for _fmt in fmt_list:
            try:
                _dt = datetime.strptime(str_, _fmt)
            except Exception:
                pass
        if _dt is None:
            raise TypeError(f"iTime input format wrong, expected [{', '.join(fmt_list)}], got: {str_}")
        self.dt = _dt

    def _from_uts(self, uts_, is_ms):
        """Init from unix timestamp"""
        data = uts_
        if is_ms:
            data /= 1000.
        try:
            _dt = datetime.fromtimestamp(data)
        except ValueError:
            _dt = datetime.fromtimestamp(data / 1000.)
            warnings.warn(f"iTime init from millisecond unix timestamp should specified is_ms=True.")
        self.dt = _dt

    def _from_dt(self, dt):
        """Init from datetime.datetime object"""
        self.dt = dt

    def uts(self, is_ms=False) -> int:
        """Get unix timestamp"""
        _uts = self.dt.timestamp()
        if is_ms:
            return int(_uts * 1000)
        else:
            return int(_uts)

    def date_str(self, deli='-'):
        return self.dt.strftime(self._TIME_FMT_DICT.get(f'date{deli}'))

    def time_str(self, deli='-'):
        return self.dt.strftime(self._TIME_FMT_DICT.get(f'time{deli}'))

    def strf(self, fmt="%Y-%m-%d %H:%M:%S"):
        return self.dt.strftime(fmt)

    def pop(self):
        return self.dt

    def __str__(self):
        return self.time_str()

    def delta(self, days=0, seconds=0, minutes=0, hours=0):
        _dt = self.dt + timedelta(days=days, seconds=seconds, minutes=minutes, hours=hours)
        return _new_itime(_dt)

    def ds(self, hours=None, minutes=None, seconds=None):
        """down sample time
        Examples:
        time: '2021-07-21 23:23:12'
        hours = 5  >>> '2021-07-21 20:00:00'
        hours = 23 >>> '2021-07-21 23:00:00'
        minutes = 5 >>> '2021-07-21 23:20:00'
        seconds = 5 >>> '2021-07-21 23:23:10'
        """
        _today = self.today().uts()
        _diff = self.uts() - _today
        _div = 0
        if hours is not None:
            assert 1 <= hours <= 24
            _div += 3600 * hours
        if minutes is not None:
            assert 1 <= minutes <= 60
            _div += 60 * minutes
        if seconds is not None:
            assert 1 <= seconds <= 60
            _div += seconds
        if _div == 0:
            raise Exception('iTime floor unmodified input.')
        _floor = _diff // _div * _div
        return _new_itime(_today + _floor)

    def get_date(self):
        """2021-08-01 12:12:00 -> 2021-08-01 00:00:00(iTime)"""
        return _new_itime(self.date_str())

    @staticmethod
    def now():
        return _new_itime(datetime.now())

    @staticmethod
    def today():
        return _new_itime(datetime.today().strftime("%Y-%m-%d"))

    @ staticmethod
    def strp(d_str, fmt):
        _dt = datetime.strptime(d_str, fmt)
        return _new_itime(_dt)


def _new_itime(data, is_ms=False):
    """In order to construct new instance for some iTime method"""
    return iTime(data, is_ms)


__all__ = ['iTime']
