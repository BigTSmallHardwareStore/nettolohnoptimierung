import nettolohnrechner
import nettolohnoptimierer

if __name__ == '__main__':
    obj = nettolohnrechner.UserData()
    obj.user_input()
    df = nettolohnoptimierer.calculate_perfect_working_hour(obj)

