# ============================================================================
# ~/cerebunit/cerebunit/hypothesisTesting.py
#
# created 7 March 2019 Lungsi
#
# This py-file contains custum score functions initiated by
#
# from cerebunit.hypothesisTesting import XYZ
# ============================================================================

from scipy.stats import t as student_t
import quantities as pq

# ==========================HtestAboutMeans===================================
# created  6 March 2019 Lungsi
# modified 
#
class HtestAboutMeans:
    '''
    Hypothesis Testing (significance testing) about means.
    '''
    #
    # -----------------------------Use Case-----------------------------------
    # score.description = HtestAboutMeans( observation, prediction, score,
    #                                      side="less_than" ) # side is optional
    # ------------------------------------------------------------------------
    #
    def __init__(self, observation, prediction, t_statistic, side="not_equal"):
        # observation -- dictionary; must have keys: 'mean', 'sample_size'
        # prediction -- float; model prediction
        # t_statistic -- float; test score
        # side -- string; less_than, greater_than, not_equal(default)
        self.sample_statistic = observation["mean"] # quantities.Quantity
        self.sample_size = observation["sample_size"]
        self.populn_parameter = prediction # quantities.Quantity
        self.t_statistic = t_statistic
        self.side = side
        self.deg_of_freedom = self.sample_size - 1
        self.outcome = self.test_outcome()

    def test_outcome(self):
        self.pvalue = self._compute_pvalue()
        symbol_null_value = chr(0x3bc).encode('utf-8') + "0" # mu_0
        symbol_sample_statistic = chr(0x3bc).encode('utf-8') # mu
        parameters = ( symbol_null_value +" = "+str(self.populn_parameter)+", "
                + symbol_sample_statistic+" = "+str(self.sample_statistic)+", "
                + "n = "+str(self.sample_size) )
        outcome = ( self.null_hypothesis(symbol_null_value, symbol_sample_statistic)
             + self.alternate_hypothesis(self.side, symbol_null_value, symbol_sample_statistic)
             + "\nTest statistic: t = "+ str(self.t_statistic)
             + "\nAssuming H0 is true, p-value ="+ str(self.pvalue) )
        return parameters+outcome

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

    #@staticmethod
    def _compute_pvalue(self):
        left_side = student_t.cdf(self.t_statistic, self.deg_of_freedom)
        if self.side is "less_than":
            return left_side
        elif self.side is "greater_than":
            return 1-left_side
        else: #side is "not_equal"
            return 2*(1-left_side)
