import src.utils.helper_ab_test as f
import pandas as pd


df = pd.read_csv(filepath_or_buffer="data/interim/df_conversion_clean.csv")

conversions_control, total_users_control = f.report_conversions(
    data=df,
    group_col="group",
    group_filter="control",
    convert_col="converted",
    page_col="landing_page",
)

conversions_treatment, total_users_treatment = f.report_conversions(
    data=df,
    group_col="group",
    group_filter="treatment",
    convert_col="converted",
    page_col="landing_page",
)
