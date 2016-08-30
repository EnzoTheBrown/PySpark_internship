def least_square(xs, ys):
    def sum(bunch):
        res = 0
        for b in bunch:
            res += b
        return res
    xys = []
    xxs = []
    yys = []
    for i in range(0, min(len(xs), len(ys))):
        xys.append(xs[i]*ys[i])
        xxs.append(xs[i]**2)
        yys.append(ys[i]**2)
    n = min(len(xs), len(ys))
    m = (n*sum(xys) - sum(xs)*sum(ys))/(n*sum(xxs)-sum(xxs))
    b = (sum(ys) - m*sum(xs)) / n
    return m, b

def mean(ys):
    mean = 0
    for y in ys:
        mean += y
    return mean/len(ys)

