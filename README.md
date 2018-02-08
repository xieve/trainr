# trainr
The first terminal-based vocabulary trainer.

## Requirements
Trainr uses [TUI](https://github.com/xieve/tui/), a little module for textual user interfaces I wrote myself.

## Configuration
Trainr can be configurated very little at the moment, but that'll change soon. Until now you can (and **must**) set only one param: `languages`.
Values are semicolon-separated. E.g.
```trainr.conf
languages = german; french
```

## TODO
- An extra phase with words that aren't yet needed \(\-1)
- Automatic incremental activation for those words
- More configuration possibilities
