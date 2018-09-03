# ~/managers/operatorsStatistics/inference_popmean_largesample_Test.py
import unittest

from inference_popmean_largesample import InferencePopMeanLargeN as iml

class InferencePopMeanLargeNTest(unittest.TestCase):

    def setUp(self):
        self.hypothesis_testing = {}

    #@unittest.skip("reason for skipping")
    def test_1_set_null_hypothesis(self):
        hypothesis_testing = {}
        iml.set_null_hypothesis(hypothesis_testing, 25)
        self.assertEqual( hypothesis_testing["H0"], {"mu0": 25} )

    #@unittest.skip("reason for skipping")
    def test_2_set_null_hypothesis_modify(self):
        hypothesis_testing = {"H0": {"mu": 25}}
        iml.set_null_hypothesis(hypothesis_testing, 520)
        self.assertEqual( hypothesis_testing["H0"]["mu0"], 520 )

    #@unittest.skip("reason for skipping")
    def test_3_set_research_hypothesis_error(self):
        hypothesis_testing = {}
        self.assertRaises( ValueError,
                           iml.set_research_hypothesis,
                           hypothesis_testing, ">" )

    #@unittest.skip("reason for skipping")
    def test_4_set_research_hypothesis(self):
        hypothesis_testing = {}
        iml.set_null_hypothesis(hypothesis_testing, 520)
        iml.set_research_hypothesis(hypothesis_testing, "=")
        self.assertEqual( hypothesis_testing["Ha"], {"mu": "=520"} )

    #@unittest.skip("reason for skipping")
    def test_5_set_research_hypothesis_modify(self):
        hypothesis_testing = {}
        iml.set_null_hypothesis(hypothesis_testing, 520)
        iml.set_research_hypothesis(hypothesis_testing, "=")
        iml.set_research_hypothesis(hypothesis_testing, ">")
        self.assertEqual( hypothesis_testing["Ha"], {"mu": ">520"} )

    #@unittest.skip("reason for skipping")
    def test_6_set_test_statistic_error(self):
        hypothesis_testing = {}
        self.assertRaises( ValueError,
                           iml.set_test_statistic,
                           hypothesis_testing, 2.56 )

    #@unittest.skip("reason for skipping")
    def test_7_set_test_statistic(self):
        hypothesis_testing = {}
        iml.set_null_hypothesis(hypothesis_testing, 520)
        iml.set_research_hypothesis(hypothesis_testing, ">")
        iml.set_test_statistic(hypothesis_testing, 1.56)
        self.assertEqual( hypothesis_testing["TS"], 1.56 )

    #@unittest.skip("reason for skipping")
    def test_8_set_test_statistic_modify(self):
        hypothesis_testing = {}
        iml.set_null_hypothesis(hypothesis_testing, 520)
        iml.set_research_hypothesis(hypothesis_testing, ">")
        iml.set_test_statistic(hypothesis_testing, 1.56)
        iml.set_test_statistic(hypothesis_testing, 2.56)
        self.assertEqual( hypothesis_testing["TS"], 2.56 )

    #@unittest.skip("reason for skipping")
    def test_9_get_alpha_default(self):
        x1 = iml.get_alpha_default(">")
        x2 = iml.get_alpha_default("<")
        x3 = iml.get_alpha_default("=")
        self.assertEqual( [x1, x2, x3], [0.025, 0.025, 0.05] )

    #@unittest.skip("reason for skipping")
    def test_10_get_sigma_coeff(self):
        x1 = iml.get_sigma_coeff(0.025)
        x2 = iml.get_sigma_coeff(0.05)
        self.assertEqual( [x1, x2], [1.96, 1.96] )

    #@unittest.skip("reason for skipping")
    def test_11_deduce_reject(self):
        hypothesis_testing = {}
        tail = ">"
        alpha = iml.get_alpha_default(">")
        iml.set_null_hypothesis(hypothesis_testing, 520)
        iml.set_research_hypothesis(hypothesis_testing, tail)
        iml.set_test_statistic(hypothesis_testing, 2.56)
        sigma_coeff = iml.get_sigma_coeff( alpha )
        self.assertEqual( iml.deduce( tail, sigma_coeff, hypothesis_testing["TS"] ),
                          "reject H0 because test-statistic, z = 2.56 > "+str(sigma_coeff) )

    #@unittest.skip("reason for skipping")
    def test_12_deduce_accept(self):
        hypothesis_testing = {}
        tail = ">"
        alpha = 0.01
        iml.set_null_hypothesis(hypothesis_testing, 380)
        iml.set_research_hypothesis(hypothesis_testing, tail)
        iml.set_test_statistic(hypothesis_testing, 2.01)
        sigma_coeff = iml.get_sigma_coeff( alpha )
        self.assertEqual( iml.deduce( tail, sigma_coeff, hypothesis_testing["TS"] ),
                          "accept H0" )

    #@unittest.skip("reason for skipping")
    def test_13_set_rejection_region(self):
        hypothesis_testing = {}
        tail = ">"
        alpha = iml.get_alpha_default(">")
        iml.set_null_hypothesis(hypothesis_testing, 520)
        iml.set_research_hypothesis(hypothesis_testing, tail)
        iml.set_test_statistic(hypothesis_testing, 2.56)
        iml.set_rejection_region(hypothesis_testing, alpha)
        #
        sigma_coeff = iml.get_sigma_coeff( alpha )
        deduction = iml.deduce( tail, sigma_coeff, hypothesis_testing["TS"] )
        compare = "For a probability alpha = "+str(alpha)+" of a type-I error, "+deduction
        #
        self.assertEqual( hypothesis_testing["RR"], compare )

if __name__ == '__main__':
    unittest.main()
