# ~/cerebunit/cerebunit/validation_tests/cells/Granule/test_for_spontFiring.py
#
# =============================================================================
# test_for_spontFiring.py
#
# created 7 March 2019
# modified
#
# Test for spontaneous firing from the neuron (soma).
# The model runs without any stimulus for 1 second, then spikes (if any) are
# considered. This firing rate is compared against those of experimental data.
#
# =============================================================================

import sciunit
import numpy
import quantities as pq
import scipy

from cerebunit.capabilities.measurements_ephys import ProducesEphysMeasurement
from cerebunit.statScore import TScore
from cerebunit.hypothesisTesting import HtestAboutMeans

# to execute the model you must be in ~/cerebmodels
from executive import ExecutiveControl

class SpontaneousFiringTest(sciunit.Test):
    """
    This test compares the measured unstimulated firing frequency observed in real animal (in-vitro or in-vivo, depending on the data) generated from neuron against those by the model.
    """
    required_capabilities = (ProducesEphysMeasurement,)
    score_type = TScore
    ec = ExecutiveControl()

    def generate_prediction(self, model, confidence=0.95, verbose=False):
        """
        Generates resting Vm from soma.
        The function is automatically called by sciunit.Test which this test is a child of.
        Therefore as part of sciunit generate_prediction is mandatory.
        """
        self.confidence = confidence # set confidence for test 90%, 95% (default), 99%
        #
        runtimeparam = {"dt": 0.025, "celsius": 30, "tstop": 1000.0, "v_init": -80.}
        stimparam = {"type": ["current", "IClamp"],                                                  
                     "stimlist": [ {"amp": 0.006, "dur": 800.0, "delay": 100.0} ],                 
                     "tstop": runtimeparam["tstop"] }
        ec.launch_model( parameters = runtimeparam, stimparameters = stimparam,
                         stimloc = model.cell.soma, onmodel = model,
                         capabilities = {"model": "produce_restingVm",
                                         "vtest": ProducesEphysMeasurement} )
        return pq.Quantity( numpy.mean(model.restingVm) # prediction
                            units = observation["units"] )

    def validate_observation(self, observation, first_try=True):
        """
        This function is called automatically by sciunit and
        clones it into self.observation
        This checks if the experimental_data is of some desired
        form or magnitude.
        Not exactly this function but a version of this is already
        performed by the ValidationTestLibrary.get_validation_test
        """
        if ("mean" not in observation or
            "margin_of_error" not in observation or
            "sample_size" not in observation or
            "units" not in observation):
            raise sciunit.ObservationError
        self.observation["mean"] = pq.Quantity( self.observation["mean"],
                                                units=observation["units"] )
        self.observation["margin_of_error"] = pq.Quantity( self.observation["margin_of_error"],
                                                          units=observation["units"] )
        self.observation["standard_error"] = self.observation["margin_of_error"] / \
                               self.get_tmultiplier(self.confidence, observation["sample_size"])

    @staticmethod
    def get_tmultiplier(confidence, n):
        return scipy.stats.t.ppf( (1+confidence)/2, n-1 )

    def compute_score(self, observation, prediction, verbose=False):
        """
        This function like generate_pediction is called automatically by sciunit
        which RestingVmTest is a child of. This function must be named compute_score
        The prediction processed from "vm_soma" is compared against
        the experimental_data to get the binary score; 0 if the
        prediction correspond with experiment, else 1.
        """
        score = TScore.compute( observation, prediction  )
        score.description = HtestAboutMeans( observation, prediction, score )
        print score.hypotest
        return score

