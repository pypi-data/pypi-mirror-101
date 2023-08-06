import pandas as pd


def _value_counts(df):
    """
    Generalizes pd.value_counts() to all columns

    df : DataFrame object
    """
    print('>> Value counts:\n')
    for c in df.columns:
        print(f'# {c}:\n{df[c].value_counts()}\n\n')


def _describe(df):
    """
    Generalizes pd.describe() to all columns

    df : DataFrame object
    """
    print('>> Describe columns:\n')
    for c in df.columns:
        print(f'# {c}:\n{df[c].describe()}\n\n')


def _isnull(df):
    """
    Generalizes pd.isnull() to all columns

    df : DataFrame object
    """
    print('>> Null registers:\n')
    for c in df.columns:
        cnt = df[pd.isnull(df[c])].shape[0]
        if cnt == 0:
            print(f'# {c}: 0 null rows')
        else:
            print(f'# {c}: {cnt} rows')


def total_amazing_inspection(df):
    """
    Runs an amazing inspection

    Parameters
    ----------
    df: DataFrame object

    Returns
    -------
    This
        Exactly what you wish for!
    """
    pass
