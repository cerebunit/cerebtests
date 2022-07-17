# ~/cerebtests/cerebtests/validation_tests/cells/Granule/test_for_nonadaptingGrC.py
#
# =============================================================================
# test_for_nonadaptingGrC.py
#
# created 6 July 2022
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
# Test for determining Non-adapting Granule cell (i.e. Regular GrC).
# This is done by IClamp stimulation of 10 pA for 2 seconds and comparing the
# frequencies in the four 500 ms intervals.
# Note that the total duration of 2 seconds of stimulation is longer than commonly
# used because the experiment is based on wet tissue experiment where frequencies
# for shorter stimulation can be affected by mossy fibre discharges.
#
# =============================================================================

import os

import h5py
import sciunit
import numpy
import quantities as pq
from scipy.stats import t as student_t

from cerebtests.capabilities.cells.measurements import ProducesSpikeFrequency
from cerebstats.statScores import Chi2Score
from cerebstats.hypothesisTesting import HtestAboutMeans

# to execute the model you must be in ~/cerebmodels
from executive import ExecutiveControl
from sciunit.scores import NoneScore, ErrorScore


class NonAdaptingGrCTest(sciunit.Test):
    """
    This test compares the measured resting Vm observed in real animal (in-vitro or in-vivo, depending on the data) generated from neuron against those by the model.
    """
    required_capabilities = (ProducesSpikeFrequency,)
    score_type = Chi2Score

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
        if ("dataset" not in observation or
                os.path.splitext(observation["dataset"])[1] != ".h5" or
                "MembVolts" not in h5py.File(observation["dataset"], 'r').keys()):
            raise sciunit.ObservationError
        self.observation = observation
        self.observation["success_numbers"] = pq.Quantity(observation["mean"],
                                                          units=observation["units"])
        print("Validated.")

    def generate_prediction(self, model, verbose=False):
        """
        Generates resting Vm from soma.
        The function is automatically called by sciunit.Test which this test is a child of.
        Therefore as part of sciunit generate_prediction is mandatory.
        """
        # self.confidence = confidence # set confidence for test 90%, 95% (default), 99%
        #
        runtimeparam = {"dt": 0.025, "celsius": 32, "tstop": 5000, "v_init": -65}
        stimparam = {"type": ["current", "IClamp"],
                     "stimlist": [{"amp": 0.006, "dur": 800.0, "delay": 100.0}],
                     "tstop": runtimeparam["tstop"]}
        ec = ExecutiveControl()
        # ec.chosenmodel = model
        # ec.chosenmodel.restingVm = \
        model = ec.launch_model(parameters=runtimeparam, stimparameters=stimparam,
                                stimloc="soma", onmodel=model,
                                capabilities={"model": "produce_spike_instantaneous_frequency",
                                              "vtest": ProducesSpikeFrequency},
                                mode="capability")
        # return pq.Quantity( numpy.mean(ec.chosenmodel.prediction), # prediction
        #                    units = self.observation["units"] )
        return pq.Quantity(numpy.mean(model.prediction),  # prediction
                           units=self.observation["units"])

    def _get_tmultiplier(self, confidence, n):
        return student_t.ppf((1 + confidence) / 2, n - 1)

    def compute_score(self, observation, prediction, verbose=False):
        """
        This function like generate_pediction is called automatically by sciunit
        which RestingVmTest is a child of. This function must be named compute_score
        The prediction processed from "vm_soma" is compared against
        the experimental_data to get the binary score; 0 if the
        prediction correspond with experiment, else 1.
        """
        print("Computing score ...")
        # print(observation == self.observation) # True
        x = Chi2Score.compute(observation, prediction)
        hypo = HtestAboutMeans(self.observation, prediction, x)
        score = Chi2Score(x)
        score.description = hypo.outcome
        print("Done.")
        print(score.description)
        return score
