# -*- coding: utf-8 -*-
"""
Title:   Veerification of the validity of the candidate capability
Author:  Y. Dong
E-mail:  dyx_xjtu@163.com
Created: Jun 12, 2024

Description: 
"""

from scipy.stats import chi2


def chi_square_test(observed_dict, expected_dict, alpha=0.05):
    """Perform the chi-square test for the data."""
    # calculate the degree of freedom and the chi-square statistic
    degree_of_freedom = len(observed_dict) - 1
    chi_square_statistic = sum([(observed_dict[k] - expected_dict[k])**2 / expected_dict[k] for k in observed_dict.keys()])
    critical_value = chi2.ppf(1 - alpha, degree_of_freedom)
    # determine whether the null hypothesis is rejected
    print(f'>> Null hypothesis: The observed frequency is equal to the expected frequency. <<')
    if chi_square_statistic > critical_value:
        print(f'>> The chi-square statistic is {chi_square_statistic:.2f}, which is greater than the critical value {critical_value:.2f}.')
        print('>> Sorry, we have to reject the null hypothesis.')
        return False, f'{chi_square_statistic:.2f}'
    else:
        print(f'>> The chi-square statistic is {chi_square_statistic:.2f}, which is less than the critical value {critical_value:.2f}.')
        print('>> Congratulations! we do not reject the null hypothesis.')
        return True, f'{chi_square_statistic:.2f}'
    