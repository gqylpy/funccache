import gqylpy_cache


class Test(metaclass=gqylpy_cache):

    @staticmethod
    def test_cache():
        print('Run test_cache once.')

    @staticmethod
    def test_not_cache():
        print('Run test_not_cache once.')

    __not_cache__ = [test_not_cache]


t = Test()

t.test_cache()
t.test_cache()

t.test_not_cache()
t.test_not_cache()


@gqylpy_cache
def test():
    print('Run test once.')


test()
test()
