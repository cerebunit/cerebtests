# ============================================================================
# ~/cerebtests/cerebunit/stat_scores/zWilcoxSignedRank.py
#
# created 18 September 2019 Lungsi
#
# This py-file contains custum score functions initiated by
#
# from cerebunit import scoreScores
# from cerebunit.scoreScores import ABCScore
# ============================================================================

import numpy as np
import sciunit


# ======================ZScoreForWilcoxSignedRankTest=========================
class ZScoreForWilcoxSignedRankTest(sciunit.Score):
    """
    Compute z-statistic for Wilcox Signed Rank Test. Note that this is **not** Wilcoxon Signed Rank-Sum test.

    .. table:: Title here

    ====================  ============================================================================
      Definitions          Interpretation                    
    ====================  ============================================================================
    :math:`\eta_0`        some specified value :math:`^{\dagger}`
    :math:`x_i`           each data value
    :math:`|x_i-\eta_0|`  absolute difference between data value and null value
    :math:`T`             ranks of the computed absolute difference (excluding difference = 0 )
    :math:`T^+`           sum of ranks above :math:`\eta_0`; Wilcoxon signed-rank statistic
    :math:`n_U`           number of values in sample not equal to :math:`\\eta_0`; sample size
    :math:`\mu_{T^+}`     assuming :math:`H_0: \\nu = \\nu_0` is true,
                          :math:`\mu_{T^+}` = :math:`\\frac{ n_U(1+n_U) }{ 4 }`
    :math:`\sigma_{T^+}`  assuming :math:`H_0` is true,
                          :math:`\sigma_{T^+}` = :math:`\\sqrt{ \\frac{ n_U(1+n_U)(1+2n_U) }{24} }`
    z-statistic, z        z = :math:`\\frac{ T^+ - \mu_{T^+} }{ \sigma_{T^+} }`
    ====================  ============================================================================

    :math:`^{\dagger} \eta_0`, null value is

    * the model prediction for one sample testing
    * 0 for testing with paired data (observation - prediction)

    **NOTE:**

    * use this test only when the distribution is **symmetric** (not necessarily bell-shaped)
    * this test should **not** be used for skewed data
    * the test is *often* applied to paired data
    * :math:`\eta_0` is the prediction if its not a list of same length as the observation data
    * for paired data :math:`\eta_0 = 0` for zero poulation median difference
    
    **Use Case:**

    ::

      x = ZScoreForWilcoxSignedRankTest.compute( observation, prediction )
      score = ZScoreForWilcoxSignedRankTest(x)

    *Note*: As part of the `SciUnit <http://scidash.github.io/sciunit.html>`_ framework this custom :py:class:`.TScore` should have the following methods,

    * :py:meth:`.compute` (class method)
    * :py:meth:`.sort_key` (property)
    * :py:meth:`.__str__`

    Additionally,

    * :py:meth:`.get_observation_rank` (instance method)
    * :py:meth:`__orderdata_ranks` (private method)

    """
    #_allowed_types = (float,)
    _description = ( "ZScoreForWilcoxRankSumTest gives the z-statistic applied to a median of the population. "
                   + "The experimental data (observation) is taken as the sample-1. "
                   + "The simulated data (prediction) is taken as sample-2. "
                   + "There is no null-value, instead H0: n1=n2; median of sample-1 = median of sample-2. " )

    @classmethod
    def compute(cls, observation, prediction):
        """
        +----------------------------+------------------------------------------------+
        | Argument                   | Value type                                     |
        +============================+================================================+
        | first argument             | dictionary; observation/experimental data      |
        +----------------------------+------------------------------------------------+
        | second argument            | float or array; simulated data                 |
        +----------------------------+------------------------------------------------+

        *Note:*

        * observation **must** have the key "raw_data" whose value is the list of numbers
        * simulation, i.e, model prediction is not a float it  **must** also have the key "raw_data"

        """
        if np.array( prediction ).shape is (): # single sample test
            data = observation["raw_data"]
            eta0 = prediction
        else: # paired difference test
            data = observation["raw_data"] - prediction
            eta0 = 0
        # 
        Tplus = self.get_Tplus( data, eta0 )
        n_u = (data != eta0).sum()
        #
        muTplus = n_u * (n_u + 1) / 4
        sdTplus = np.sqrt( n_u * (n_u + 1) * (2*n_u + 1) / 24 )
        #
        self.score = (Tplus - muTplus) / sdTplus
        return self.score # z_statistic

    @property
    def sort_key(self):
        return self.score

    def __str__(self):
        return "ZScore is " + str(self.score)

    def get_Tplus(self, data, null_value):
        """Returns computed Wilcoxon signed-rank statistic, Tplus.

        * case1: data = observation["raw_data"], null_value = prediction
        * case2: data = observation["raw_data"] + prediction, null_value = 0

        *Example for describing what 'ranking' means:*

        :math:`data = [65, 55, 60, 62, 70]`

        :math:`null\_value = 60`

        Then,

        :math:`ordered\_data = [55, 60, 62, 65, 70]`

        :math:`absolute\_difference = [5, 0, 2, 5, 10]`

        :math:`absolute\_difference\_without\_zeros = [5, 2, 5, 10]`

        :math:`ordered\_data\_without\_zeros = [55, 62, 65, 70]`

        :math:`all\_ranks    =                 [1, 2, 3, 4]`

        Therefore, :math:`T^+`, Wilcoxon signed-rank statistic is

        :math:`Tplus= 1+2+3+4 = 10`

        """
        ordered_data = np.sort( data )
        # get rank
        abs_diff = np.abs( ordered_data - null_value )
        #
        abs_diff_no0s = abs_diff[ abs_diff != 0 ]
        non0indices = np.where( abs_diff != 0 )
        ordered_data_no0s = np.take( ordered_data, non0indices )[0]
        #
        all_ranks = self.__ranks_in_absdifferences_of_ordered_data( abs_diff_no0s )
        Tplus = 0
        for i in non0indices: # go through all the ordered data
            if ordered_data_no0s[i] > null_value:
                Tplus = Tplus + all_ranks[i]
        return Tplus

    def __ranks_in_absdifferences_of_ordered_data(self, absdiff_without_zero):
        """ Private function that orders the data and returns its appropriate rank.

        **Step-1:**

        * get unique values in the ordered data
        * also get the number of frequencies for each unique value

        **Step-2:**

        * construct raw ranks based on the ordered data

        **Step-4:**

        * for each value in the ordered data find its index in unique values array
        * if the corresponding count is more than one compute its midrank (sum ranks/its count)
        * set ranks (in raw ranks) for the corresponding number of values with the computed midrank
        
        """
        unique_values, counts = np.unique( absdiff_without_zero, return_counts=True )
        raw_ranks = [ i+1 for i in range(len(absdiff_without_zero)) ]
        #
        i = 0 # initiate from first index of ordered_data and raw_ranks
        while i < len(absdiff_without_zero):
            indx_in_uniques = int( np.where( unique_values == absdiff_without_zero[i] )[0] )
            if counts[indx_in_uniques]>1:
                numer = 0.0
                numer = [ numer + raw_ranks[i+j] for j in range( counts[indx_in_uniques] ) ][0]
                for j in range( counts[indx_in_uniques] ):
                    raw_ranks[i+j] = numer/counts[indx_in_uniques]
            # raw_ranks[i] does not need to be set for counts = 1
            i = i + counts[indx_in_uniques] # update loop (skipping repeated values)
        return raw_ranks
# ============================================================================
