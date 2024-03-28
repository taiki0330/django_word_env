from django import template
import datetime

register = template.Library()

@register.filter
def to_japanese_era(value):
    if not isinstance(value, datetime.date):
        return value

    # ここでは令和の例だけを示しますが、必要に応じて平成、昭和などを追加してください
    reiwa_start_date = datetime.date(2019, 5, 1)
    if value >= reiwa_start_date:
        era_name = '令和'
        era_year = value.year - 2018
    else:
        era_name = '平成'  # 仮の処理。実際には正しい年号を計算する必要があります。
        era_year = value.year - 1988  # 仮の計算。実際には正しい計算を行う必要があります。

    if era_year == 1:
        era_year = '元'

    return f'{era_name}{era_year}年{value.month}月{value.day}日'