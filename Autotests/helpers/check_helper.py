from pytest_check import check

def check_api_error(response, expected_status_code: int, expected_message=None):
    check.equal(
        response.status_code, expected_status_code,
        f"\nExpected status code: {expected_status_code}\nActual status code: {response.status_code}"
    )
    if expected_message:
        actual_error = response.text
        check.is_in(
            expected_message, actual_error,
            f'\nExpected error: {expected_message}\nActual error: {actual_error}'
        )
