import os
import allure
import pytest
from time import sleep
from ui.pages.login_page import LoginPage
from ui.pages.analytics_page import AnalyticsPage
from helpers.filename_helpers import generate_filename
from helpers.compare_csv import compare_csv_files

@pytest.mark.parametrize(
    "compare, from_date, to_date, compareShift, dataSource, splitBy, timeFrom, timeTo, selectedMetrics", [
        (0, "2024-06-10", "2024-06-15", None, None, None, None, None, None),
        (2, "2024-06-10", "2024-06-15", 1, False, None, None, None, None),
        (2, "2024-06-10", "2024-06-15", 1, False, "zone_id", None, None, None),
        (2, "2024-06-10", "2024-06-15", 1, False, "shop_id", "02:00", "23:00", None),
        (3, "2024-06-10", "2024-06-15", None, False, "shop_id", "21:00", "23:00", None),
        (3, "2024-06-10", "2024-06-15", None, False, "shop_id", "21:00", "23:00", "engagements_per_customer,csat_avg"),
    ])
def test_wayvee_dashboard(page, compare, from_date, to_date, compareShift, dataSource, splitBy, timeFrom, timeTo,
                          selectedMetrics):
    login_page = LoginPage(page)
    analytics_page = AnalyticsPage(page)
    base_url = "https://app.wayvee.com/analytics"
    params = {
        "compare": compare,
        "from": from_date,
        "to": to_date,
        "compareShift": compareShift,
        "dataSource": dataSource,
        "splitBy": splitBy,
        "timeFrom": timeFrom,
        "timeTo": timeTo,
        "selectedMetrics": selectedMetrics
    }

    # Filter out None values
    params = {k: v for k, v in params.items() if v is not None}
    query_string = "&".join([f"{key}={value}" for key, value in params.items()])
    url = f"{base_url}?{query_string}"

    with allure.step("Open login page"):
        login_page.open()

    with allure.step("Enter username and password"):
        login_page.login("testing_admin@wayvee.com", 'kz767ErQ9DvNXHuo1afB')
        sleep(5)

    with allure.step("Navigate to URL with parameters"):
        page.goto(url)
        sleep(5)

    with allure.step("Click to the Export button"):
        analytics_page.click_export()

    with allure.step("Fill the File Name and click to download button"):
        expected_filename = generate_filename(params)
        # Start waiting for the download
        with page.expect_download() as download_info:
            # Perform the action that initiates download
            analytics_page.click_download(expected_filename)
        download = download_info.value
        # Save the downloaded file to the specified directory
        download_dir = "csv_downloads"
        os.makedirs(download_dir, exist_ok=True)
        # Generate the expected filename based on the parameters
        downloaded_file_path = os.path.join(download_dir, expected_filename)
        download.save_as(downloaded_file_path)

    # Assuming the file is downloaded to the specified directory
    expected_file = f"csv_examples/{expected_filename}"  # Path to your expected CSV file


    assert os.path.exists(downloaded_file_path), "CSV file was not downloaded."

    with allure.step("Compare downloaded CSV with expected CSV"):
        assert compare_csv_files(downloaded_file_path, expected_file), "CSV files do not match."

    os.remove(downloaded_file_path)
