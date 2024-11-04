from datetime import datetime


def expiry_date_difference(date_str1, date_str2):
    format_str = '%Y-%m-%dT%H:%M:%SZ'

    date1 = datetime.strptime(date_str1, '%Y-%m-%dT%H:%M:%SZ')
    date2 = datetime.strptime(date_str2, format_str)

    difference = date1 - date2
    return abs(difference.total_seconds())