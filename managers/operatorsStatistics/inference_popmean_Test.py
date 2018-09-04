# ~/managers/operatorsStatistics/inference_popmean_Test.py
import unittest

from inference_popmean import InferencePopMean as infer

from scipy import stats

class InferencePopMeanTest(unittest.TestCase):

    def setUp(self):
        self.hypothesis_testing = {}

    #@unittest.skip("reason for skipping")
    def test_1_set_null_hypothesis(self):
        hypothesis_testing = {}
        infer.set_null_hypothesis(hypothesis_testing, 25)
        self.assertEqual( hypothesis_testing["H0"], {"mu0": 25} )

    #@unittest.skip("reason for skipping")
    def test_2_set_null_hypothesis_modify(self):
        hypothesis_testing = {"H0": {"mu": 25}}
        infer.set_null_hypothesis(hypothesis_testing, 520)
        self.assertEqual( hypothesis_testing["H0"]["mu0"], 520 )

    #@unittest.skip("reason for skipping")
    def test_3_set_research_hypothesis_error(self):
        hypothesis_testing = {}
        self.assertRaises( ValueError,
                           infer.set_research_hypothesis,
                           hypothesis_testing, ">" )

    #@unittest.skip("reason for skipping")
    def test_4_set_research_hypothesis(self):
        hypothesis_testing = {}
        infer.set_null_hypothesis(hypothesis_testing, 520)
        infer.set_research_hypothesis(hypothesis_testing, "=")
        self.assertEqual( hypothesis_testing["Ha"], {"mu": "=520"} )

    #@unittest.skip("reason for skipping")
    def test_5_set_research_hypothesis_modify(self):
        hypothesis_testing = {}
        infer.set_null_hypothesis(hypothesis_testing, 520)
        infer.set_research_hypothesis(hypothesis_testing, "=")
        infer.set_research_hypothesis(hypothesis_testing, ">")
        self.assertEqual( hypothesis_testing["Ha"], {"mu": ">520"} )

    #@unittest.skip("reason for skipping")
    def test_6_set_test_statistic_error(self):
        hypothesis_testing = {}
        self.assertRaises( ValueError,
                           infer.set_test_statistic,
                           hypothesis_testing, 2.56 )

    #@unittest.skip("reason for skipping")
    def test_7_set_test_statistic(self):
        hypothesis_testing = {}
        infer.set_null_hypothesis(hypothesis_testing, 520)
        infer.set_research_hypothesis(hypothesis_testing, ">")
        infer.set_test_statistic(hypothesis_testing, {"z-score": 1.56})
        self.assertEqual( hypothesis_testing["TS"].values()[0], 1.56 )

    #@unittest.skip("reason for skipping")
    def test_8_set_test_statistic_modify(self):
        hypothesis_testing = {}
        infer.set_null_hypothesis(hypothesis_testing, 520)
        infer.set_research_hypothesis(hypothesis_testing, ">")
        infer.set_test_statistic(hypothesis_testing, {"z-score": 1.56})
        infer.set_test_statistic(hypothesis_testing, {"z-score": 2.56})
        self.assertEqual( hypothesis_testing["TS"].values()[0], 2.56 )

    #@unittest.skip("reason for skipping")
    def test_9_get_pvalue_zstat(self):
        hypothesis_testing = {}
        infer.set_null_hypothesis(hypothesis_testing, 520)
        infer.set_research_hypothesis(hypothesis_testing, ">")
        infer.set_test_statistic(hypothesis_testing, {"z-score": 2.56})
        x1 = infer.get_pvalue_zstat(hypothesis_testing)
        #
        infer.set_research_hypothesis(hypothesis_testing, "<")
        x2 = infer.get_pvalue_zstat(hypothesis_testing)
        #
        infer.set_research_hypothesis(hypothesis_testing, "=")
        x3 = infer.get_pvalue_zstat(hypothesis_testing)
        #
        c1 = stats.norm.sf( 2.56 )
        c2 = c1
        c3 = 2*stats.norm.sf( 2.56 )
        self.assertEqual( [x1, x2, x3], [c1, c2, c3] )

    #@unittest.skip("reason for skipping")
    def test_10_get_pvalue_tstat(self):
        hypothesis_testing = {}
        infer.set_null_hypothesis(hypothesis_testing, 42)
        infer.set_research_hypothesis(hypothesis_testing, "<")
        infer.set_test_statistic(hypothesis_testing, {"t-score": -0.88, "sample-size": 10})
        x1 = infer.get_pvalue_tstat(hypothesis_testing)
        #
        infer.set_research_hypothesis(hypothesis_testing, ">")
        x2 = infer.get_pvalue_tstat(hypothesis_testing)
        #
        infer.set_research_hypothesis(hypothesis_testing, "=")
        x3 = infer.get_pvalue_tstat(hypothesis_testing)
        #
        c1 = stats.norm.sf( abs(-0.88), 10-1 )
        c2 = c1
        c3 = 2*stats.norm.sf( abs(-0.99), 10-1 )
        self.assertEqual( [round(x1, 5), round(x2, 5), round(x3, 5)],
                          [round(c1, 5), round(c2, 5), round(c3, 5)] )

    #@unittest.skip("reason for skipping")
    def test_11_get_pvalue(self):
        hypothesis_testing = {}
        infer.set_null_hypothesis(hypothesis_testing, 520)
        infer.set_research_hypothesis(hypothesis_testing, ">")
        infer.set_test_statistic(hypothesis_testing, {"z-score": 2.56})
        x1 = infer.get_pvalue(hypothesis_testing)
        #
        infer.set_research_hypothesis(hypothesis_testing, "<")
        x2 = infer.get_pvalue(hypothesis_testing)
        #
        infer.set_research_hypothesis(hypothesis_testing, "=")
        x3 = infer.get_pvalue(hypothesis_testing)
        #
        c1 = stats.norm.sf( 2.56 )
        c2 = c1
        c3 = 2*stats.norm.sf( 2.56 )
        self.assertEqual( [x1, x2, x3], [c1, c2, c3] )

    #@unittest.skip("reason for skipping")
    def test_12_get_pdescription(self):
        hypothesis_testing = {}
        infer.set_null_hypothesis(hypothesis_testing, 380)
        infer.set_research_hypothesis(hypothesis_testing, ">")
        infer.set_test_statistic(hypothesis_testing, {"z-score": 2.01})
        hypothesis_testing.update( {"p-value": 0.0222} )
        desc = infer.get_pdescription(hypothesis_testing)
        self.assertEqual( type(desc), str )

    #@unittest.skip("reason for skipping")
    def test_13_set_pvalue(self):
        hypothesis_testing = {}
        infer.set_null_hypothesis(hypothesis_testing, 380)
        infer.set_research_hypothesis(hypothesis_testing, ">")
        infer.set_test_statistic(hypothesis_testing, {"z-score": 2.01})
        infer.set_pvalue(hypothesis_testing)
        pval = hypothesis_testing["p-value"]
        desc = hypothesis_testing["p-description"]
        self.assertEqual( [round(pval,4), type(desc)], [0.0222, str] )

    #@unittest.skip("reason for skipping")
    def test_14_deduce(self):
        hypothesis_testing = {}
        infer.set_null_hypothesis(hypothesis_testing, 380)
        infer.set_research_hypothesis(hypothesis_testing, ">")
        infer.set_test_statistic(hypothesis_testing, {"z-score": 2.01})
        infer.set_pvalue(hypothesis_testing) # p-value = 0.022
        deduce1 = infer.deduce(hypothesis_testing, 0.05)
        deduce2 = infer.deduce(hypothesis_testing, 0.01)
        a = "accept Ha" in deduce1
        b = "not enough evidence to reject H0" in deduce2
        self.assertTrue( a and b is True )

    #@unittest.skip("reason for skipping")
    def test_15_set_conclusion(self):
        hypothesis_testing = {}
        infer.set_null_hypothesis(hypothesis_testing, 380)
        infer.set_research_hypothesis(hypothesis_testing, ">")
        infer.set_test_statistic(hypothesis_testing, {"z-score": 2.01})
        infer.set_pvalue(hypothesis_testing) # p-value = 0.022
        infer.set_conclusion(hypothesis_testing, 0.05)
        #
        conc = hypothesis_testing["Fin"]
        a = "type-I error" in conc
        b = "accept Ha" in conc
        #
        self.assertTrue( a and b is True )

if __name__ == '__main__':
    unittest.main()
