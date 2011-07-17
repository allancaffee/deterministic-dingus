import os

from dingus import Dingus

from deterministic_dingus import DeterministicDingus, DingusWhitelistTestCase


####
##
## DeterministicDingus
##
####

class WhenComparingDingusResults(object):

    def setup(self):
        self.dingus = DeterministicDingus()

    def when_calling_with_identical_args_should_be_equal(self):
        assert self.dingus('an arg') == self.dingus('an arg')
        assert self.dingus() == self.dingus()
        assert self.dingus(foo='bar') == self.dingus(foo='bar')
        assert self.dingus({'foo': 'bar'}) == self.dingus({'foo': 'bar'})

    def when_calling_with_different_args_should_not_be_equal(self):
        assert self.dingus('an arg') != self.dingus('other arg')
        assert self.dingus('an arg') != self.dingus()
        assert self.dingus(foo='bar') != self.dingus(biz='bat')
        assert self.dingus(foo='bar') != self.dingus(foo='not bar')
        assert self.dingus(foo='bar') != self.dingus()
        assert self.dingus({'foo': 'bar'}) != self.dingus({'foo': 2})


class WhenGettingAttribute(object):

    def setup(self):
        self.dingus = DeterministicDingus()

    def should_return_deterministic_dingus(self):
        assert isinstance(self.dingus.my_func, DeterministicDingus)


####
##
## DingusWhitelistTestCase
##
####

class WhenMockingOs(DingusWhitelistTestCase):

    module = os
    mock_list = ['isatty']
    additional_mocks = ['foo']

    def setup(self):
        self.old_isatty = os.isatty
        self.old_kill = os.kill
        DingusWhitelistTestCase.setup(self)

    def teardown(self):
        DingusWhitelistTestCase.teardown(self)
        # Make sure it got put back
        assert os.isatty == self.old_isatty

    def should_dingus_isatty(self):
        assert isinstance(os.isatty, Dingus)

    def should_set_name_on_isatty(self):
        assert repr(os.isatty) == '<Dingus isatty>'

    def should_not_dingus_kill(self):
        assert os.kill == self.old_kill

    def should_set_up_additional_mocks(self):
        assert isinstance(self.foo, Dingus)

    def should_set_name_on_additional_mocks(self):
        assert repr(self.foo) == '<Dingus foo>'
