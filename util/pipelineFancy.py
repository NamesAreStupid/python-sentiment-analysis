from functools import reduce


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


def makePipelineFancy(*args):
    def pipeline(values):
        for g in args:
            values = g(values)
        return values
    return pipeline


def makeIterativePipeline(*args):
    def pipeline(values):
        gx = (args[0](val) for val in values)
        for f in args[1:]:
            gx = (f(gx) for val in values)
        return gx
    return pipeline


def makeIterativePipelineFancy(*args):
    def pipeline(values):
        for f in args:
            values = map(f, values)
        return values
    return pipeline


def makeIterativePipelineVerbose(*args):
    def pipeline(values):
        def valueGenerator(func):
            for val in values:
                yield func(val)
        gx = valueGenerator(args[0])
        for f in args[1:]:
            gx = valueGenerator(f(gx))
        return gx
    return pipeline


def makeFunctionalPipeline(*args):
    def pipeline(values):
        return map(lambda x: reduce(lambda y, z: z(y), args, x), values)
    return pipeline


def makeFunctionalPipelineNoLambda(*args):
    def pipeline(values):
        def reduction(x):
            return reduce(lambda y, z: z(y), args, x)
        return map(reduction, values)
    return pipeline
