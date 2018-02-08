import sys, os

# Replace certain char in string
def strInsert(str, char, pos):
    parts = list()
    parts.append(str[:pos])
    parts.append(str[pos + 1:])
    return parts[0] + char + parts[1]

# Find the right getCh() and getKey() implementations
try:
    # POSIX system: Create and return a getCh that manipulates the tty
    import termios
    import sys, tty
    def getCh():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

    # Read arrow keys correctly
    def getKey():
        firstChar = getCh()
        if firstChar == '\x1b':
            return {"[A": "up", "[B": "down", "[C": "right", "[D": "left"}[getCh() + getCh()]
        else:
            return firstChar

except ImportError:
    # Non-POSIX: Return msvcrt's (Windows') getCh
    import msvcrt
    getCh = msvcrt.getch

    # Read arrow keys correctly
    def getKey():
        firstChar = getCh()
        if firstChar == b'\xe0':
            return {"H": "up", "P": "down", "M": "right", "K": "left"}[getCh()]
        else:
            return firstChar

# Edits last line by printing \r without \n
def editLast(out):
    sys.stdout.write('\r' + out)
    sys.stdout.flush()

# Clear screen
def clear(): os.system("cls" if os.name == "nt" else "clear")

# Minimalistic arrow-key-controlled menu to select an object from a dict
def dictMenu(itms):
    menuStr = ''
    curItem = 0
    itmList = []
    for key in itms.keys():
        itmList.append(key)
        menuStr += "  " + key
    editLast(strInsert(strInsert(menuStr, '>', 1), '<', len(itmList[0]) + 2) + " ")
    while True:
        pos = 0
        c = getKey()
        if c == "left":
            if curItem > 0: curItem -= 1
        elif c == "right":
            if len(itmList) > curItem + 1: curItem += 1
        elif c == b'\r' or c == '\r':
            print('')
            return itms[itmList[curItem]]
        for item in itmList[0:curItem]:
            pos += 2 + len(item)
        editLast(strInsert(strInsert(menuStr, '>', pos + 1), '<', pos + len(itmList[curItem]) + 2) + ' ')

# Generate a text progress bar
def progBar(current, total):
    return '[' + '#' * current + '-' * (total - current) + ']'
