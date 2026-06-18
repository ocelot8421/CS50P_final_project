"""
$ pytest test_calculator.py
"""

import pytest
from project import preshow_delete_node

def test_delete_node():
    """Test some pisitive number"""
    assert preshow_delete_node(2) == 4