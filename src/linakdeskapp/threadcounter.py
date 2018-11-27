#
#
#


_threadCounter = dict()


def getThreadName(prefix=None):
    if prefix is None:
        prefix = "Thread"
    threadNum = getThreadNumber(prefix)
    return "%s-%d" % (prefix, threadNum)

def getThreadNumber(prefix=None):
    currNum = 0
    if prefix in _threadCounter:
        currNum = _threadCounter[prefix]
    else:
        currNum = 1
    _threadCounter[prefix] = currNum + 1
    return currNum
