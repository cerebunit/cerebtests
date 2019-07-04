# ============================================================================
# ~/cerebunit/cerebunit/hypothesis_testings/tTest.py
#
# created 7 March 2019 Lungsi
# modified 4 July 2019 Lungsi
#
# This py-file contains custom score functions initiated by
#
# from cerebunit.hypothesisTesting import XYZ
# ============================================================================

from scipy.stats import t as student_t
import quantities as pq


class HtestAboutMeans:
    """
    Hypothesis Testing (significance testing) about means.
    ======================================================

    1. Verify necessary data conditions.
    ------------------------------------

    +-------------------------------------+-------------------------------------+
    | Statistic                           | Interpretation                      |
    +=====================================+=====================================+
    | sample size, n                      | experiment/observed n               |
    +-------------------------------------+-------------------------------------+
    | optionally: raw data                | experiment/observed data array      |
    +-------------------------------------+-------------------------------------+

    Is n >= 30?

    If not, check if data is from normal distribution.

    If both returns NO, you can't perform hypothesis testing about means.
    Instead use sign test.

    If either of the above two question returns YES continue below.

    2. Defining __null__ and __alternate__ hypotheses.
    --------------------------------------------------

    +-------------------------------------+-------------------------------------+
    | Statistic                           | Interpretation                      |
    +=====================================+=====================================+
    | sample statistic, u                 | experiment/observed mean            |
    +-------------------------------------+-------------------------------------+
    | null value/population parameter, u0 | model prediction                    |
    +-------------------------------------+-------------------------------------+
    | null hypothesis, H0                 | u = u0                              |
    +-------------------------------------+-------------------------------------+
    | alternate hypothesis, Ha            | u =/= or < or > u0                  |
    +-------------------------------------+-------------------------------------+

    Two-sided hypothesis (default)
        H0: u = u0 and Ha: u =/= u0

    One-side hypothesis (left-sided)
        H0: u = u0 and Ha: u < u0

    One-side hypothesis (right-sided)
        H0: u = u0 and Ha: u > u0

    3. Assuming H0 is true, find p-value.
    -------------------------------------

    +-------------------------------------+-------------------------------------+
    | Statistic                           | Interpretation                      |
    +=====================================+=====================================+
    | sample size, n                      | experiment/observed n               |
    +-------------------------------------+-------------------------------------+
    | standard error, SE                  | experiment/observed SE = SD/sqrt(n) |
    | or                                  | or                                  |
    | standard deviation, SD              | experiment/observed SD              |
    +-------------------------------------+-------------------------------------+
    | t-statistic, t                      | test score = (u - u0)/SE            |
    +-------------------------------------+-------------------------------------+
    | degree of freedom, df               | n - 1                               |
    +-------------------------------------+-------------------------------------+

    Using t and df look up table for t-distrubution which will return its corresponding p.

    4. Answer, Based on the p-value is the result (true H0) statistically significant?
    ----------------------------------------------------------------------------------

    5. Report.
    ----------

    How to use.
    ===========

    ::

       ht = HtestAboutMeans( observation, prediction, score,
                             side="less_than" ) # side is optional
       score.description = ht.outcome
       score.statistics = ht.statistics

    """
    def __init__(self, observation, prediction, t_statistic, side="not_equal"):
        """
        **Arguments**

        +----------+------------------------+---------------------------------+
        | Argument | Representation         | Value type                      |
        +==========+========================+=================================+
        | first    | experiment/observation | dictionary that must have keys; |
        |          |                        | "mean" and "sample_size"        |
        +----------+------------------------+---------------------------------+
        | second   | model prediction       | float                           |
        +----------+------------------------+---------------------------------+
        | third    | test score/t-statistic | float                           |
        +----------+------------------------+---------------------------------+
        | fourth   | sidedness of test      | string; "not_equal" (default)   |
        |          |                        | or "less_than", "greater_than"  |
        +----------+------------------------+---------------------------------+

        """
        self.sample_statistic = observation["mean"] # quantities.Quantity
        self.sample_size = observation["sample_size"]
        self.popul_parameter = prediction # quantities.Quantity
        self.t_statistic = t_statistic
        self.side = side
        self.deg_of_freedom = self.sample_size - 1
        #
        self.outcome = self.test_outcome()
        #
        self.standard_error = observation["standard_error"]
        self.statistics = self._register_statistics()

    @staticmethod
    def null_hypothesis(symbol_null_value, symbol_sample_statistic):
        return "\nH0: "+ symbol_sample_statistic +" = "+ symbol_null_value

    @staticmethod
    def alternate_hypothesis(side, symbol_null_value, symbol_sample_statistic):
        if side is "less_than":
            return "\nHa: "+ symbol_sample_statistic +" < "+ symbol_null_value
        elif side is "greater_than":
            return "\nHa: "+ symbol_sample_statistic +" > "+ symbol_null_value
        else: #side is "not_equal
            return "\nHa: "+ symbol_sample_statistic +" =/= "+ symbol_null_value

    def _compute_pvalue(self):
        left_side = student_t.cdf(self.t_statistic, self.deg_of_freedom)
        if self.side is "less_than":
            return left_side
        elif self.side is "greater_than":
            return 1-left_side
        else: #side is "not_equal"
            return 2*(1-left_side)

    def test_outcome(self):
        self.pvalue = self._compute_pvalue()
        #symbol_null_value = unichr(0x3bc).encode('utf-8') + "0" # mu_0; chr for Python3
        #symbol_sample_statistic = unichr(0x3bc).encode('utf-8') # mu
        symbol_null_value = "u0"
        symbol_sample_statistic = "u"
        parameters = ( symbol_null_value +" = "+str(self.popul_parameter)+", "
                + symbol_sample_statistic+" = "+str(self.sample_statistic)+", "
                + "n = "+str(self.sample_size) )
        outcome = ( self.null_hypothesis(symbol_null_value, symbol_sample_statistic)
             + self.alternate_hypothesis(self.side, symbol_null_value, symbol_sample_statistic)
             + "\nTest statistic: t = "+ str(self.t_statistic)
             + "\nAssuming H0 is true, p-value = "+ str(self.pvalue) )
        return parameters+outcome

    def _register_statistics(self):
        return { "u0": self.popul_parameter, "u": self.sample_statistic,
                 "n": self.sample_size, "df": self.deg_of_freedom,
                 "t": self.t_statistic, "se": self.standard_error }
