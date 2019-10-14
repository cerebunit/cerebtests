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
    :math:`n_U`           number of values in sample not equal to :math:`\\nu_0`; sample size
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
        | second argument            | float or dictionary; simulated data            |
        +----------------------------+------------------------------------------------+

        *Note:*

        * observation **must** have the key "raw_data" whose value is the list of numbers
        * simulation, i.e, model prediction is not a float it  **must** also have the key "raw_data"

        """
        if hasattr(prediction, '__len__'):
            eta0 = prediction
            n2 = len(prediction)
        else: # paired data
            eta0 = 0
            n2 = 1
        n1 = len( observation["raw_data"] )
        N = n1 + n2
        #
        mu_W = n1*(1+N)/2
        sigma_W = np.sqrt( n1*n2*(1+N)/12 )
        #
        obs_rank = cls.get_observation_rank( observation, prediction )
        W = np.sum( obs_rank )
        #
        self.score = (W - mu_W) / sigma_W
        return self.score # z_statistic

    @property
    def sort_key(self):
        return self.score

    def __str__(self):
        return "ZScore is " + str(self.score)

    def get_observation_rank(self, observation, prediction):
        """Returns ranks for the observation data.

        * sample 1, observation["raw_data"]
        * sample 2, prediction["raw_data"]

        *Example for describing what 'ranking' means:*

        :math:`sample1 = [65, 60, 62, 70]`

        :math:`sample2 = [60, 55, 65, 70]`

        Then,

        :math:`ordered\_data = [55, 60, 60, 62, 65, 65, 70, 70]`

        :math:`raw\_ranks    = [ 1,  2,  3,  4,  5,  6,  7,  8]`

        and

        :math:`correct\_ranks= [ 1, 2.5, 2.5, 4, 5.5, 5.5, 7.5, 7.5]`

        Therefore, ranks for sample1 is

        :math:`sample1\_ranks = [5.5, 2.5, 4, 7.5]`

        **NOTE:**

        * corrected ranks have midranks for repeated values
        * the returned sample1 rank is numpy array 

        """
        ordered_data, all_ranks = self.__orderdata_ranks(observation, prediction)
        sample1 = np.array( observation["raw_data"] )
        sample1_ranks = np.zeros((1,len(sample1)))[0]
        for i in range(len(ordered_data)): # go through all the ordered data
            a_data = ordered_data[i]
            its_rank = all_ranks[i]
            # for each picked data value get its index w.r.t sample1
            indx_in_sample1 = np.where( sample1 == a_data )[0]
            if len(indx_in_sample1)>1: # if the picked data value exists within sample1
                for j in range( len(indx_in_sample1) ): # at each corresponding index in sample1
                    sample1_ranks[ indx_in_sample1[j] ] = its_rank # set appropriate rank
        #return sample1_ranks
        absolute_diffs = np.zeros((1,len(observation)))[0]
        for i in range(len(observation)):
            absolute_diffs[i] = abs( observation[i] - eta0 )

    def __orderdata_ranks(self, observation, prediction):
        """ Private function that orders the data and returns its appropriate rank.

        * sample 1, observation["raw_data"]
        * sample 2, prediction["raw_data"]

        **Step-1:**

        * append the two lists (i.e, the two samples)
        * order the values in ascending manner

        **Step-2:**

        * get unique values in the ordered data
        * also get the number of frequencies for each unique value

        **Step-3:**

        * construct raw ranks based on the ordered data

        **Step-4:**

        * for each value in the ordered data find its index in unique values array
        * if the corresponding count is more than one compute its midrank (sum ranks/its count)
        * set ranks (in raw ranks) for the corresponding number of values with the computed midrank
        
        """
        ordered_data = np.sort( observation["raw_data"] + prediction["raw_data"] )
        unique_values, counts = np.unique( ordered_data, return_counts=True )
        raw_ranks = [ i+1 for i in range(len(ordered_data)) ]
        #
        i = 0 # initiate from first index of ordered_data and raw_ranks
        while i < len(ordered_data):
            indx_in_uniques = int( np.where( unique_values == ordered_data[i] )[0] )
            if counts[indx_in_uniques]>1:
                numer = 0.0
                numer = [ numer + raw_ranks[i+j] for j in range( counts[indx_in_uniques] ) ][0]
                for j in range( counts[indx_in_uniques] ):
                    raw_ranks[i+j] = numer/counts[indx_in_uniques]
            # raw_ranks[i] does not need to be set for counts = 1
            i = i + counts[indx_in_uniques] # update loop (skipping repeated values)
        return [ ordered_data, raw_ranks ] 
# ============================================================================
