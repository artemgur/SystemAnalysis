def range_closed(start, stop, step):
    return range(start, stop - 1, step)

def slice_closed(x, start, end):
    return x[start:end + 1]

def readlines(file):
    return map(lambda x: x.rstrip(), file.readlines())