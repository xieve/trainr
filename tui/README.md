# tui
Another Textual User Interface library for and in Python

| Function                  | Description |
| ---                       | ---         |
| `getCh()`                 | Gets a single character from stdin |
| `getKey()`                | Gets a whole keypress from stdin, e.g. arrow keys, even if the representation is longer than one character |
| `editLast(str)`           | Prints a line which can be overwritten wih the same function. **You have to print your final line with `print()` or add `print('')` when you want a new line, or the next thing printed will print in the same line!** |
| `clear()`                 | A os-independent way to clear the screen |
| `dictMenu(dict)`          | Displays a simple horizontal menu made of the keys of dict and returns the corresponding value |
| `progBar(current, total)` | Generates a text progress bar without printing it, best use with `editLast()` |
