# ~/managers/operatorsStatistics/inference_popmean.py
from scipy import stats

class InferencePopMean(object):
    def __init__(self):
        pass

    @staticmethod
    def set_null_hypothesis(statistical_inference, mu0):
        """returns statistical_inference dictionary with 'H0' key value set.
        """
        if "H0" in statistical_inference:
            statistical_inference["H0"] = {"mu0": mu0}
        else:
            statistical_inference.update( {"H0": {"mu0": mu0}} )

    @staticmethod
    def set_research_hypothesis(statistical_inference, tail):
        """returns statistical_inference dictionary with 'Ha' key value set.
        tail -- string; '=', '>', '<'
        """
        if "H0" not in statistical_inference:
            raise ValueError("statistical_inference must have the key 'H0', that is, set_null_hypothesis must be called first")
        elif "Ha" in statistical_inference:
            statistical_inference["Ha"] = {"mu": tail + str(statistical_inference["H0"]["mu0"])}
        else:
            statistical_inference.update( {"Ha":
                                          {"mu": tail + str(statistical_inference["H0"]["mu0"])}
                                        } )

    @staticmethod
    def set_test_statistic(statistical_inference, test_statistic):
        """returns statistical_inference dictionary with 'TS' key value set.
        """
        if "Ha" not in statistical_inference:
            raise ValueError("statistical_inference must have the key 'Ha', that is, set_research_hypothesis must be evoked before calling this method")
        elif "TS" in statistical_inference:
            statistical_inference["TS"] = test_statistic
        else:
            statistical_inference.update( {"TS": test_statistic} )

    @staticmethod
    def get_pvalue_zstat(statistical_inference):
        tail = statistical_inference["Ha"]["mu"][0]
        test_score = statistical_inference["TS"].values()[0]
        if (tail==">") or (tail=="<"):
            return stats.norm.sf( abs(test_score) )
        else:
            return 2*stats.norm.sf( abs(test_score) )

    @staticmethod
    def get_pvalue_tstat(statistical_inference):
        tail = statistical_inference["Ha"]["mu"][0]
        test_score = statistical_inference["TS"]["t-score"]
        df = statistical_inference["TS"]["sample-size"] - 1
        if (tail==">") or (tail=="<"):
            return stats.norm.sf( abs(test_score), df )
        else:
            return 2*stats.norm.sf( abs(test_score), df )

    @classmethod
    def get_pvalue(cls, statistical_inference):
        test_statistic = statistical_inference["TS"]
        for scoretype, value in test_statistic.iteritems():
            if scoretype=="z-score":
                return cls.get_pvalue_zstat(statistical_inference)
            elif scoretype=="t-score":
                return cls.get_pvalue_tstat(statistical_inference)

    @staticmethod
    def get_pdescription(statistical_inference):
        mu0 = statistical_inference["H0"]["mu0"]
        test_score = statistical_inference["TS"].values()[0]
        p_value = statistical_inference["p-value"]
        desc = "Assuming that, mu0 = "+str(mu0)+" is true, the probability that the test-statistic would take the value of the observed test-score = "+str(test_score)+" is p-value = "+str(p_value)
        return desc
            
    @classmethod
    def set_pvalue(cls, statistical_inference):
        """returns statistical_inference dictionary with 'TS' key value set.
        """
        if "TS" not in statistical_inference:
            raise ValueError("statistical_inference must have the key 'TS', that is, set_test_statistic must be evoked before calling this method")
        elif "p-value" in statistical_inference:
            statistical_inference["p-value"] = cls.get_pvalue(statistical_inference)
            statistical_inference.update( {"p-description": cls.get_pdescription(statistical_inference)} )
        else:
            statistical_inference.update( {"p-value": cls.get_pvalue(statistical_inference)} )
            statistical_inference.update( {"p-description": cls.get_pdescription(statistical_inference)} )

    @staticmethod
    def deduce(statistical_inference, alpha):
        mu0 = statistical_inference["H0"]["mu0"]
        mu = statistical_inference["Ha"]["mu"]
        p_value = statistical_inference["p-value"]
        if p_value <= alpha:
            return "reject H0: mu0 = "+str(mu0)+" because p-value = "+str(p_value)+" is small; small defined as p-value <= "+str(alpha)+", the level of significance. Thus accept Ha: mu "+mu
        else:
            return "there is not enough evidence to reject H0: mu0 = "+str(mu0)+" because p-value = "+str(p_value)+" is not small; small defined as p-value > "+str(alpha)+", the level of significance."

    @classmethod
    def set_conclusion(cls, statistical_inference, alpha):
        """returns Fin
        """
        if "p-value" not in statistical_inference:
            raise ValueError("statistical_inference must have the key 'p-value', that is, set_pvalue must be evoked before calling this method")
        else:
            deduction = cls.deduce(statistical_inference, alpha)
            statistical_inference.update(
                   {"Fin": "For a probability alpha = "+str(alpha)+" of a type-I error, "+deduction} )
