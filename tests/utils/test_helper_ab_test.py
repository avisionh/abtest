import src.utils.helper_ab_test as f


def test_report_conversions(df_ab_test, out_report_conversions):
    assert (
        f.report_conversions(
            data=df_ab_test,
            group_col="group",
            group_filter="control",
            convert_col="converted",
            page_col="landing_page",
        )
        == out_report_conversions
    )


def test_get_sample_size(baseline_rate, out_sample_size):
    assert f.get_sample_size(baseline_rate=baseline_rate) == out_sample_size


def test_get_ab_test_ci(in_ab_test_ci, out_ab_test_ci):
    lower_bound, upper_bound = f.get_ab_test_ci(
        conversions_control=in_ab_test_ci["control_conv"],
        conversions_treatment=in_ab_test_ci["treatment_conv"],
        total_users_control=in_ab_test_ci["control_size"],
        total_users_treatment=in_ab_test_ci["treatment_size"],
    )
    lower_bound, upper_bound = round(number=lower_bound, ndigits=4), round(
        number=upper_bound, ndigits=2
    )

    assert lower_bound, upper_bound == out_ab_test_ci
