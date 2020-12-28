import pandas as pd

df = pd.read_csv(filepath_or_buffer="data/raw/ab_data.csv")

# expect control group to see old_page
# and treatment to see new_page only
df.drop_duplicates(subset=["group", "landing_page"], inplace=False)
# remove control group seeing new_page
# and treatment group seeing old_page
mask_control_old = (df["group"] == "control") & (df["landing_page"] == "old_page")
mask_treatment_new = (df["group"] == "treatment") & (df["landing_page"] == "new_page")
mask = mask_control_old | mask_treatment_new
df_clean = df.loc[mask].copy()

# check balanced classes
df_clean["group"].value_counts()

# check and drop duplicate users
df_clean["user_id"].count()
df_clean["user_id"].nunique()
df_clean["user_id"].value_counts(sort=True)
# see no difference in actual `group`, `landing_page` and `converted` values so can drop indiscriminately
df_clean[df_clean["user_id"] == 773192]
df_clean = df_clean.drop_duplicates(subset="user_id", keep="last", inplace=False)

df_clean.to_csv(path_or_buf="data/interim/df_conversion_clean.csv", index=False)
