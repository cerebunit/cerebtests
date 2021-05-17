# ~/cerebtests/cerebtests/validation_tests/cells/Purkinje/test_for_soma_restVm.py
#
# =============================================================================
# test_for_soma_restVm.py 
#
# created 2 July 2019
# modified
#
# =============================================================================

import sciunit
import numpy
import quantities as pq

from cerebtests.capabilities.cells.measurements import ProducesEphysMeasurement
from cerebstats.data_conditions import NecessaryForHTMeans
from cerebstats.stat_scores import TScore # if NecessaryForHTMeans passes
from cerebstats.stat_scores import ZScoreStandard
from cerebstats.stat_scores import ZScoreForSignTest
from cerebstats.stat_scores import ZScoreForWilcoxSignedRankTest
from cerebstats.hypothesis_testings import HtestAboutMeans, HtestAboutMedians

# to execute the model you must be in ~/cerebmodels
from executive import ExecutiveControl
from sciunit.scores import NoneScore#, ErrorScore

class SomaRestingVmTest(sciunit.Test):
    """This test compares the measured resting Vm observed in real animal (in-vitro or in-vivo, depending on the data) generated from neuron against those by the model.

    The test class has three levels of mechanisms.

    **Level-1**  :py:meth:`.validate_observation`

    Given that the experimental/observed data has the following: *mean*, *SD* (or *SE*), *sample_size*, *units*, and *raw_data*, :py:meth:`.validate_observation` checks for them. The method then checks the data condition by asking ``NecessaryForHTMeans``. Depending on the data condition the appropriate ``score_type`` is assigned and corresponding necessary parameter; for t-Test, the parameter ``observation["standard_error"]`` and for sign-Test, the parameter ``observation["median"]``.

    **Level-2**  :py:meth:`.generate_prediction`

    The model is executed to get the model prediction. The prediction is a the resting Vm from the soma of a PurkinjeCell returned as a ``quantities.Quantity`` object.

    **Level-3**  :py:meth:`.compute_score`

    The prediction made by the model is then used as the *null value* for the compatible ``score_type`` based on the data condition (*normality* and *skewness*) determined by :py:meth:`.validate_observation`. The level ends by returning the compatible test-statistic (t or z-statistic) as a ``score``.

    **How to use:**

    ::

       from cerebtests.validation_tests.cells.Purkinje import SomaRestingVmTest
       data = json.load(open("/home/main-dev/cerebdata/expdata/cells/PurkinjeCell/Llinas_Sugimori_1980_soma_restVm.json"))
       test = SomaRestingVmTest( data )
       s = test.judge(chosenmodel, deep_error=True)


    Then to get the test score ``s.score`` and test report call ``print(s.description)``. If one is interested in getting the computed statistics call ``s.statistics``.

    **Further notes on the test.**

    * The experimental observation data (as *json* file) must have the element *protocol_parameters*, which in turn has the nests the elements *temperature* and *initial_resting_Vm*.
    * One should consider whether the model is compared against *in vitro* or *in vivo* experimental data (in addition to the species under study). For example,

       - Consider the Llinas and Sugimori (1980, 10.1113/jphysiol.1980.sp013357) experimental data (*Llinas_Sugimori_1980_soma_restVm.json*)
       - The reported experimental data only includes those with initial resting levels for :math:`\\geq -50 mV` discarding those for :math:`< -50 mV`.
       - The observed resting potential are claimed by the authors to be more negative than those observed in vivo.
       - The authors infer that this could be due to in vitro which is done on slices. The slicing removes background synaptic input generated by parallel fibre synapses.
       - For more details see Llinas_Sugimori_1980_soma_restVm.json

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
             ("SD" not in observation and "SE" not in observation)or
             "sample_size" not in observation or
             "units" not in observation or
             "raw_data" not in observation or
             "protocol_parameters" not in observation or # these last two are required for
             "temperature" not in observation["protocol_parameters"] or # for running the
             "initial_resting_Vm" not in observation["protocol_parameters"] ): # test correctly
            #raise sciunit.ObservationError("error")
            raise ValueError(
                    "Observation must be of the form "+ 
                    "{'mean': float, 'SD' or 'SE': float, 'sample_size': float, "+
                     "'units': string, 'raw_data': list, "+
                     "'protocol_parameters': {'temperature': float, "+
                                             "'initial_resting_Vm': float} }" )
        self.observation = observation
        self.observation["mean"] = pq.Quantity( observation["mean"],
                                                units=observation["units"] )
        if "SD" in self.observation:
            self.observation["standard_deviation"] = pq.Quantity( observation["SD"],
                                                                  units=observation["units"] )
            self.test_statistic_name = "z"
        elif "SE" in self.observation:
            self.observation["standard_error"] = pq.Quantity( observation["SE"],
                                                              units=observation["units"] )
            self.test_statistic_name = "t"
        self.observation["raw_data"] = pq.Quantity( observation["raw_data"],
                                                    units=observation["units"] )
        self.normaldata = NecessaryForHTMeans.ask("normal?", self.observation["raw_data"])
        if self.normaldata == True:
            print("dataset is normal") 
            if self.test_statistic_name == "t":
                self.score_type = TScore
            elif self.test_statistic_name == "z":
                self.score_type = ZScoreStandard
        else:
            print("dataset is Not normal")
            if NecessaryForHTMeans.ask("skew?", self.observation["raw_data"]) == True:
                print("dataset is skewed")
                ZScore = ZScoreForSignTest
            else:
                print("dataset is Not skewed")
                ZScore = ZScoreForWilcoxSignedRankTest
            self.score_type = ZScore
            #self.observation["median"] = numpy.median(self.observation["raw_data"])
        # parameters for properly running the test
        self.observation["celsius"] = observation["protocol_parameters"]["temperature"]
        self.observation["v_init"] = observation["protocol_parameters"]["initial_resting_Vm"]
        #
        print("Validated.")

    def generate_prediction(self, model, verbose=False):
        """
        Generates resting Vm from soma.
        The function is automatically called by sciunit.Test which this test is a child of.
        Therefore as part of sciunit generate_prediction is mandatory.
        """
        #self.confidence = confidence # set confidence for test 90%, 95% (default), 99%
        #
        print("Testing ...")
        runtimeparam = {"dt": 0.025, "celsius": self.observation["celsius"],
                        "tstop": 500.0, "v_init": self.observation["v_init"]}
        stimparam = {"type": ["current", "IClamp"],                                                                    "stimlist": [ {"amp": 0.00, "dur": 300.0, "delay": 200.0} ],                                      "tstop": runtimeparam["tstop"] }
        ec = ExecutiveControl()
        #ec.chosenmodel = model
        #ec.chosenmodel.restingVm = \
        model = ec.launch_model( parameters = runtimeparam, stimparameters = stimparam,
                                 stimloc = model.cell.soma, onmodel = model,
                                 capabilities = {"model": "produce_soma_restingVm",
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
        x = self.score_type.compute( observation, prediction  )
        if self.normaldata==True:
            #x = self.score_type.compute( observation, prediction  )
            hypoT = HtestAboutMeans( self.observation, prediction,
                                     {self.test_statistic_name: x}, side="not_equal" )
            test_statistic = x
            #score = self.score_type(x)
        else:
            #x = self.score_type.compute( observation, prediction )
            x.update( {"side": "not_equal"} )
            hypoT = HtestAboutMedians( self.observation, prediction, test=x )
            #score = self.score_type(x["z_statistic"])
            test_statistic = x["z_statistic"]
        score = self.score_type( test_statistic )
        score.description = hypoT.outcome
        score.statistics = hypoT.statistics
        print("Done.")
        print(score.description)
        return score
