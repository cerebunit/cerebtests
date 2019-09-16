# ============================================================================
# ~/cerebtests/cerebunit/stat_scores/zTwoSampleRankSum.py
#
# created 16 September 2019 Lungsi
#
# This py-file contains custum score functions initiated by
#
# from cerebunit import scoreScores
# from cerebunit.scoreScores import ABCScore
# ============================================================================

import numpy as np
import sciunit


# ======================ZScoreForTwoSampleRankSumTest=========================
class ZScoreForTwoSampleRankSumTest(sciunit.Score):
    """
    Compute z-statistic for Two Sample Rank-Sum Test (aka, Wilcoxon rank-sum or Mann-Whitney test). Note that this is **not** Wilcoxon Signed Rank test.

    .. table:: Title here

    ================= ================================================================================
      Definitions      Interpretation                    
    ================= ================================================================================
    :math:`\eta_0`    some specified value              
    :math:`n_1`       sample size for sample 1
    :math:`n_2`       sample size for sample 2
    :math:`N`         total sample size, :math`n_1 + n_2`
    :math:`W`         sum of ranks for observations in sample 1 (post dataset ranking)
    :math:`\mu_W`     assuming :math:`H_0` is true, :math:`\mu_W` = :math:`\\frac{ n_1(1+N) }{ 2 }`
    :math:`\sigma_W`  assuming :math:`H_0` is true,
                      :math:`\mu_W` = :math:`\\sqrt{ \\frac{ n_1 n_2 (1+N) }{12} }`
    z-statistic, z    z = :math:`\\frac{ W - \mu_W }{ \sigma_W }`
    ================= ================================================================================

    **NOTE:**

    * :math:`H_0` is true :math:`\Rightarrow` for samples 1 and 2 their population distributions are the same
    *
    
    **Use Case:**

    ::

      x = ZScoreForTwoSampleRankSumTest.compute( observation, prediction )
      score = ZScoreForTwoSampleRankSumTest(x)

    *Note*: As part of the `SciUnit <http://scidash.github.io/sciunit.html>`_ framework this custom :py:class:`.TScore` should have the following methods,

    * :py:meth:`.compute` (class method)
    * :py:meth:`.sort_key` (property)
    * :py:meth:`.__str__`

    """
    #_allowed_types = (float,)
    _description = ( "ZScoreForSignTest gives the z-statistic applied to medians. "
                   + "The experimental data (observation) is taken as the sample. "
                   + "The sample statistic is 'median' or computed median form 'raw_data'. "
                   + "The null-value is the 'some' specified value whic is taken to be the predicted value generated from running the model. " )

    @classmethod
    def compute(self, observation, prediction):
        """
        +----------------------------+------------------------------------------------+
        | Argument                   | Value type                                     |
        +============================+================================================+
        | first argument             | dictionary; observation/experimental data      |
        +----------------------------+------------------------------------------------+
        | second argument            | floating number                                |
        +----------------------------+------------------------------------------------+

        *Note:*

        * observation **must** have the key "raw_data" whose value is the list of numbers

        """
        data = np.array( observation["raw_data"] )
        splus = ( data < prediction ).sum()
        n_u = (data != prediction ).sum()
        self.score = (splus - (n_u/2)) / np.sqrt(n_u/4)
        return self.score # z_statistic

    @property
    def sort_key(self):
        return self.score

    def __str__(self):
        return "ZScore is " + str(self.score)
# ============================================================================
