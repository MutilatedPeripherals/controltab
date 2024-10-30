# controltab

OR

- [X] get text represenation of tabs -> unzip gp (guitarpro7) -> Content/score.gpif
- [X] repackage to .gp file after changing the .gpif file. in the folder which contains the `VERSION` and `Content` we run `zip -r new.gp ./*`
- [ ] given a line number in a gpif file, output a Bar(notes: Note[]) structure.
    - Score > Track > Staff > Bar > Voice > Beat > Note
    - def noteIdFromLineNumber(lineNumber: number): number
    - now parse the full bars to notes
    - and somewhere take the note id and get only the relevant bar or whatever

* Given a note id (3), find corresponding beat with <Notes> containing the note id
* find the voice by the beat
* find the bar by the voice

THEN

- [ ] diff 2 xml files
- [ ] recognize bar(s) from the diff
- [ ] extract the bars to a nex xml file
- [ ] transform new xmls to guitar pro
- [ ] transfer guitar pro to js visualization lib

nice to have
- [ ] paint notes?