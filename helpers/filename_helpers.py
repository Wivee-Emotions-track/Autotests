def generate_filename(params):
    filename_parts = []
    for key, value in params.items():
        if value is not None:
            # Replace special symbols with underscores and append to filename parts
            safe_value = str(value).replace(":", "").replace(",", "_").replace(" ", "_")
            filename_parts.append(f"{key}-{safe_value}")
    return "DataAnalytics-" + "-".join(filename_parts) + ".csv"