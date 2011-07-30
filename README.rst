Deterministic Dingus
====================

This is a very simple wrapper around the Dingus library to simplify
checking that the result of the tested is the result of calling the
function with particular arguments.

Dingus Whitelist Test Case
==========================


.. automodule:: deterministic_dingus
    :members:

This test helper makes it easier to set up and tear down tests.  Let's start
with an example.

.. code-block:: python

    from deterministic_dingus import DingusWhitelistTestCase

    from my_module import my_func
    import my_module as mod

    class DescribeMyFunc(DingusWhitelistTestCase):
    
        module = mod
        mock_list = ['a_global_function']
        additional_mocks = ['value']

        def run(self):
            self.returned = my_func(self.value)

        def should_call_a_global_function_with_value(self):
            assert mod.a_global_function.calls('()', self.value)

        def should_return_global_value_result(self):
            assert self.returned == mod.a_global_function()

First let's examine the class attributes.
