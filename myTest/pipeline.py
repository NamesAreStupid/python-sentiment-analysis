def pipeline(numbers, *args):
    x = args[0](numbers)
    for g in args[1:]:
        print(g.__name__)
        x = g(x)
    return x


def chain(*args):
    def closure(values):
        x = args[0](values)
        for g in args[1:]:
            x = g(x)
        return x
    return closure


def addOne(values):
    for i in values:
        print('add 1 to ', i)
        yield i + 1


def square(values):
    for i in values:
        print('square ', i)
        yield i ** 2


def substractOne(values):
    for i in values:
        print('substract 1 ', i)
        yield i - 1


def printer(values):
    for i in values:
        print('print ', i)


numbers = [1, 2, 3, 4, 5]
# pipeline(numbers, addOne, square, substractOne, printer)

mixins = [addOne, square, substractOne, printer]
# pipeline(numbers, *mixins)

mixins2 = [addOne, square, substractOne]
# piped = list(pipeline(numbers, *mixins2))
# print(piped)

x = chain(mixins)
x(numbers)
