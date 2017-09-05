from functools import reduce


def makePipeline(*args):
    def pipeline(values):
        return reduce(lambda x, y: y(x), args, values)
    return pipeline
