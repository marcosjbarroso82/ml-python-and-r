import pytest
from .json_helpers import json_set_nested_value

def test_setSimpleNestedValue():
    instance = {}
    expected_instance = {'arr': ['v']}
    
    path = ['arr', 0]
    value = 'v'
    
    instance = json_set_nested_value(instance, value, path)
    
    assert expected_instance == instance
    


def test_setDoubleNestedValue():
    instance = {}
    expected_instance = {'arr': ['v']}
    
    path = ['arr', 0]
    value = 'v'
    
    instance = json_set_nested_value(instance, value, path)
    
    assert expected_instance == instance