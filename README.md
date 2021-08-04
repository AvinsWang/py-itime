## itime
itime对datetime的定制和功能增强. itime中的核心类为iTime类, 提供以下方法:

### 静态方法:
- now() -> iTime, 获取当前时间.
- today() -> iTime, 获取当前日期, 时分秒为00:00:00, 结合date_str()方法使用.
- strp(time_str, fmt) -> iTime, 从给定的字符串初始化iTime对象. 

### 成员方法  
- uts(is_ms=False) -> int, 返回unix时间戳, 如果is_ms=True, 则返回为毫秒格式.  
- date_str(deli='-') -> str, 获取字符串日期, deli为分隔符, 可以取'', '-', '/'.
- time_str(deli='-') -> str, 获取字符串时间, deli为分隔符, 可以取'', '-', '/'.
- strf(fmt) -> str, 获取自定义格式的时间, fmt格式同datetime格式.
- pop() -> datetime.datetime, 获取datetime.datetime对象.
- delta(days=0, seconds=0, minutes=0, hours=0) -> iTime, 获取日期偏移.
- ds(hours=None, minutes=None, seconds=None) -> iTime, 时间下采样,  
> time: '2021-07-21 23:23:12'  
> hours = 5  >>> '2021-07-21 20:00:00'  
> hours = 23 >>> '2021-07-21 23:00:00'  
> minutes = 5 >>> '2021-07-21 23:20:00'  
> seconds = 5 >>> '2021-07-21 23:23:10'  

### 初始化
1. 默认字符串初始化, "%Y{}%m{}%d", "%Y{}%m{}%d %H:%M:%S" 分隔符为'','-','/'.  
e.g. iTime('20210701'), iTime('2021/07/01 00:00:01')
2. unix时间戳初始化, 支持秒或毫秒, 默认为秒; 输入可以是int或float  
e.g. iTime(1625068800), iTime(1625068800000, is_ms=True)
3. 任意字符串格式初始化, 需要使用iTime.strp(), 且指定fmt  
e.g. iTime('2021-07-01 12:05', fmt='%Y-%m-%d %H:%M')  
4. datetime类初始化
e.g. dt = datetime.datetime.now(), iTime(dt)

### 示例
```python
# 获取前一天指定时间的字符串时间  
>>> iTime(f'{iTime.now().delta(days=-1).date_str()} 10:00:00').time_str()
2021-07-20 10:00:00
# 获取前一天的uts毫秒时间
>>> iTime.now().delta(days=-1).uts(is_ms=True)
1627211818635
# 获取字符串时间对应的uts时间
>>> iTime('2021-07-20 10:00:00').uts()
1626746400
# 获取当前时间对应的UTC时间并找到最近5分钟点,再转换成字符串
>>> iTime.now().delta(hours=-8).ds(minutes=5).time_str()
2021-08-02 08:20:00
```