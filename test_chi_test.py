# -*- coding: utf-8 -*-
"""
Title:   Veerification of the validity of the candidate capability
Author:  Y. Dong
E-mail:  dyx_xjtu@163.com
Created: Jun 12, 2024

Description: 
"""

import argparse
import pandas as pd

from utils.chi_square_test import chi_square_test
from utils.data_process import get_stats, cal_bound


def main(file_path, head, save_path):
    # load the data from csv file
    data = pd.read_csv(file_path)
    total_num = data.shape[0]
    # get the descriptive statistics of the data
    average_score, std_score, Q1, Q3, IQR = get_stats(data, head)
    # remove the outliers ('std' or 'quantile')
    lower_bound, upper_bound = cal_bound(average_score, std_score, Q1, Q3, IQR, mode='std')
    upper_outlier, lower_outlier = data[data[head] > upper_bound], data[data[head] < lower_bound]
    data = data[(data[head] >= lower_bound) & (data[head] <= upper_bound)]
    print(f'> # Upper outliers: {upper_outlier.shape[0]}, ' +
          f'# lower outliers: {lower_outlier.shape[0]}. ' +
          f'(#samples: {total_num} -> {data.shape[0]}.)')
    # divide the range between the lower bound and the upper bound into 5 intervals
    gap_ratio = [0.2] * 5 # [1/12, 1/4, 1/3, 1/4, 1/12]
    interval = [lower_bound + (upper_bound - lower_bound) * sum(gap_ratio[:i]) for i in range(6)]
    data['Interval'] = pd.cut(data[head], bins=[interval[i] for i in range(6)], 
                              right=True, include_lowest=True)
    # check whether the total number of samples is equal to the sum of the number of samples in each interval
    if data.shape[0] != data['Interval'].value_counts().sum():
        raise ValueError('The number of samples is not equal to the sum of the number of samples in each interval.')
    # get the number of samples in each interval as a dictionary
    interval_count = data['Interval'].value_counts().to_dict()
    interval_count = dict(sorted(interval_count.items(), key=lambda x: x))
    interval_count = {f'level {i+1}': v for i, v in enumerate(interval_count.values())}
    interval_count['level 5'] += upper_outlier.shape[0]
    interval_count['level 1'] += lower_outlier.shape[0]
    # the expected frequency of each interval
    predinfed_ratio = [0.05, 0.15, 0.6, 0.15, 0.05]
    expected_frequency = {f'level {i+1}': total_num * predinfed_ratio[i] for i in range(5)}
    # print the number of samples in each interval
    interval_range_dict = {f'level {i+1}': f'[{interval[i]:.2f}, {interval[i+1]:.2f})' for i in range(5)}
    for level, interval in interval_range_dict.items():
        count = interval_count[level]
        expected_count = int(expected_frequency[level])
        print(f'>> {level}: {interval}, Number of samples: {count}\t(Expected: {expected_count}).')
    # check whether the total number of samples is equal to the sum of the number of samples in each interval
    if sum(interval_count.values()) != total_num:
        raise ValueError('The number of samples is not equal to the sum of the number of samples in each interval.')
    # the expected frequency of each interval
    predinfed_ratio = [0.05, 0.15, 0.6, 0.15, 0.05]
    expected_frequency = {f'level {i+1}': total_num * predinfed_ratio[i] for i in range(5)}
    # perform the chi-square test between the interval_count and the expected_frequency
    print('> Perform the chi-square test...')
    result, val = chi_square_test(interval_count, expected_frequency, alpha=0.05)
    # save the result to the csv file
    file_idx = int(file_path[-5])
    test_idx = int(head[-1])
    df = pd.read_csv(save_path)
    df.iloc[test_idx, file_idx] = 'Pass:'+val if result else 'Fail:'+val
    df.to_csv(save_path, index=False)

if __name__ == '__main__': 
    parser = argparse.ArgumentParser(description='Verify the validity of the candidate capability.')
    parser.add_argument('--file_path', type=str, default='data/paper_data.csv', help='The path of the data file.')
    parser.add_argument('--head', type=str, default='paper3', help='The head name of the data.')
    parser.add_argument('--save_path', type=str, default='res/paper_data.csv', help='The path of the data file.')
    args = parser.parse_args()
    main(args.file_path, args.head, args.save_path)
    