# coding: utf-8


import re
import warnings
from datetime import datetime, timedelta


def _init_default_time_format(date_seps, time_seps):
    fmt_dict = dict()
    date_tpl = "%Y{}%m{}%d"
    time_tpl = "%H{}%M{}%S"
    for d_sep in date_seps:
        for t_sep in time_seps:
            fmt_dict[f'd{d_sep}'] = date_tpl.format(d_sep, d_sep)
            fmt_dict[f't{t_sep}'] = time_tpl.format(t_sep, t_sep)
            fmt_dict[f'dt{d_sep}{t_sep}'] = f"{date_tpl.format(d_sep, d_sep)} " \
                                            f"{time_tpl.format(t_sep, t_sep)}"
    return fmt_dict


def _get_fmt(d_sep, t_sep, default_fmt):
    """get pre-defined time format by d_sep & t_sep"""
    head = ''
    if d_sep is not None:
        head += 'd'
    else:
        d_sep = ''
    if t_sep is not None:
        head += 't'
    else:
        t_sep = ''
    try:
        fmt = _FMT_DICT[f'{head}{d_sep}{t_sep}']
    except Exception:
        fmt = default_fmt
        warnings.warn(f"Time format date_sep excepted {_DEF_DATE_SEPS}, got '{d_sep}';"
                      f" time_sep excepted {_DEF_TIME_SEPS}, got '{t_sep}',"
                      f" use default '{fmt}', just use iTime.strf() get format time want.")
    return fmt


_DEF_DATE_SEPS = ['-', '/', '']
_DEF_TIME_SEPS = [':', '']
_FMT_DICT = _init_default_time_format(_DEF_DATE_SEPS, _DEF_TIME_SEPS)
_FMT_LIST = list(_FMT_DICT.values())
_FMT_UNIT = ['%Y', '%m', '%d', '%H', '%M', '%S']


class iTime:
    def __init__(self, data, is_ms=False):
        """
        beijing time, tz = 8, utc time, tz = 0
        :param data: input time, support str, uts, and datetime;
         if custom format use strip to init.
        :param is_ms: Valid only if data is uts.
        """
        self._dt = None
        if isinstance(data, str):
            self._from_str(data)
        elif isinstance(data, int) or isinstance(data, float):
            self._from_uts(data, is_ms)
        elif isinstance(data, datetime):
            self._from_dt(data)
        elif isinstance(data, list) or isinstance(data, tuple):
            self._from_timetuple(data)
        else:
            raise NotImplementedError(f'iTime init failed, expected types: '
                                      f'[str, int, float, datetime, timetuple], got: {type(data)}.')

    def _from_str(self, str_):
        """Init from str, only can init from predefined formats, e.g.
        "%Y{}%m{}%d", "%Y{}%m{}%d %H:%M:%S" sep in ['','-','/'],
        other formats for example %Y-%m, %Y-%m-%d %H:%M etc should be
        inited with staticmethod iTime.strp()
        """
        _dt = None
        for _fmt in _FMT_LIST:
            try:
                _dt = datetime.strptime(str_, _fmt)
                break
            except Exception:
                pass
        if _dt is None:
            raise TypeError(
                f"iTime input format wrong, expected [{', '.join(_FMT_LIST)}], got: {str_}")
        self._dt = _dt

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
        self._dt = _dt

    def _from_dt(self, dt):
        """Init from datetime.datetime object"""
        self._dt = dt

    def _from_timetuple(self, timetuple):
        assert len(timetuple) == 6
        timetuple = list(map(str, timetuple))
        datetime_str = f"{'-'.join(timetuple[:3])} {':'.join(timetuple[3:])}"
        self._dt = _new_itime(datetime_str).pop()

    def uts(self, is_ms=False) -> int:
        """Get unix timestamp"""
        _uts = self._dt.timestamp()
        if is_ms:
            return int(_uts * 1000)
        else:
            return int(_uts)

    def date_str(self, date_sep='-'):
        fmt = _get_fmt(d_sep=date_sep, t_sep=None, default_fmt=_FMT_DICT.get('d-'))
        return self._dt.strftime(fmt)

    def time_str(self, time_sep=':'):
        fmt = _get_fmt(d_sep=None, t_sep=time_sep, default_fmt=_FMT_DICT.get('t:'))
        return self._dt.strftime(fmt)

    def datetime_str(self, date_sep='-', time_sep=':'):
        fmt = _get_fmt(d_sep=date_sep, t_sep=time_sep, default_fmt=_FMT_DICT.get('dt-:'))
        return self._dt.strftime(fmt)

    def strf(self, fmt="%Y-%m-%d %H:%M:%S"):
        return self._dt.strftime(fmt)

    def pop(self):
        return self._dt

    def __str__(self):
        return self.datetime_str()

    def delta(self, days=0, seconds=0, minutes=0, hours=0):
        _dt = self._dt + timedelta(days=days, seconds=seconds, minutes=minutes, hours=hours)
        return _new_itime(_dt)

    def ds(self, hours=None, minutes=None, seconds=None):
        """down sample time
        Examples:
        it = iTime('2021-07-21 23:23:12')
        >>> it.ds(hours=5)
        '2021-07-21 20:00:00'
        >>> it.ds(hours=23)
        '2021-07-21 23:00:00'
        >>> it.ds(minutes=5)
        '2021-07-21 23:20:00'
        >>> it.ds(seconds=5)
        '2021-07-21 23:23:10'
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

    def join(self, time_str: str, fmt='%H:%M:%S'):
        """Join iTime self with given time str
        Notice: There is no date or time range checking, be careful
        >>> iTime('2021-08-01 12:12:00').join('10:00:00')
        iTime('2021-08-01 10:00:00')
        >>> iTime('2021-08-01 12:12:00').join('09', '%m')
        iTime('2021-09-01 10:00:00')
        """
        src_dt_list = re.split(r'[- :]', self.datetime_str())
        dst_dt_list = re.split(r'[- :]', iTime.strp(time_str, fmt).datetime_str())
        for idx, f in enumerate(_FMT_UNIT):
            if f in fmt:
                src_dt_list[idx] = dst_dt_list[idx]
        return _new_itime(src_dt_list)

    @staticmethod
    def now():
        return _new_itime(datetime.now())

    @staticmethod
    def today():
        return _new_itime(datetime.today().strftime("%Y-%m-%d"))

    @staticmethod
    def strp(d_str, fmt):
        _dt = datetime.strptime(d_str, fmt)
        return _new_itime(_dt)


def _new_itime(data, is_ms=False):
    """In order to construct new instance for some iTime method"""
    return iTime(data, is_ms)


__all__ = ['iTime']


if __name__ == '__main__':
    x = iTime.now().join('09', '%m')
    print(x)
