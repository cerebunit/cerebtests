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

    Implementation
    --------------

    +-------------------------------------+--------------------------------+
    | Method name                         | Arguments                      |
    +=====================================+================================+
    | :py:meth:`.ask`                     | sample_size, experimental_data |
    +-------------------------------------+--------------------------------+
    | :py:meth:`.check_normal_population` | data                           |
    +-------------------------------------+--------------------------------+

    """
    @staticmethod
    def check_normal_population(data):
        """Tests if sample is from a normal distribution.

        Algorithm to check if population is normal
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        .. math::

           \\textbf{Given:} data

           \\textbf{Parameter:} \\alpha = 0.001

           \\textbf{Compute:} p \\leftarrow \\texttt{normaltest}(data)
           \\textbf{if} p < \\alpha
                   \\text{"data is normal"}
           \\textbf{else}
                   \\text{"data is not normal"}

        *Note:*

        * :math:`\\alpha` is an arbitrarily small value, here taken as equal to 0.001
        * `scipy.stats.normaltest <https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.normaltest.html>`_ is based on `D'Agostino <https://doi.org/10.1093/biomet/58.2.341>`_ & `Pearson's <https://doi.org/10.1093/biomet/60.3.613>`_ omnibus test of normality.

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

        Algorithm that asks if the distribution of an experimental data is normal, given its sample size.
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        .. math::

           \\textbf{Given:} sample_size, experimental_data

           \\textbf{if} sample_size \\geq 30
                   \\text{"data is normal"}
           \\textbf{else}
                   \\textit{invoke} :py:meth:`.check_normal_population`

        *Note:*

        * sample size of 30 is taken as the lower bound for considering central limit theorem.

        """
        if sample_size >= 30:
            return True
        else:
            try:
                return cls.check_normal_population( experimental_data )
            except:
                return False

