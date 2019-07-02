# ~/cerebunit/cerebunit/validation_tests/cells/Granule/test_for_restingVm.py
#
# =============================================================================
# test_for_restingVm.py 
#
# created 5 March 2019
# modified
#
# Test for comparing resting Vm of the neuron against those from experiments.
# The model runs initially without any stimulus for an interval, then
# it run with current-clamp 6pA for an interval, and finally without stimulus.
# The model runs continuously over the three epochs with respective intervals.
# Each interval is associated with a resting Vm.
# The computed resting Vm of the model for the validation is based on the
# average of the resting Vm over the three intervals.
#
# =============================================================================

import sciunit
import numpy
import quantities as pq
from scipy.stats import t as student_t

from cerebunit.capabilities.cells.measurements import ProducesEphysMeasurement
from cerebunit.statistics.statScores import TScore
from cerebunit.statistics.hypothesisTesting import HtestAboutMeans

# to execute the model you must be in ~/cerebmodels
from executive import ExecutiveControl

class SciunitOrder(sciunit.Test):
    """
    This test compares the measured resting Vm observed in real animal (in-vitro or in-vivo, depending on the data) generated from neuron against those by the model.
    """
    required_capabilities = (ProducesEphysMeasurement,)
    score_type = TScore

    def validate_observation(self, observation, first_try=True):
        """
        This function is called automatically by sciunit and
        clones it into self.observation
        This checks if the experimental_data is of some desired
        form or magnitude.
        Not exactly this function but a version of this is already
        performed by the ValidationTestLibrary.get_validation_test
        """
        print("validate_observation")

    def generate_prediction(self, model, verbose=False):
        """
        Generates resting Vm from soma.
        The function is automatically called by sciunit.Test which this test is a child of.
        Therefore as part of sciunit generate_prediction is mandatory.
        """
        #self.confidence = confidence # set confidence for test 90%, 95% (default), 99%
        #
        self.observation["created_later"] = "generate_prediction"
        #print(self.observation)
        print(self.observation["created_later"])
        return 666.

    def _get_tmultiplier(self, confidence, n):
        return student_t.ppf( (1+confidence)/2, n-1 )

    def compute_score(self, observation, prediction, verbose=False):
        """
        This function like generate_pediction is called automatically by sciunit
        which RestingVmTest is a child of. This function must be named compute_score
        The prediction processed from "vm_soma" is compared against
        the experimental_data to get the binary score; 0 if the
        prediction correspond with experiment, else 1.
        """
        #print(observation)
        score = TScore.compute( self.observation, prediction  )
        print("compute_score")

