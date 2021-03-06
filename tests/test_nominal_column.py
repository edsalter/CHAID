"""
Testing module for the class NominalColumn
"""
from unittest import TestCase
import numpy as np
from numpy import nan
from setup_tests import list_ordered_equal, CHAID


def test_chaid_vector_converts_strings():
    """
    Check that the metadata is correct when NominalColumns are created from
    strings
    """
    arr = np.array(['2', '4'])
    vector = CHAID.NominalColumn(arr)

    assert np.array_equal(vector.arr, np.array([0, 1])), \
        'The indices are correctly substituted'
    assert vector.metadata == {0: '2', 1: '4'}, \
        'The metadata is formed correctly'


def test_chaid_vector_with_ints():
    """
    Check that the metadata is correct when NominalColumns are created from ints
    """
    arr = np.array([1, 2])
    vector = CHAID.NominalColumn(arr)

    assert np.array_equal(vector.arr, np.array([0, 1])), \
        'The indices are correctly substituted'
    assert vector.metadata == {0: 1, 1: 2}, \
        'The metadata is formed correctly'


def test_chaid_vector_with_ints_and_nan():
    """
    Check that the metadata is correct when NominalColumns are created from ints
    """
    arr = np.array([1, 2, np.nan])
    vector = CHAID.NominalColumn(arr)

    assert np.array_equal(vector.arr, np.array([0, 1, -1])), \
        'The indices are correctly substituted'
    assert vector.metadata == {0: 1, 1: 2, -1: '<missing>'}, \
        'The metadata is formed correctly'


def test_chaid_vector_with_floats():
    """
    Check that the metadata is correct when NominalColumns are created from
    floats
    """
    arr = np.array([1.0, 2.0])
    vector = CHAID.NominalColumn(arr)

    assert np.array_equal(vector.arr, np.array([0, 1])), \
        'The indices are correctly substituted'
    assert vector.metadata == {0: 1.0, 1: 2.0}, \
        'The metadata is formed correctly'


def test_chaid_vector_with_floats_and_nan():
    """
    Check that the metadata is correct when NominalColumns are created from
    floats
    """
    arr = np.array([1.0, 2.0, np.nan])
    vector = CHAID.NominalColumn(arr)

    assert np.array_equal(vector.arr, np.array([0, 1, -1])), \
        'The indices are correctly substituted'
    assert vector.metadata == {0: 1.0, 1: 2.0, -1: '<missing>'}, \
        'The metadata is formed correctly'


def test_chaid_vector_with_dtype_object():
    """
    Check that the metadata is correct when NominalColumns are created from
    objects
    """
    arr = np.array([1, 2], dtype="object")
    vector = CHAID.NominalColumn(arr)

    assert np.array_equal(vector.arr, np.array([0, 1])), \
        'The indices are correctly substituted'
    assert vector.metadata == {0: 1, 1: 2}, \
        'The metadata is formed correctly'


def test_chaid_vector_with_dtype_object_and_nans():
    """
    Check that the metadata is correct when NominalColumns are created from
    objects
    """
    arr = np.array([1, 2, np.nan], dtype="object")
    vector = CHAID.NominalColumn(arr)

    assert np.array_equal(vector.arr, np.array([0, 1, -1])), \
        'The indices are correctly substituted'
    assert vector.metadata == {0: 1, 1: 2, -1: '<missing>'}, \
        'The metadata is formed correctly'

def test_column_stores_weights():
    """
    Tests that the columns store the weights when they are passed
    """
    arr = np.array([1.0, 2.0, 3.0])
    wt = np.array([2.0, 1.0, 0.25])
    nominal = CHAID.NominalColumn(arr, weights=wt)
    ordinal = CHAID.OrdinalColumn(arr, weights=wt)
    continuous = CHAID.ContinuousColumn(arr, weights=wt)
    assert (nominal.weights == wt).all()
    assert (ordinal.weights == wt).all()
    assert (continuous.weights == wt).all()

class TestDeepCopy(TestCase):
    """ Test fixture class for deep copy method """
    def setUp(self):
        """ Setup for copy tests"""
        # Use string so numpy array dtype is object and may store references
        arr = np.array(['5.0', '10.0'])
        self.orig = CHAID.NominalColumn(arr)
        self.copy = self.orig.deep_copy()

    def test_deep_copy_does_copy(self):
        """ Ensure a copy actually happens when deep_copy is called """
        assert id(self.orig) != id(self.copy), 'The vector objects must be different'
        assert list_ordered_equal(self.copy, self.orig), 'Vector contents must be the same'

    def test_changing_copy(self):
        """ Test that altering the copy doesn't alter the original """
        self.copy.arr[0] = 55.0
        assert not list_ordered_equal(self.copy, self.orig), 'Altering one vector should not affected the other'

    def test_metadata(self):
        """ Ensure metadata is copied correctly or deep_copy """
        assert self.copy.metadata == self.orig.metadata, 'Copied metadata should be equivilent'
