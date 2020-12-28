import pytest


@pytest.fixture()
def out_report_conversions():
    print("Percentage of control users who saw ['old_page']: 60.0%")
    return 1, 3, 0.3333333333333333


@pytest.fixture()
def baseline_rate():
    return 0.1204


@pytest.fixture()
def out_get_sample_size():
    print("Required sample size: 17210 per group")
    return 17210.118424055283
