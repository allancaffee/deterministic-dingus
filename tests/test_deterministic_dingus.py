from tests.helpers.deterministic_dingus import DeterministicDingus


class WhenComparingDingusResults(object):

    def setup(self):
        self.dingus = DeterministicDingus()

    def when_calling_with_identical_args_should_be_equal(self):
        assert self.dingus('an arg') == self.dingus('an arg')
        assert self.dingus() == self.dingus()
        assert self.dingus(foo='bar') == self.dingus(foo='bar')

    def when_calling_with_different_args_should_not_be_equal(self):
        assert self.dingus('an arg') != self.dingus('other arg')
        assert self.dingus('an arg') != self.dingus()
        assert self.dingus(foo='bar') != self.dingus(biz='bat')
        assert self.dingus(foo='bar') != self.dingus(foo='not bar')
        assert self.dingus(foo='bar') != self.dingus()


class WhenGettingAttribute(object):

    def setup(self):
        self.dingus = DeterministicDingus()

    def should_return_deterministic_dingus(self):
        assert isinstance(self.dingus.my_func, DeterministicDingus)
