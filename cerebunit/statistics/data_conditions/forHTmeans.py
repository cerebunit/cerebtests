# =============================================================================
# ~/cerebtests/cerebunit/statistics/data_conditions/forHTmeans.py
#
# create 3 July 2019 Lungsi
#
# =============================================================================

from scipy.stats import normaltest

class NecessaryForHTMeans(object):
    """
    Checks for situations for which Hypothesis Testing About Means is valid, i.e, is t-Test valid?
    ==============================================================================================

    Situation-1
    -----------

    For large sample sizes, n >= 30, where 30 is the arbitrary demarcation for __large__. This situtation assumes that the population of the measurements (of interest) is not normal.

    Situation-2
    -----------

    When there is not evidence of extreme outliers or skewed population shape. This is usually the case for population of the measurements that are approximately normal.

    """
    @staticmethod
    def check_normal_population(data):
        """Test if sample is from a normal distribution.
        scipy.stats.normaltest is based on D'Agostino & Pearson's omnibus test of normality.
        """
        alpha = 0.001 # an arbitrarily small alpha value
        k2, p = normaltest(data)
        if p < alpha: # null hypothesis: sample comes from normal distribution
            return True
        else:
            return False

    @classmethod
    def ask(cls, sample_size, experimental_data):
        """If the sample size is large the data condition is met otherwise check if the distribution of the raw data is normal.
        """
        if sample_size >= 30:
            return True
        else:
            try:
                return cls.check_normal_population( experimental_data )
            except:
                return False

