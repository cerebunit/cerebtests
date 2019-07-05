# =============================================================================
# ~/cerebunit/cerebunit/statistics/data_conditions/forHTmeans.py
#
# create 3 July 2019 Lungsi
#
#
# =============================================================================

from scipy.stats import normaltest

class NecessaryForHTMeans(object):
    """doc
    """
    @staticmethod
    def check_normal_population(data):
        """Test if sample is from a normal distribution.
        scipy.stats.normaltest is based on D'Agostino & Pearson's omnibus test of normality.
        """
        alpha = 0.001
        k2, p = normaltest(data)
        if p < alpha: # null hypothesis: sample comes from normal distribution
            return True
        else:
            return False

    @classmethod
    def ask(cls, sample_size, experimental_data):
        if sample_size >= 30:
            return True
        else:
            try:
                return cls.check_normal_population( experimental_data )
            except:
                return False

