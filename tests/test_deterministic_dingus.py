import os

from dingus import Dingus

from deterministic_dingus import (
    DeterministicDingus,
    DingusWhitelistTestCase,
    _DingusWhitelistTestCaseMetaclass,
)
import deterministic_dingus as mod


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
## _DingusWhitelistTestCaseMetaclass
##
####

class DescribeDingusWhitelistTestCaseMetaclass(object):

    def should_be_metaclass(self):
        assert issubclass(_DingusWhitelistTestCaseMetaclass, type)


class WhenMakingNewDingusWhitelistTestCaseClass(object):

    def setup(self):

        class BaseClassA(DingusWhitelistTestCase):
            additional_mocks = Dingus.many(3)
            mock_list = Dingus.many(3)

        class BaseClassB(DingusWhitelistTestCase):
            additional_mocks = Dingus.many(3)
            mock_list = Dingus.many(3)

        self.subclass_mock_list = Dingus.many(3)
        self.subclass_additional_mocks = Dingus.many(3)
        class Subclass(BaseClassA, BaseClassB):
            additional_mocks = self.subclass_additional_mocks
            mock_list = self.subclass_mock_list

        self.BaseClassA = BaseClassA
        self.BaseClassB = BaseClassB
        self.Subclass = Subclass

    def should_aggregate_mock_list(self):
        assert self.Subclass.mock_list  == (
            set(self.subclass_mock_list)
            | self.BaseClassA.mock_list
            | self.BaseClassB.mock_list
        )

    def should_aggregate_additional_mocks(self):
        assert self.Subclass.additional_mocks == (
            set(self.subclass_additional_mocks)
            | self.BaseClassA.additional_mocks
            | self.BaseClassB.additional_mocks
        )


####
##
## DingusWhitelistTestCase
##
####

class DescribeDingusWhitelistTestCaseClass(object):

    def should_use_DingusWhitelistTestCaseMetaclass_as_metaclass(self):
        assert DingusWhitelistTestCase.__metaclass__ \
            == _DingusWhitelistTestCaseMetaclass


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


class WhenARunMethodIsDefined(DingusWhitelistTestCase):

    module = os
    additional_mocks = ['function']

    def run(self):
        self.function()

    def should_call_run(self):
        assert self.function.calls('()')
