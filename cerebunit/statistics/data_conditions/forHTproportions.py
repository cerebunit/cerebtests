# =============================================================================
# ~/cerebtests/cerebunit/statistics/data_conditions/forHTproportions.py
#
# create 18 October 2019 Lungsi
#
# =============================================================================

from scipy.stats import normaltest, skew

class NecessaryForHTProportions(object):
    """
    **Checks for situations for which Hypothesis Testing About Proportions is valid, i.e, is t-Test (or standard z-score) valid?**


    **Situation-1**

    With respect to distributions condition for hypothesis testing about proportions is valid if

    - random sample (from population)
    - data from `binomial experiment <https://en.wikipedia.org/wiki/Binomial_distribution>`_ **with independent trials**.

    Below are some rule-of-thumbs guide to check if an experiment if binomial:

    - it is repeated a fixed number of times

    - trials are independent

    - trial outcomes are either success or failure

    - probability of success is the same for all trials.


    **Situation-2**

    Hypothesis testing about proportions is also valid when **both** the quantities :math:`np` **and** :math:`n(1 - p_0)` are *at least* :math:`5^{\dagger}`. Note that, :math:`n` is the sample size and :math:`p_0` is the null value. Some consider :math:`10^{\ddagger}` (instead of 5) as the lower bound.

    - Ott, R.L. (1998). An Introduction to Statistical Methods and Data Analysis. (p.370) :math:`^{\dagger}`
    - Utts, J.M, Heckard, R.F. (2010). Mind on Statistics. (p.465) :math:`^{\ddagger}`

    **Implementation**

    +-------------------------------------+--------------------------------+
    | Method name                         | Arguments                      |
    +=====================================+================================+
    | :py:meth:`.ask`                     | experimental_data              |
    +-------------------------------------+--------------------------------+

    """
    @staticmethod
    def ask(n, p0, lb=5):
        """This function checks if the sample size requirement for running hypothesis testing for proportions.

        +------------+-------------------------------+
        | Arguments  | Meaning                       |
        +============+===============================+
        | first, n   | sample size                   |
        +------------+-------------------------------+
        | second, p0 | null value                    |
        +------------+-------------------------------+
        | third, lb  | lower bound (5 (default))     |
        +------------+-------------------------------+

        Algorithm that asks if the distribution of an experimental data is normal.

        --------

        |  **Given:** :math:`n, p0, lb`
        |  **Compute** result1 :math:`\\leftarrow` :math:`np_0`
        |  **Compute** result2 :math:`\\leftarrow` :math:`n(1-p_0)`
        |  **if** result1 :math:`\\cap` result2 :math:`\\geq lb`
        |         "sample size requirement is satified"
        |  **else**
        |         "sample size requirement is not satisfied"

        --------

        *Note:*

        * boolean return (`True` or `False`)
        * `True` if sample size requirement is satisfied
        * `False` if sample size requirement is **not** satisfied

        """
        #    raise ValueError("question must be normal? or skew?")
        np0_check = lambda n,p0,lb: True if n*p0 >= lb else False
        n1minusp0_check = lambda n,p0,lb: True if ( n*(1-p0) ) >= lb False
        if ( np0_check(lb, n, p0) and n1minusp0_check(lb, n, p0) is True ):
            return True
        else:
            return False
