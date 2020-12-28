import pandas as pd


def report_conversions(
    data: pd.DataFrame,
    group_col: str,
    group_filter: str,
    convert_col: str,
    page_col: str,
) -> (int, float):
    """
    Calculates the count and percentages of conversions. Reports on percentage of conversions for control/treatment.

    This function assumes the data being passed in has a control and treatment group, where each group only sees one
    version of a page.

    Parameters
    __________
    data : pd.DataFrame
        Dataframe of data to use for calculating counts and percentages of conversions.
    group_col : str
        String of the grouping column that identifies whether conversion belongs to 'control' or 'treatment'.
    group_filter : str
        String of the value to filter the grouping column on.
    convert_col: str
        String of the column that identifies whether the user has converted or not.
    page_col: str
        String of the column that identifies the page seen by the user.

    Returns
    _______
    (int, float)
        Integer of the counts of conversions and decimal representation of the percentages of conversions.

    Examples
    ________
    >>> df = pd.DataFrame(data={'user_id': [1, 2, 3, 4, 5],
    ...                         'group': ['control', 'control', 'treatment', 'control', 'treatment'],
    ...                         'landing_page': ['old_page', 'old_page', 'new_page', 'old_page', 'new_page'],
    ...                         'converted': [0, 1, 0, 0, 1]})
    >>> df
       user_id      group landing_page  converted
    0        1    control     old_page          0
    1        2    control     old_page          1
    2        3  treatment     new_page          0
    3        4    control     old_page          0
    4        5  treatment     new_page          1
    >>> report_conversions(data=df,
    ...                    group_col='group',
    ...                    group_filter='control',
    ...                    convert_col='converted',
    ...                    page_col='landing_page')
    """
    try:
        df_filter = data[data[group_col] == group_filter]
        page_seen = df_filter[page_col].unique()

        # expect only one page seen by control/treatment group
        if len(page_seen) != 1:
            print(
                f"Have non-singular pages seen by the {group_filter} group.",
                f"Please process data so you have single pages seen by the {group_filter} group.",
            )
        else:
            conversions = df_filter[convert_col].sum()
            total_users = df_filter[convert_col].count()

            percent_page = (total_users / data[group_col].count()) * 100
            percent_page = round(number=percent_page, ndigits=2)

            print(
                f"Percentage of {group_filter} users who saw {page_seen}: {percent_page}%"
            )
            return conversions, conversions / total_users

    except Exception:
        raise
