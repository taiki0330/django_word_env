from django import template
import datetime

register = template.Library()

@register.filter
def to_japanese_time(value):
    if not value or not isinstance(value, datetime.time):
        return value  # valueが時間オブジェクトでない場合はそのまま返す
    hour = value.hour
    minute = value.minute
    am_pm = '午前' if hour < 12 else '午後'
    hour = hour if hour <= 12 else hour - 12
    return f'{am_pm}{hour}時{minute}分'