class Sentinel(object):
    def __init__(self):
        self._errs = set()

    def clear(self):
        self._errs = set()

    def error(self, name, msg):
        if isinstance(name, tuple) or isinstance(name, list):
            name = '.'.join(name)
        self._errs.add((name, msg))

    @property
    def ok(self):
        return len(self._errs) == 0

    @property
    def errors(self):
        return self._errs

    def __str__(self):
        output = ''
        for name, msg in self._errs:
            if output:
                output += '\n'
            output += 'ERROR ({}): {}'.format(name, msg)
        return output

    def __repr__(self):
        return repr(self._errs)
