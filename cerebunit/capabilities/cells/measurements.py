# =============================================================================
# ~/cerebtests/cerebunit/capabilities/cells/measurements.py
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
Capabilities w.r.t measurements attainable from a cerebellar cell in general
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+-------------------------------------+--------------------------------------------------+
|      Class name (capabilities)      |        method name (capacities)                  |
+=====================================+==================================================+
|:py:class:`.ProducesEphysMeasurement`|- :py:meth:`.produce_soma_restingVm`              |
|                                     |- :py:meth:`.produce_soma_spikeheight`            |
|                                     |- :py:meth:`.produce_soma_spikeheight_antidromic` |
|                                     |- :py:meth:`.produce_soma_inputR`                 |
+-------------------------------------+--------------------------------------------------+

"""

import sciunit


# ========================Produce Ephys Measurement============================
class ProducesEphysMeasurement(sciunit.Capability):
    '''
    capability to produce electrophysiological measurments.
    '''
    def __init__(self):
        pass
    def produce_soma_restingVm(self):
        "capacity (of getting soma resting membrane voltage) to fulfill the capability."
        raise NotImplementedError("Must implement produce_soma_restingVm")

    def produce_soma_spikeheight(self):
        "capacity (of getting soma spike height) to fulfill the capability."
        raise NotImplementedError("Must implement produce_soma_spikeheight")

    def produce_soma_spikeheight_antidromic(self):
        "capacity (of getting soma spike height with antidromic stimulation) to fulfill the capability."
        raise NotImplementedError("Must implement produce_soma_spikeheight_antidromic")

    def produce_soma_inputR(self):
        "capacity (of getting soma input resistance) to fulfill the capability."
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
