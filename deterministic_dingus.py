from dingus import Dingus

class DeterministicDingus(Dingus):
    """This dingus returns a different Dingus depending on the arguments it's called with.

    It has the property of being purely deterministic (i.e. the same
    arguments always return the same object).  Unfortunately this
    means that the behaviour of returning an identical `Dingus` when
    called without arguments is lost.

    >>> d = DeterministicDingus()
    >>> d('an arg') == d('other arg')
    False
    >>> d('an arg') == d('an arg')
    True
    >>> d.func('an arg') == d.func('other arg')
    False
    >>> d.func('an arg') == d.func('an arg')
    True
    >>> d.func('an arg') == d.func()
    False
    """
    def __init__(self, *args, **kwargs):
        self.__argument_map = {}
        Dingus.__init__(self, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        key = (tuple(args), tuple(kwargs.items()),)
        if key in self.__argument_map:
            rv = self.__argument_map[key]
        else:
            self.__argument_map[key] = rv = self._create_child('()')
            self._children['()'] = rv

        self._log_call('()', args, kwargs, rv)
        return rv
