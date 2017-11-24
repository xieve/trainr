# trainr
The first terminal-based vocabulary trainer.

## Configuration
Trainr can be configurated very little at the moment, but that'll change soon. Until now you can (and **must**) set only one param: `languages`.
Values are semicolon-separated. E.g.
```trainr.conf
languages = german; french
```
For each language you **must create an empty file named "<language>.csv"** where <language> has to be replaced by the language's name.

## TODO
- Automatic creation of csv-files and config
- An extra phase with words that aren't yet needed \(\-\1)
- Automatic incremental activation for those words
- More configuration possibilities
