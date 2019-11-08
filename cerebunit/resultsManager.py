# ~/cerebtests/cerebunit/resultsManager.py
import h5py   # to create HDF5 file
import numpy  # to create string (Fixed-length ASCII) dataset
import ast    # to convert string to dictionary for reading

class ResultsManager(object):

    def __init__(self):
        pass

    @staticmethod
    def create_file( vtest ):
        filename = type(vtest).__name__
        return h5py.File( filename, "w" )

    @staticmethod
    def save_test_statistic( hdf5file = None, desired_model = None,
                             test_statistic = None ):
        #
        dset = hdf5file.create_dataset( desired_model.modelname, (1,), dtype="f" )
        dset[0] = test_statistic.score
        #
        dset.attrs["description"] = numpy.string_( test_statistic.description )
        dset.attrs["statistics"] = numpy.string_( test_statistic.statistics )

    @staticmethod
    def read_file( vtest ):
        try: # vtest IS ACTUALLY a cerebunit test (class instance)
            filename = type(vtest).__name__
        except: # otherwise it is the name of the desired filename
            filename = vtest
        return h5py.File( filename, "r" )

    #@staticmethod
    #def visualize_scores
