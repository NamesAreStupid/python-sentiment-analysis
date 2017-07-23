from functools import reduce


def makePipeline(*args):
    def pipeline(values):
        return map(lambda x: reduce(lambda y, z: z(y), args, x), values)
    return pipeline
