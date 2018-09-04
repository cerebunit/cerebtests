# ~/managers/operatorsStatistics/inference_popmean_largesample.py

class InferencePopMeanLargeN(object):
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
    def get_alpha_default(tail):
        if tail==">" or tail=="<":
            return 0.025
        else:
            return 0.05
            
    @staticmethod
    def get_sigma_coeff(alpha):
        if (alpha==0.025) or (alpha==0.05):
            return 1.96
        elif (alpha==0.01) or (alpha==0.02):
            return 2.33

    @staticmethod
    def deduce(tail, sigma_coeff, zscore):
        if (tail==">") and (zscore > sigma_coeff):
            return "reject H0 because test-statistic, z = "+ str(zscore) +" > "+ str(sigma_coeff)
        elif (tail=="<") and (score < -sigma_coeff):
            return "reject H0 because test-statistic, z = "+ str(zscore) +" < "+ str(sigma_coeff)
        elif (tail=="=") and (abs(score) > sigma_coeff):
            return "reject H0 because test-statistic, |z| = "+str(abs(zscore))+" > "+str(sigma_coeff)
        else:
            return "accept H0"

    @classmethod
    def set_rejection_region(cls, statistical_inference, alpha):
        """returns RR
        """
        tail = statistical_inference["Ha"]["mu"][0]
        sigma_coeff = cls.get_sigma_coeff( alpha )
        deduction = cls.deduce( tail, sigma_coeff, statistical_inference["TS"] )
        if "RR" not in statistical_inference:
            statistical_inference.update(
                   {"RR": "For a probability alpha = "+str(alpha)+" of a type-I error, "+deduction} )
        else:
            statistical_inference["RR"] = "For a probability alpha = "+str(alpha)+" of a type-I error, "+deduction
