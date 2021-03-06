from collections import MutableMapping

from dingus import Dingus, DingusTestCase, exception_raiser, DontCare


__all__ = [
    'DeterministicDingus',
    'Dingus',
    'DingusTestCase',
    'DingusWhitelistTestCase',
    'DontCare',
    'exception_raiser',
]

class NonHashingMap(MutableMapping):
    """This is a :class:`dict`\ -like object that supports unhashable keys.

    This is a theoretically less performant mapping than a normal :class:`dict`
    but it can use keys containing values that cannot be hashed.  Since
    :class:`DeterministicDingus` shouldn't be storing very large mappings the
    fact that lookups are O(n) is irrelevant.
    """

    def __init__(self):
        self.__mapping = []

    def __setitem__(self, key, value):
        self.__mapping.append((key, value,))

    def __getitem__(self, key):
        for my_key, value in self.__mapping:
            if my_key == key:
                return value
        raise KeyError(key)

    def __contains__(self, key):
        for my_key, value in self.__mapping:
            if my_key == key:
                return True
        return False

    def __iter__(self):
        return [key for key, value in self.__mapping]

    def __delitem__(self):
        raise NotImplementedError

    def __len__(self):
        return len(self.__mapping)


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
        self.__argument_map = NonHashingMap()
        Dingus.__init__(self, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        key = (args, kwargs,)
        if key in self.__argument_map:
            rv = self.__argument_map[key]
        else:
            self.__argument_map[key] = rv = self._create_child('()')
            self._children['()'] = rv

        self._log_call('()', args, kwargs, rv)
        return rv


class _DingusWhitelistTestCaseMetaclass(type):
    """Aggregate relevant attributes.

    This metaclass aggregates attributes of base classes so that subclasses can
    specify just the values that are specific to their tests.
    """

    __aggretated_attrs = ('additional_mocks', 'module_mocks', 'mock_list')

    def __new__(cls, name, bases, attrs):
        for attr_name in cls.__aggretated_attrs:
            if attr_name in attrs:
                attrs[attr_name] = set(attrs[attr_name])
            else:
                attrs[attr_name] = set()

            for base in bases:
                if hasattr(base, attr_name):
                    attrs[attr_name].update(getattr(base, attr_name))

        attrs['module_mocks'].update(attrs['mock_list'])
        return type.__new__(cls, name, bases, attrs)


class DingusWhitelistTestCase(object):
    """A helpful base test case for unit testing.

    This class is similar in function to the original :class:`DingusTestCase`
    except that it operates on white list of what to mock rather than a black
    list.  What to actually mock should be set as a class attribute on
    inheriting classes as :data:`module_mocks`.
    """

    __metaclass__ = _DingusWhitelistTestCaseMetaclass
    module = None
    """The module to mock.

    This should be set in the concrete subclass.
    """

    mock_list = set()
    """Old name for `module_mocks`.

    This attribute works identically to `module_mocks` but is honored for
    backwords compatability.  Newly written tests should use `module_mocks`
    instead.
    """

    module_mocks = set()
    """A collection of names that should be mocked out in `module`.

    `module` will be reset to its original contents during :meth:`teardown`.
    """

    additional_mocks = set()
    """A collection of additional attributes to be set on the class during :meth:`setup`.
    """

    def setup(self):
        self.__old_module_dict = self.module.__dict__.copy()
        for key in self.module_mocks:
            self.module.__dict__[key] = Dingus(key)
        for key in self.additional_mocks:
            setattr(self, key, Dingus(key))

        if hasattr(self, 'run') and callable(self.run):
            self.run()

    def teardown(self):
        self.module.__dict__.clear()
        self.module.__dict__.update(self.__old_module_dict)
