import nettolohnrechner
import nettolohnoptimierer


if __name__ == '__main__':
    # init object with user input
    obj = nettolohnrechner.UserData()
    obj.user_input()

    # calculate data per hour for dataframe
    df = nettolohnoptimierer.calculate_data_per_hour(obj)
    df = nettolohnoptimierer.write_data_to_dataframe(df)
    df.to_csv(f'{obj.RE4}_my_salary_calc.csv', index=None)
