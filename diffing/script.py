from typing import List, Dict

from lxml import etree
from lxml.etree import Element

tree = etree.parse('./simple/Empty/Content/score.gpif')


def beats_from_notes(note_ids: List[str]) -> Dict[str, Element]:
    results = {}

    beats = tree.xpath('//Beat')
    for beat in beats:
        notes = beat.find('Notes').text.split()
        for note_id in note_ids:
            if note_id in notes:
                results[beat.attrib["id"]] = beat

    return results


result = beats_from_notes(["2", "3"])

print("Hello")
