import os

import pytest
from lxml import etree

from script2 import compare_gpif_files, decompress_gpif


def test_materialize_gpif():
    score_path = os.path.join('test_data', 'simple_new.gpif')
    tree = etree.parse(score_path)
    master_bars = decompress_gpif(tree, score_path)
    assert len(master_bars) == 2

    assert len(master_bars[0].bars) == 1
    assert len(master_bars[0].bars[0].beats) == 4

    assert len(master_bars[1].bars) == 1
    assert len(master_bars[1].bars[0].beats) == 4

@pytest.mark.skip()
def test_compare_gpif_simple():
    test_data_dir = os.path.join('test_data')
    score_a_path = os.path.join(test_data_dir, 'simple_old.gpif')
    score_b_path = os.path.join(test_data_dir, 'simple_new.gpif')
    x = compare_gpif_files(score_a_path, score_b_path)

    assert x == {1}

def test_compare_gpif_jesus():
    test_data_dir = os.path.join('test_data')
    score_a_path = os.path.join(test_data_dir, 'jesusisalive_old.gpif')
    score_b_path = os.path.join(test_data_dir, 'jesusisalive_new.gpif')
    x = compare_gpif_files(score_a_path, score_b_path)

    x = list(x)
    assert len(x) == 2