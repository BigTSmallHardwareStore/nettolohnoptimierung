import nettolohnrechner
import time
import random
import pandas as pd


def calculate_data_per_hour(obj):
    min_hour = obj.min_hour
    max_hour = obj.max_hour
    df = pd.DataFrame(columns=['Wochenstunden', 'Nettolohn', 'Nettostundenlohn'])

    for i in range(min_hour, max_hour+1, 1):
        obj.RE4 = obj.RE4 / 40 * i
        nl = nettolohnrechner.NetSalary(obj)
        print(f'Nettolohn bei {i} Wochenstunden ist {nl.nettolohn}')

        nl_per_hour = nl.nettolohn / (i * 52)
        print(f'Nettostundenlohn: {nl_per_hour: .2f}')

        df.loc[len(df)] = [i, nl.nettolohn, nl_per_hour]

        # to get the original user input value of RE4 for the next loop
        obj.RE4 = obj.RE4 * 40 / i

        wait_time = random.randint(5, 20)
        if i == max_hour:
            break
        # TODO: remove print
        print(wait_time)
        time.sleep(wait_time)

    return df


def calculate_marginal_salary(wochenstunden, wochenstunden_2, nettolohn, nettolohn_2):
    marginal_salary = (nettolohn - nettolohn_2) / (wochenstunden - wochenstunden_2)
    marginal_salary = marginal_salary / 52
    return marginal_salary


def calculate_salary_ratio(Nettolohn, Nettolohn_max, Wochenstunden, Wochenstunden_max):
    salary_ratio = (Nettolohn / Nettolohn_max) / (Wochenstunden / Wochenstunden_max)
    return salary_ratio


def write_data_to_dataframe(dataframe):
    df = dataframe

    # add columns to df for calculation
    df['Nettolohn_2'] = df['Nettolohn'].shift(1)
    df.loc[:, 'Nettolohn_2'].fillna(0, inplace=True)
    df['Wochenstunden_2'] = df['Wochenstunden'].shift(1)
    df.loc[:, 'Wochenstunden_2'].fillna(0, inplace=True)
    df.loc[:, 'Wochenstunden_max'] = df.loc[:, 'Wochenstunden'].max()
    df.loc[:, 'Nettolohn_max'] = df.loc[:, 'Nettolohn'].max()

    # apply functions to df
    df.loc[:, 'Grenzstundenlohn'] = df.apply(lambda x: calculate_marginal_salary(x['Wochenstunden'], x['Wochenstunden_2'], x['Nettolohn'], x['Nettolohn_2']), axis=1)
    df.loc[:, 'Verhältnis Reduzierung'] = df.apply(lambda x: calculate_salary_ratio(x['Nettolohn'], x['Nettolohn_max'], x['Wochenstunden'], x['Wochenstunden_max']), axis=1)

    # drop unneeded columns
    df.drop(columns=['Nettolohn_2', 'Wochenstunden_2', 'Nettolohn_max', 'Wochenstunden_max'], inplace=True)

    return df
