def generate_filename(params):
    filename_parts = []
    for key, value in params.items():
        if value is not None:
            # Replace special symbols with underscores and append to filename parts
            safe_value = str(value).replace(":", "").replace(",", "_").replace(" ", "_")
            filename_parts.append(f"{key}-{safe_value}")
    return "DataAnalytics-" + "-".join(filename_parts) + ".csv"


def get_url_with_filter(base_url, compare, from_date, to_date, compareShift, dataSource, splitBy, timeFrom, timeto,
                        selectedMetrics):
    params = {
        "compare": compare,
        "from": from_date,
        "to": to_date,
        "compareShift": compareShift,
        "dataSource": dataSource,
        "splitBy": splitBy,
        "timeFrom": timeFrom,
        "timeTo": timeto,
        "selectedMetrics": selectedMetrics
    }

    # Filter out None values
    params = {k: v for k, v in params.items() if v is not None}
    query_string = "&".join([f"{key}={value}" for key, value in params.items()])
    url = f"{base_url}?{query_string}"

    return url, params