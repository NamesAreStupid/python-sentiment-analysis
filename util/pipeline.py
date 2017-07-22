def pipeline(values, *args):
    x = args[0](values)
    for g in args[1:]:
        print(g.__name__)
        x = g(x)
    return x


def makePipeline(*args):
    def pipeline(values):
        x = args[0](values)
        for g in args[1:]:
            x = g(x)
        return x
    return pipeline
