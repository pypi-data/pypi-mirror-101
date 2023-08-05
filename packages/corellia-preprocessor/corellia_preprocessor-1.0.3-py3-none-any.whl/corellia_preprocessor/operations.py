import logging
import numpy as np
import pandas as pd
from ruamel.yaml import YAML
from sklearn import preprocessing


def normalize(data, **kwargs):
    """
    Normalizes the data
    :param data: data
    :param independent: If columns should be scaled together or individually
    :return: normalized data
    """
    if kwargs.get('independent', False):
        data = preprocessing.normalize(data, axis=1)
    else:
        data = preprocessing.normalize(data, axis=0)

    return data


def onehot_encode(data, label_col, **kwargs):
    """
    One-hot encoding
    :param data: data
    :param columns: column to OHE
    :return: OHE data
    """
    columns = kwargs.get('columns', [])

    if columns:
        data = pd.get_dummies(data, columns=columns)
    else:
        data = pd.get_dummies(data, columns=[label_col])

    return data


def reshape(data, **kwargs):
    """
        Reshaping
        :param data: data
        :param shape: desired shape
        :return: reshaped data
    """

    return np.asarray(data).reshape([-1] + kwargs.get('shape'))
