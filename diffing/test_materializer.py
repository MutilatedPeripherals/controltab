from lxml import etree

from script2 import compare_gpif_files, decompress_gpif


def test_compare_gpif_files():
    x = compare_gpif_files('./simple/Empty/Content/score.gpif', './simple/Empty2/Content/score.gpif')
    assert x == {1}

def test_decompress_gpif():
    tree = etree.parse('./simple/Empty/Content/score.gpif')
    master_bars = decompress_gpif(tree, './simple/Empty/Content/score.gpif')
    assert len(master_bars) == 2

    assert len(master_bars[0].bars) == 1
    assert len(master_bars[0].bars[0].beats) == 4

    assert len(master_bars[1].bars) == 1
    assert len(master_bars[1].bars[0].beats) == 4
