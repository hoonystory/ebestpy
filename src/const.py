# define constants
const = {
    'status': {
        'STAND_BY': 0
        , 'SUCCESS': 1
    }
}

STAND_BY = 0
LOGGED_ON = 1
SUCCESS = 1


# Decorator
def constant(func):
    def func_set(self, value):
        raise TypeError

    def func_get(self):
        return func()

    return property(func_get, func_set)


# const class
# noinspection PyMethodParameters
class Const(object):
    @constant
    def daytime_start_hour():
        return 15

    @constant
    def daytime_end_hour():
        return 4

    @constant
    def weekday_list():
        return list(range(0, 5))

    # 현재 시간을 가져와서, 어느 시간대(주간/야간) 데이터를 수집할 것인지를 판단함
    # dayOfWeek = funcs.todayOfWeek()

    # weekday_dayStrtHour = 15
    # weekday_dayEndHour = 4
    # weekday_dayList = list(range(0, 5))

    # weekday_nightStrtHour = list(range(5, 12))
    # weekday_nightList = list(range(1, 6))