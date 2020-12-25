#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np


def generate(p_center=None,
             p_edge=None,
             x_pair=np.array(
                 [[100, 0], [200, 0], [300, 0], [400, 0], [800, 0], [1600, 0], [200, 100], [300, 100], [300, 200],
                  [400, 200], [400, 300]]),
             condition='expand'
             ):
    """
    Generate exp data.
    Returns the DataFrame contains the stimulus

    Parameters
    ----------
    p_center : list
        1-D list of series probabilities in center group.
    p_edge : list
        1-D list of series probabilities in edge group.
    x_pair : array
        values for probabilities, (x1, x2)
    condition : str
        exp condition: expand, shrink, large, small

    Returns
    -------
    df : DataFrame
    """
    if p_edge is None:
        p_edge = [0.25, 0.75, 0.15, 0.85, 0.05, 0.95, 0.01, 0.99]
    if p_center is None:
        p_center = [0.45, 0.55, 0.4, 0.6, 0.35, 0.65, 0.25, 0.75]
    df_center = pd.DataFrame()
    df_edge = pd.DataFrame()
    df_center['p'] = np.repeat(p_center, len(x_pair))
    df_center['x1'] = np.tile(x_pair[:, 0], len(p_center))
    df_center['x2'] = np.tile(x_pair[:, 1], len(p_center))
    df_edge['p'] = np.repeat(p_edge, len(x_pair))
    df_edge['x1'] = np.tile(x_pair[:, 0], len(p_edge))
    df_edge['x2'] = np.tile(x_pair[:, 1], len(p_edge))
    df_large = pd.concat([df_edge.loc[df_edge.p > 0.5].copy(), df_center.loc[df_center.p > 0.5].copy()])
    df_small = pd.concat([df_edge.loc[df_edge.p < 0.5].copy(), df_center.loc[df_center.p < 0.5].copy()])
    while True:
        df_center = df_center.sample(frac=1)
        df_edge = df_edge.sample(frac=1)
        df_large = df_large.sample(frac=1)
        df_small = df_small.sample(frac=1)
        if condition == 'expand':
            df_center['order'] = 0
            df_edge['order'] = 1
            df = pd.concat([df_center, df_edge])
        elif condition == 'shrink':
            df_center['order'] = 1
            df_edge['order'] = 0
            df = pd.concat([df_edge, df_center])
        elif condition == 'large':
            df_small['order'] = 1
            df_large['order'] = 0
            df = pd.concat([df_large, df_small])
        elif condition == 'small':
            df_small['order'] = 0
            df_large['order'] = 1
            df = pd.concat([df_small, df_large])
        else:
            raise ValueError("condition must be expand, shrink or large, small")
        df.index = range(len(df))
        df['block'] = df.index // 44 + 1
        if df.groupby('block').p.mean().max() - df.groupby('block').p.mean().min() < 0.1:
            break
        elif condition in ['large', 'small']:
            break
    df['large'] = df.p > 0.5
    df['id'] = range(len(df))
    df['type'] = condition
    return df


def generate_train(p=None,
             x_pair=None,
             condition='expand'
             ):
    """
    Generate exp data for training.
    Returns the DataFrame contains the stimulus

    Parameters
    ----------
    p : list
        1-D list of series probabilities in training.
    x_pair : array
        values for probabilities, (x1, x2)
    condition : str
        exp condition: expand, shrink, large, small

    Returns
    -------
    df : DataFrame
    """
    if p is None:
        p = [0.25, 0.5, 0.75]
    if x_pair is None:
        x_pair = np.array([[800, 0], [300, 200]])
    df = pd.DataFrame()
    if condition == 'expand':
        df['p'] = np.repeat([0.4, 0.6], len(x_pair))
        df['x1'] = np.tile(x_pair[:, 0], 2)
        df['x2'] = np.tile(x_pair[:, 1], 2)
    elif condition == 'shrink':
        df['p'] = np.repeat([0.05, 0.95], len(x_pair))
        df['x1'] = np.tile(x_pair[:, 0], 2)
        df['x2'] = np.tile(x_pair[:, 1], 2)
    elif condition == 'large':
        df['p'] = np.repeat([0.5, 0.75], len(x_pair))
        df['x1'] = np.tile(x_pair[:, 0], 2)
        df['x2'] = np.tile(x_pair[:, 1], 2)
    elif condition == 'small':
        df['p'] = np.repeat([0.5, 0.25], len(x_pair))
        df['x1'] = np.tile(x_pair[:, 0], 2)
        df['x2'] = np.tile(x_pair[:, 1], 2)
    else:
        raise ValueError("condition must be expand, shrink or large, small")
    df = df.sample(frac=1)
    df.index = range(len(df))
    df['type'] = condition
    return df


if __name__ == '__main__':
    df = generate()
    df.to_csv('trial.csv')