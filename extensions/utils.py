from . import jalali
from django.utils import timezone

def jalali_converter(time):
    jmonth = [
     'فروردین',
    'اردیبهشت',
    'خرداد',
    'تیر',
    'مرداد',
    'شهریور',
    'مهر',
    'آبان',
    'آذر',
     'دی',
     'بهمن',
     'اسفند']
    time=timezone.localtime(time)
    time_to_str='{},{},{}'.format(time.year,time.month,time.day)
    time_to_tuple= jalali.Gregorian(time_to_str).persian_tuple()
    output='{} {} {}, ساعت {}:{}'.format(
        time_to_tuple[2],
        jmonth[time_to_tuple[1]],
        time_to_tuple[0],
        time.hour,
        time.minute
    )
    return output
