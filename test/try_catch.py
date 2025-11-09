import time


def test_func():
    try:
        raise Exception('test {}', id(test))
    except Exception as e:
        print(e)
        time.sleep(1)
        test_func()


test = test_func
test_func()