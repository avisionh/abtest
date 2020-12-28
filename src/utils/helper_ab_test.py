from doctest import testmod
from typing import Union
import pandas as pd
import math
import statsmodels.stats.api as sms
import scipy.stats as st


def report_conversions(
    data: pd.DataFrame,
    group_col: str,
    group_filter: str,
    convert_col: str,
    page_col: str,
) -> (int, int, float):
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
    (int, int, float)
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
    Percentage of control users who saw ['old_page']: 60.0%
    (1, 3, 0.3333333333333333)
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
            return conversions, total_users, conversions / total_users

    except Exception:
        raise


def get_sample_size(
    baseline_rate: Union[int, float],
    practical_significance: float = 0.01,
    confidence_level: float = 0.05,
    sensitivity: float = 0.8,
) -> float:
    """
    Calculates the required sample size for hypothesis-testing.

    Reference:
        - https://github.com/RobbieGeoghegan/AB_Testing/blob/master/AB_Testing.ipynb

    Parameters
    __________
    baseline_rate : Union[int, float]
        Integer or float of an estimate of the metric being analyzed before making any changes.
    practical_significance : float
        Float of an estimate of the the minimum change to the baseline rate that is useful to the business. For example
        an increase in the conversion rate of 0.001% may not be worth the effort required to make the change whereas a
        2% change will be.
    confidence_level : float
        Float of the probability that the null hypothesis (experiment and control are the same) is rejected when it
        should not be. Also called significance level.
    sensitivity : float
        Float of the probability that the null hypothesis is not rejected when it should be.

    Returns
    _______
    sample_size : float
        Float of the sample size to use for the A/B test experiment.

    Examples
    ________
    >>> baseline_rate = 0.1204
    >>> get_sample_size(baseline_rate=baseline_rate)
    Required sample size: 17210 per group
    17210.118424055283
    """
    try:
        effect_size = sms.proportion_effectsize(
            prop1=baseline_rate, prop2=baseline_rate + practical_significance
        )
        sample_size = sms.NormalIndPower().solve_power(
            effect_size=effect_size, power=sensitivity, alpha=confidence_level, ratio=1
        )
        print(f"Required sample size: {round(sample_size)} per group")
        return sample_size
    except Exception:
        raise


def check_sample_sizes(
    total_users_control: int,
    total_users_treatment: int,
    baseline_rate: Union[int, float],
    **kwargs,
):
    """
    Checks whether the control and treatment sizes are large enough to conduct hypothesis-testing.

    Parameters
    __________
    total_users_control : int
       Number of people in the control group.
    total_users_treatment : int
        Number of people in the treatment group.
    baseline_rate : Union[int, float]
        Integer or float of an estimate of the metric being analyzed before making any changes.
    **kwargs
        These parameters will be passed to the get_sample_size() function.

    See Also
    ________
    get_sample_size : Calculates the required sample size for hypothesis-testing.
    """
    try:
        sample_size = get_sample_size(baseline_rate=baseline_rate, **kwargs)
        if total_users_control >= sample_size & total_users_treatment >= sample_size:
            print(
                "Control and treatment groups are sufficiently large to conduct hypothesis testing"
            )
        elif total_users_control >= sample_size & total_users_treatment < sample_size:
            print(
                "Treatment group not sufficiently large to conduct hypothesis testing."
            )
        elif total_users_control < sample_size & total_users_treatment >= sample_size:
            print("Control group not sufficiently large to conduct hypothesis testing.")
        else:
            print(
                "Control and treatment groups not sufficiently large to conduct hypothesis testing."
            )
    except Exception:
        raise


def get_ab_test_ci(
    conversions_control: int,
    conversions_treatment: int,
    total_users_control: int,
    total_users_treatment: int,
    confidence_level: float = 0.05,
) -> str:
    """
    Conducts an A/B test on the two sided hypothesis:
        - H_0: Probability of conversion in treatment group minus probability of conversion in control group is 0.
        - H_1: Probability of conversion in treatment group minus probability of conversion in control group is not 0.

    References:
        - https://henryfeng.medium.com/handy-functions-for-a-b-testing-in-python-f6fdff892a90

    Parameters
    __________
    conversions_control : int
        Number of people who converted in the control group.
    conversions_treatment : int
        Number of people who converted in the treatment group.
    total_users_control : int
        Number of people in the control group.
    total_users_treatment : int
        Number of people in the treatment group.
    confidence_level : float
        Float of the probability that the null hypothesis (experiment and control are the same) is rejected when it
        should not be. Also called significance level.

    Returns
    _______
    lower_bound, upper_bound : float, float
        Floats of the lower and upper-bounds of the C.I.
    """
    try:
        # compute conversion rates
        conversion_rate_control = conversions_control / total_users_control
        conversion_rate_treatment = conversions_treatment / total_users_treatment

        # compute statistics for constructing C.I.
        conversion_mean = conversion_rate_treatment - conversion_rate_control
        variance = (
            conversion_rate_treatment
            * (1 - conversion_rate_treatment)
            / total_users_treatment
            + conversion_rate_control
            * (1 - conversion_rate_control)
            / total_users_control
        )
        sd = math.sqrt(variance)
        z_score = abs(st.norm.ppf(q=(1 - confidence_level) / 2))

        # compute C.I.
        lower_bound = conversion_mean - z_score * sd
        upper_bound = conversion_mean + z_score * sd

        return lower_bound, upper_bound
    except Exception:
        raise


if __name__ == "__main__":
    testmod(verbose=True)
