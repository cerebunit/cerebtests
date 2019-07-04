# ============================================================================
# ~/cerebunit/cerebunit/stat_scores/tScore.py
#
# created 6 March 2019 Lungsi
#
# This py-file contains custom score functions initiated by
#
# from cerebunit import scoreScores
# from cerebunit.scoreScores import ABCScore
# ============================================================================

import sciunit


# ==========================TScore=======================================
# created  6 March 2019 Lungsi
# modified 
#
class TScore(sciunit.Score):
    '''
    Compute t-statistic as the standardized statistic
    
    '''
    #
    # -----------------------------Use Case-----------------------------------
    # x = TScore.compute( observation, prediction )
    # score = TScore(x)
    # ------------------------------------------------------------------------
    #
    #_allowed_types = (float,)
    _description = ( "TScore gives the student-t as the standardized statistic applied to means. "
                   + "The experimental data (observation) is taken as the sample. "
                   + "The sample statisic is 'mean' and s.e is the 'standard_error' of this sample. "
                   + "The population parameter or null-value is the the predicted value generated from running the model. " )

    @classmethod
    def compute(self, observation, prediction):
        # observation (sample) is in dictionary form with keys mean and
        # standard_error whose value has magnitude and python quantity
        # the populations parameter is the predicted value
        self.score = ((observation["mean"] - prediction)/observation["standard_error"])
        return self.score # t_statistic

    @property
    def sort_key(self):
        return self.score

    def __str__(self):
        return "TScore is " + str(self.score)
# ============================================================================
#
# ==========================Score=============================================
class NameHereScore(sciunit.Score):
    '''
    text
    '''

    def __init__(self):
        pass
# ============================================================================

