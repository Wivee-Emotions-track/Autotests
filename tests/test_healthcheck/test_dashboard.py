import os
import time
import shutil

import allure
import pytest

from ui.pages.login_page import LoginPage
from ui.pages.analytics_page import AnalyticsPage
from helpers.filename_helpers import generate_filename, get_url_with_filter
from helpers.compare_csv import compare_csv_files


@pytest.fixture(scope="function")
def remove_download_files():
    download_dir = "csv_downloads"

    yield download_dir
    shutil.rmtree('csv_downloads')


@pytest.mark.parametrize(
    "compare, from_date, to_date, compareShift, dataSource, splitBy, timeFrom, timeTo, selectedMetrics", [
        (0, "2024-06-10", "2024-06-15", None, None, None, None, None, None),
        (2, "2024-06-10", "2024-06-15", 1, False, None, None, None, None),
        (2, "2024-06-10", "2024-06-15", 1, False, "zone_id", None, None, None),
        (2, "2024-06-10", "2024-06-15", 1, False, "shop_id", "02:00", "23:00", None),
        (3, "2024-06-10", "2024-06-15", None, False, "shop_id", "21:00", "23:00", None),
        (3, "2024-06-10", "2024-06-15", None, False, "shop_id", "21:00", "23:00", "engagements_per_customer,csat_avg"),
    ])
def test_check_analytics_export_file(page, get_config, compare, from_date, to_date,
                                     compareShift, dataSource, splitBy, timeFrom, timeTo,
                                     selectedMetrics):
    username = get_config['credentials']['super_user']['login']
    password = get_config['credentials']['super_user']['password']
    base_url = "https://app.wayvee.com/analytics"

    login_page = LoginPage(page, get_config['urls']['host'])
    analytics_page = AnalyticsPage(page)

    url, params = get_url_with_filter(base_url, compare, from_date, to_date,
                                      compareShift, dataSource, splitBy,
                                      timeFrom, timeTo, selectedMetrics)

    login_page.open(url)

    login_page.login(username, password)
    time.sleep(5)
    expected_filename = generate_filename(params)

    with page.expect_download() as download_info:
        analytics_page.export_data(expected_filename)
    download = download_info.value

    # Save the downloaded file to the specified directory
    download_dir = "csv_downloads"
    os.makedirs(download_dir, exist_ok=True)

    # Generate the expected filename based on the parameters
    downloaded_file_path = os.path.join(os.getcwd(), download_dir, expected_filename)
    download.save_as(downloaded_file_path)

    # Assuming the file is downloaded to the specified directory
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    expected_file = os.path.join(root_dir, 'tests', 'test_healthcheck', 'csv_examples', expected_filename)

    assert os.path.exists(downloaded_file_path), "CSV file was not downloaded."

    with allure.step("Compare downloaded CSV with expected CSV"):
        assert compare_csv_files(downloaded_file_path, expected_file), "CSV files do not match."

