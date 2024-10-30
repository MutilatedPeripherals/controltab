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


def voices_from_beats(beats: Dict[str, Element]) -> Dict[str, Element]:
    results = {}

    voices = tree.xpath('//Voice')
    for voice in voices:
        voice_beat_ids = voice.find('Beats').text.split()
        beat_ids = beats.keys()
        for beat_id in beat_ids:
            if beat_id in voice_beat_ids:
                results[voice.attrib["id"]] = voice

    return results

beats = beats_from_notes(["3"]) # 2 beats
voices = voices_from_beats(beats)

print("Hello")
