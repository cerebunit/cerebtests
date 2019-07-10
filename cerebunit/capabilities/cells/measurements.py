# =============================================================================
# ~/cerebunit/cerebunit/capabilities/cells/measurements.py
#
# created  04 March 2019 Lungsi
# modified 
#
# This py-file contains general capabilities for cerebellar cells.
#
# note: Each capability is its own class. The way SciUnit works is that the
#       method of the model must have the same name as the name of the
#       method in the capability class. Thus both the model class and the
#       capability class must have the same method name.
#
# =============================================================================
"""
GENERAL CEREBELLAR CELL CAPABILITIES
====================================

+-------------------------------------+---------------------------------------+
|            Class name               |          method name                  |
+=====================================+=======================================+
|:py:meth:`.ProducesEphysMeasurement` |:py:meth:`.produce_soma_restingVm`     |
|                                     |:py:meth:`.produce_soma_spikeheight`   |
+-------------------------------------+---------------------------------------+

"""

import sciunit


# ========================Produce Ephys Measurement============================
class ProducesEphysMeasurement(sciunit.Capability):
    '''
    The model produces resting membrane voltage.
    '''
    def __init__(self):
        pass
    def produce_soma_restingVm(self):
        "The model produces resting membrane voltage from soma."
        raise NotImplementedError("Must implement produce_soma_restingVm")

    def produce_soma_spikeheight(self):
        "The model produces spike height measured from resting potential from soma."
        raise NotImplementedError("Must implement produce_soma_spikeheight")

    def produce_soma_inputR(self):
        "The model produces input resistance from soma."
        raise NotImplementedError("Must implement produce_soma_inputR")
# ========================================================================


# ======================Produce Electrical Capability=====================
#class ProducesElectricalResponse(sciunit.Capability):
#    '''
#    The model produces electrical responses.
#    '''
#    def __init__(self):
#        pass
#    def produce_voltage_response(self):
#        '''
#        get voltage response
#        '''
#        raise NotImplementedError("Must implement produce_voltage_response")
# ========================================================================


# ========================Name of the Capability==========================
#
# ========================================================================
