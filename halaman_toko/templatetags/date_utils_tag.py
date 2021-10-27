from django import template
from datetime import datetime

register = template.Library()

@register.filter
def number_of_days_from_today(date):
    today = datetime.now().date()
    delta_time = date - today
    return delta_time.days


@register.filter
def ubah_jadi_bulan_atau_tahun_jika_perlu(number_of_days:int):
    if (number_of_days >= 30 * 12):
        return f"{number_of_days // (30*12)} Tahun"
    if (number_of_days >= 60):
        return f"{number_of_days // 30} Bulan"
    return f"{number_of_days} Hari"