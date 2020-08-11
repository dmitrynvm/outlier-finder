import numpy, pandas
from scipy import stats


def load(fname):
    output = pandas.read_csv(fname, index_col=0, parse_dates=True)
    return output


def parse(input, columns):
    to_float = lambda val: float(val[1:].replace(',', ''))
    numeric = input[columns]
    output = numeric.copy()
    for column in output.columns:
        output[column] = numeric[column].apply(to_float)
    return output


def normlz(input):
    output = input.copy()
    for column in input.columns:
        max_value = input[column].max()
        min_value = input[column].min()
        output[column] = (input[column] - min_value) / (max_value - min_value)
    return output


def sieve(input):
    aggred = input.mean(axis=1)
    zscores = numpy.abs(stats.zscore(aggred))
    output = numpy.where(zscores > 3)[0]
    return output


def execute():
    columns = ['plan_premium', 'reinsurance', 'rx', 'rx_with_rebates', 'rx_without_rebates', 'spec_cap']
    loaded = load('data1.csv')
    parsed = parse(loaded, columns)
    normlzed = normlz(parsed)
    outliers = sieve(normlzed)
    loaded.iloc[outliers].to_csv('outliers.csv')


if __name__ == '__main__':
    execute()