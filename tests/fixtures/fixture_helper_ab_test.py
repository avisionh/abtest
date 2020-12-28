import pytest


@pytest.fixture()
def out_report_conversions():
    print("Percentage of control users who saw ['old_page']: 60.0%")
    return 1, 0.3333333333333333
