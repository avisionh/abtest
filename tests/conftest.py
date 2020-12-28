import pytest
import pandas as pd


pytest_plugins = [
    "tests.fixtures.fixture_helper_ab_test",
]


@pytest.fixture()
def df_ab_test():
    return pd.DataFrame(
        data={
            "user_id": [1, 2, 3, 4, 5],
            "group": ["control", "control", "treatment", "control", "treatment"],
            "landing_page": [
                "old_page",
                "old_page",
                "new_page",
                "old_page",
                "new_page",
            ],
            "converted": [0, 1, 0, 0, 1],
        }
    )
