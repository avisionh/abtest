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


def test_get_sample_size(baseline_rate, out_get_sample_size):
    assert f.get_sample_size(baseline_rate=baseline_rate) == out_get_sample_size
