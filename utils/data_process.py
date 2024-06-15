# -*- coding: utf-8 -*-
"""
Title:   Data Preprocessing
Author:  Y. Dong
E-mail:  dyx_xjtu@163.com
Created: Jun 12, 2024

Description: 
"""

def get_stats(data, head):
    """Calculate the descriptive statistics of the data."""
    stats = data[head].describe()
    average_score, std_score, min_score, max_score = stats['mean'], stats['std'], stats['min'], stats['max']
    Q1, Q3, IQR = stats['25%'], stats['75%'], stats['75%'] - stats['25%']
    print(f'>> Average score: {average_score:.2f}, standard deviation: {std_score:.2f}; \n' + 
          f'>> minimum score: {min_score:.2f}, maximum score: {max_score:.2f};\n' +
          f'>> Q1: {Q1:.2f}, Q3: {Q3:.2f}, IQR: {IQR:.2f}.')
    return average_score, std_score, Q1, Q3, IQR

def cal_bound(average_score, std_score, Q1, Q3, IQR, mode='std'):
    """Calculate the lower bound and the upper bound of the data."""
    if mode == 'quantile':   
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
    elif mode == 'std':
        lower_bound = average_score - 3 * std_score
        upper_bound = average_score + 3 * std_score
    else:
        raise ValueError('The mode is not supported.')
    print(f'>> Lower bound: {lower_bound:.2f}, upper bound: {upper_bound:.2f}.')
    return lower_bound, upper_bound
