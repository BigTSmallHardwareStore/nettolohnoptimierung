import nettolohnrechner
import time
import random
import pandas as pd


def calculate_perfect_working_hour(obj):
    min_hour = obj.min_hour
    max_hour = obj.max_hour
    df = pd.DataFrame(columns=['Wochenstunden', 'Nettolohn', 'Nettostundenlohn'])

    for i in range(min_hour, max_hour+1, 1):
        obj.RE4 = obj.RE4 / 40 * i
        nl = nettolohnrechner.NetSalary(obj)
        print(f'Nettolohn bei {i} Wochenstunden ist {nl.nettolohn}')

        nl_per_hour = nl.nettolohn / (i * 52)
        print(f'Nettostundenlohn: {nl_per_hour: .2f}')

        df.loc[len(df)] = [i, nl, nl_per_hour]

        # to get the original user input value of RE4 for the next loop
        obj.RE4 = obj.RE4 * 40 / i

        wait_time = random.randint(5, 20)
        if i == max_hour:
            break
        # TODO: remove print
        print(wait_time)
        time.sleep(wait_time)

    return df


def calculate_ratio(df):
    pass
