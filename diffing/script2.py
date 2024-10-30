from lxml import etree
from dataclasses import dataclass, asdict
from typing import List, Set


@dataclass
class Note:
    step: str
    accidental: str
    octave: int
    fret: int
    string: int
    midi: int

@dataclass
class Beat:
    notes: List[Note]
    dynamic: str
    rhythm: str


@dataclass
class Bar:
    clef: str
    beats: List[Beat]


@dataclass
class MasterBar:
    key_accidentals: int
    key_mode: str
    time_sig: str
    bars: List[Bar]


def decompress_gpif(tree, filepath):
    master_bars = []

    # Build lookup tables
    notes_lookup = {note.get('id'): note for note in tree.xpath('//Notes/Note')}
    beats_lookup = {beat.get('id'): beat for beat in tree.xpath('//Beats/Beat')}
    bars_lookup = {bar.get('id'): bar for bar in tree.xpath('//Bars/Bar')}
    voices_lookup = {voice.get('id'): voice for voice in tree.xpath('//Voices/Voice')}

    # Process each MasterBar
    for master_bar in tree.xpath('//MasterBars/MasterBar'):
        # Get bars referenced by this master bar
        bar_ids = master_bar.find('Bars').text.split()
        materialized_bars = []

        for bar_id in bar_ids:
            bar = bars_lookup[bar_id]
            voice_ids = bar.find('Voices').text.split()
            materialized_beats = []

            # Process each voice in the bar
            for voice_id in voice_ids:
                if voice_id == '-1':
                    continue

                voice = voices_lookup[voice_id]
                beat_ids = voice.find('Beats').text.split()

                # Materialize each beat in the voice
                for beat_id in beat_ids:
                    beat = beats_lookup[beat_id]
                    note_ids = beat.find('Notes')
                    if note_ids is not None:
                         note_ids = note_ids.text.split()
                    else:
                        print(f"beat {beat_id} in file {filepath} has no notes!!!")
                        print(beat)
                        continue

                    # Materialize notes in the beat
                    materialized_notes = []
                    for note_id in note_ids:
                        note = notes_lookup[note_id]
                        props = note.findall('.//Property')
                        materialized_note = Note(
                            step=next(prop.find('.//Step').text for prop in props if prop.get('name') == 'ConcertPitch'),
                            accidental=next(prop.find('.//Accidental').text or '' for prop in props if prop.get('name') == 'ConcertPitch'),
                            octave=int(next(prop.find('.//Octave').text for prop in props if prop.get('name') == 'ConcertPitch')),
                            fret=int(next(prop.find('.//Fret').text for prop in props if prop.get('name') == 'Fret')),
                            string=int(next(prop.find('.//String').text for prop in props if prop.get('name') == 'String')),
                            midi=int(next(prop.find('.//Number').text for prop in props if prop.get('name') == 'Midi'))
                        )
                        materialized_notes.append(materialized_note)

                    materialized_beat = Beat(
                        notes=materialized_notes,
                        dynamic=beat.find('Dynamic').text,
                        rhythm=beat.find('Rhythm').get('ref')
                    )
                    materialized_beats.append(materialized_beat)

            materialized_bar = Bar(
                clef=bar.find('Clef').text,
                beats=materialized_beats
            )
            materialized_bars.append(materialized_bar)

        master_bar_obj = MasterBar(
            key_accidentals=int(master_bar.find('.//AccidentalCount').text),
            key_mode=master_bar.find('.//Mode').text,
            time_sig=master_bar.find('.//Time').text,
            bars=materialized_bars
        )
        master_bars.append(master_bar_obj)

    return master_bars


def find_changed_masterbars(old_gpif: List[MasterBar], new_gpif: List[MasterBar]) -> Set[int]:
    changed_indexes = set()

    # First ensure we handle different lengths
    max_length = max(len(old_gpif), len(new_gpif))

    for i in range(max_length):
        # If one file has more master bars than the other, mark as changed
        if i >= len(old_gpif) or i >= len(new_gpif):
            changed_indexes.add(i)
            continue

        old_master = old_gpif[i]
        new_master = new_gpif[i]

        # Convert to dict for easier comparison
        # This handles nested dataclasses automatically
        if asdict(old_master) != asdict(new_master):
            changed_indexes.add(i)

    return changed_indexes


# Usage example:
def compare_gpif_files(old_xml: str, new_xml: str) -> Set[int]:
    old_tree = etree.parse(old_xml)
    new_tree = etree.parse(new_xml)

    old_gpif = decompress_gpif(old_tree, old_xml)
    new_gpif = decompress_gpif(new_tree, new_xml)

    return find_changed_masterbars(old_gpif, new_gpif)


if __name__ == "__main__":
    # tree = etree.parse('./simple/Empty/Content/score.gpif')
    # materialized_score = decompress_gpif(tree)

    #x = compare_gpif_files('./simple/Empty/Content/score.gpif', './simple/Empty2/Content/score.gpif')
    x = compare_gpif_files('./complex/scoreA.gpif', './complex/scoreB.gpif')

    print("Hello")