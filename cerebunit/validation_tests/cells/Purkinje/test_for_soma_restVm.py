# ~/cerebunit/cerebunit/validation_tests/cells/Granule/test_for_soma_restVm.py
#
# =============================================================================
# test_for_soma_restVm.py 
#
# created 2 July 2019
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

from cerebunit.capabilities.cells.measurements import ProducesEphysMeasurement
from cerebunit.statistics.data_conditions import NecessaryForHTMeans
from cerebunit.statistics.stat_scores import TScore # if NecessaryForHTMeans passes
from cerebunit.statistics.stat_scores import ZScoreForSignTest as ZScore
from cerebunit.statistics.hypothesis_testings import HtestAboutMeans, HtestAboutMedians

# to execute the model you must be in ~/cerebmodels
from executive import ExecutiveControl
from sciunit.scores import NoneScore#, ErrorScore

class SomaRestingVmTest(sciunit.Test):
    """
    This test compares the measured resting Vm observed in real animal (in-vitro or in-vivo, depending on the data) generated from neuron against those by the model.
    """
    required_capabilities = (ProducesEphysMeasurement,)
    score_type = NoneScore # Placeholder which will be set at validate_observation

    def validate_observation(self, observation, first_try=True):
        """
        This function is called automatically by sciunit and
        clones it into self.observation
        This checks if the experimental_data is of some desired
        form or magnitude.
        Not exactly this function but a version of this is already
        performed by the ValidationTestLibrary.get_validation_test
        """
        print("Validate Observation ...")
        if ( "mean" not in observation or
             "SD" not in observation or
             "sample_size" not in observation or
             "units" not in observation or
             "raw_data" not in observation ):
            raise sciunit.ObservationError
        self.observation = observation
        self.observation["mean"] = pq.Quantity( observation["mean"],
                                                units=observation["units"] )
        self.observation["SD"] = pq.Quantity( observation["SD"],
                                                           units=observation["units"] )
        self.observation["standard_error"] = \
                  pq.Quantity( observation["SD"] / numpy.sqrt(observation["sample_size"]),
                               units=observation["units"] )
        self.observation["raw_data"] = pq.Quantity( observation["raw_data"],
                                                    units=observation["units"] )
        self.datacond = NecessaryForHTMeans.ask( observation["sample_size"],
                                                 observation["raw_data"] )
        if self.datacond==True:
            self.score_type = TScore
        else:
            self.score_type = ZScore
            self.observation["median"] = numpy.median(self.observation["raw_data"])
        print("Validated.")

    def generate_prediction(self, model, verbose=False):
        """
        Generates resting Vm from soma.
        The function is automatically called by sciunit.Test which this test is a child of.
        Therefore as part of sciunit generate_prediction is mandatory.
        """
        #self.confidence = confidence # set confidence for test 90%, 95% (default), 99%
        #
        runtimeparam = {"dt": 0.025, "celsius": 30, "tstop": 1000.0, "v_init": -80.}
        stimparam = {"type": ["current", "IClamp"],                                                                    "stimlist": [ {"amp": 0.006, "dur": 800.0, "delay": 100.0} ],                                      "tstop": runtimeparam["tstop"] }
        ec = ExecutiveControl()
        #ec.chosenmodel = model
        #ec.chosenmodel.restingVm = \
        model = ec.launch_model( parameters = runtimeparam, stimparameters = stimparam,
                                 stimloc = model.cell.soma, onmodel = model,
                                 capabilities = {"model": "produce_restingVm",
                                                 "vtest": ProducesEphysMeasurement},
                                 mode = "capability" )
        return pq.Quantity( numpy.mean(model.prediction), # prediction
                            units = self.observation["units"] )

    def compute_score(self, observation, prediction, verbose=False):
        """
        This function like generate_pediction is called automatically by sciunit
        which RestingVmTest is a child of. This function must be named compute_score
        The prediction processed from "vm_soma" is compared against
        the experimental_data to get the binary score; 0 if the
        prediction correspond with experiment, else 1.
        """
        print("Computing score ...")
        #print(observation == self.observation) # True
        if self.datacond==True:
            x = TScore.compute( observation, prediction  )
            hypoT = HtestAboutMeans( self.observation, prediction, x )
            score = TScore(x)
            score.description = hypoT.outcome
            score.statistics = hypoT.statistics
        else:
            x = ZScore.compute( observation, prediction )
            hypoT = HtestAboutMedians( self.observation, prediction, x )
            score = ZScore(x)
            score.description = hypoT.outcome
            score.statistics = hypoT.statistics
        print("Done.")
        print(score.description)
        return score

