# ============================================================================
# ~/cerebunit/cerebunit/hypothesis_testings/signTest.py
#
# created 4 July 2019 Lungsi
#
# This py-file contains custom score functions initiated by
#
# from cerebunit.hypothesisTesting import XYZ
# ============================================================================

import numpy as np
from scipy.stats import norm
import quantities as pq


class HtestAboutMedians:
    """
    Hypothesis Testing (significance testing) about medians.
    ========================================================

    This is a nonparameteric test that does not assume specific type of distribution and hence **robust** (valid over broad range of circumstances) and **resistant** (to influence of outliers) test.


    1. Verify necessary data conditions.
    ------------------------------------

    +-------------------------------------+-------------------------------------+
    | Statistic                           | Interpretation                      |
    +=====================================+=====================================+
    | sample size, n                      | experiment/observed n               |
    +-------------------------------------+-------------------------------------+
    | optionally: data                    | experiment/observed data array      |
    +-------------------------------------+-------------------------------------+

    * n is **not** >= 30
    * data is **not** from normal distribution.

    2. Defining __null__ and __alternate__ hypotheses.
    --------------------------------------------------

    +-------------------------------------+-------------------------------------+
    | Statistic                           | Interpretation                      |
    +=====================================+=====================================+
    | sample statistic, e                 | experiment/observed median          |
    +-------------------------------------+-------------------------------------+
    | null value/population parameter, e0 | model prediction (specified value)  |
    +-------------------------------------+-------------------------------------+
    | null hypothesis, H0                 | e = e0                              |
    +-------------------------------------+-------------------------------------+
    | alternate hypothesis, Ha            | e =/= or < or > e0                  |
    +-------------------------------------+-------------------------------------+

    Two-sided hypothesis (default)
        H0: e = e0 and Ha: e =/= e0

    One-side hypothesis (left-sided)
        H0: e = e0 and Ha: e < e0

    One-side hypothesis (right-sided)
        H0: e = e0 and Ha: e > e0

    3. Assuming H0 is true, find p-value.
    -------------------------------------

    +-------------------------------------+-------------------------------------+
    | Statistic                           | Interpretation                      |
    +=====================================+=====================================+
    | sample size, n                      | experiment/observed n               |
    +-------------------------------------+-------------------------------------+
    | splus                               | number of values in sample > e0     |
    +-------------------------------------+-------------------------------------+
    | sminus                              | number of values in sample < e0     |
    +-------------------------------------+-------------------------------------+
    | n_u = splus + sminus                | number of values in sample =/= e0   |
    +-------------------------------------+-------------------------------------+
    | z_statistic, z                      | (splus - (n_u/2))/sqrt(n_u/4)       |
    +-------------------------------------+-------------------------------------+

    Using z look up table for standard normal curce which will return its corresponding p.

    4. Report and Answer the question, __Based on the p-value is the result (true H0) statistically significant?__
    --------------------------------------------------------------------------------------------------------------

    Answer is not provided by the class but it is up to the person viewing the reported result. The reports are obtained calling the attributes ``.statistics`` and ``.description``. This is illustrated below.

    ::

       ht = HtestAboutMedians( observation, prediction, score,
                               side="less_than" ) # side is optional
       score.description = ht.outcome
       score.statistics = ht.statistics

    """
    def __init__(self, observation, prediction, z_statistic, side="not_equal"):
        """This constructor method generated ``.statistics`` and ``.outcome`` (which is then assigned to ``.descirption`` within the validation test class where this hypothesis test class is implemented).

        **Arguments**

        +----------+------------------------+---------------------------------+
        | Argument | Representation         | Value type                      |
        +==========+========================+=================================+
        | first    | experiment/observation | dictionary that must have keys; |
        |          |                        |"median","sample_size","raw_data"|
        +----------+------------------------+---------------------------------+
        | second   | model prediction       | float                           |
        +----------+------------------------+---------------------------------+
        | third    | test score/z-statistic | float                           |
        +----------+------------------------+---------------------------------+
        | fourth   | sidedness of test      | string; "not_equal" (default)   |
        |          |                        | or "less_than", "greater_than"  |
        +----------+------------------------+---------------------------------+

        """
        self.sample_statistic = observation["median"] # quantities.Quantity
        self.sample_size = observation["sample_size"]
        self.specified_value = prediction # quantities.Quantity
        self.z_statistic = z_statistic
        self.side = side
        #
        self.outcome = self.test_outcome()
        #
        self.get_below_equal_above(np.array(observation["raw_data"]))
        self.statistics = self._register_statistics()

    @staticmethod
    def null_hypothesis(symbol_null_value, symbol_sample_statistic):
        "Returns the statement for the null hypothesis, H0."
        return "\nH0: "+ symbol_sample_statistic +" = "+ symbol_null_value

    @staticmethod
    def alternate_hypothesis(side, symbol_null_value, symbol_sample_statistic):
        "Returns the statement for the alternate hypothesis, Ha."
        if side is "less_than":
            return "\nHa: "+ symbol_sample_statistic +" < "+ symbol_null_value
        elif side is "greater_than":
            return "\nHa: "+ symbol_sample_statistic +" > "+ symbol_null_value
        else: #side is "not_equal
            return "\nHa: "+ symbol_sample_statistic +" =/= "+ symbol_null_value

    def _compute_pvalue(self):
        "Returns the p-value."
        right_side = norm.sf(self.z_statistic)
        if self.side is "less_than":
            return 1-right_side
        elif self.side is "greater_than":
            return right_side
        else: #side is "not_equal"
            return 2*( norm.sf(abs(self.z_statistic)) )

    def test_outcome(self):
        """Puts together the returned values of :py:meth:`.null_hypothesis`, :py:meth:`.alternate_hypothesis`, and :py:meth:`._compute_pvalue`. Then returns the string value for ``.outcome``.
        """
        self.pvalue = self._compute_pvalue()
        #
        symbol_null_value = "e0"
        symbol_sample_statistic = "e"
        parameters = ( symbol_null_value +" = "+str(self.specified_value)+", "
                + symbol_sample_statistic+" = "+str(self.sample_statistic)+", "
                + "n = "+str(self.sample_size) )
        outcome = ( self.null_hypothesis(symbol_null_value, symbol_sample_statistic)
             + self.alternate_hypothesis(self.side, symbol_null_value, symbol_sample_statistic)
             + "\nTest statistic: z = "+ str(self.z_statistic)
             + "\nAssuming H0 is true, p-value = "+ str(self.pvalue) )
        return parameters+outcome

    def get_below_equal_above(self, data):
        "Set values for the attributes ``.below``, ``.equal``, and ``.above`` the null value, e0 = ``.specified_value``."
        self.below = (data < self.specified_value).sum()
        self.equal = (data == self.specified_value).sum()
        self.above = (data > self.specified_value).sum()

    def _register_statistics(self):
        "Returns dictionary value for the ``.statistics``."
        return { "e0": self.specified_value, "e": self.sample_statistic, "n": self.sample_size,
                 "below": self.below, "equal": self.equal, "above": self.above,
                 "z": self.z_statistic, "p": self.pvalue, "side": self.side }
