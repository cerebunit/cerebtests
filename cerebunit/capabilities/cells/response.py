# =========================================================================
# ~/cerebtests/cerebunit/capabilities/cells/response.py
#
# created  18 April 2019 Lungsi
# modified 
#
# This py-file contains general capabilities for cerebellar cells.
#
# note: Each capability is its own class. The way SciUnit works is that the
#       method of the model must have the same name as the name of the
#       method in the capability class. Thus both the model class and the
#       capability class must have the same method name.
#
# =========================================================================
"""
Capabilities w.r.t response from a cerebellar cell in general
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+-----------------------------------------+-----------------------------------------+
|        Class name (capability)          |        method name (capacity)           |
+=========================================+=========================================+
|:py:class:`.ProducesElectricalResponse`  |- :py:meth:`.produce_voltage_response`   |
+-----------------------------------------+-----------------------------------------+

"""


import sciunit


# ======================Produce Electrical Capability=====================
class ProducesElectricalResponse(sciunit.Capability):
    '''
    capability to produce electrical response.
    '''
    def __init__(self):
        pass
    def produce_voltage_response(self):
        '''
        capacity (getting voltage response) to fulfill the capability.
        '''
        raise NotImplementedError("Must implement produce_voltage_response")
# ========================================================================


# ========================Name of the Capability==========================
#
# ========================================================================
