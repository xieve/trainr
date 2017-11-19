#!/usr/bin/python3

import os, sys, time, random

class _word:
  def __init__(self, question, answer, phase=0, dueDate=0):
    self.question = question
    self.answer = answer
    self.phase = phase
    self.dueDate = dueDate

class _language:
  name = ''
  words = dict()
  def __init__(self, name):
    self.name = name
  def read(self):
    print("Reading " + self.name + " database...")
    dbFile = open(self.name + ".csv", 'r', encoding="utf-8")
    dbRaw = dbFile.read().splitlines()
    for line in dbRaw:
      if line == '':
        continue
      tmpLst = line.split(';')
      # Import words in the right fields of the _word (question, answer, phase, dueDate)
      self.words[tmpLst[0]] = _word(tmpLst[0], tmpLst[1], int(tmpLst[2]), int(tmpLst[3]))
    dbFile.close()
    del dbRaw
  def save(self):
    outFile = open(self.name + ".csv", 'w', encoding="utf-8")
    for word in self.words.values():
      outFile.write(word.question + ";" + word.answer + ";" + str(word.phase) + ";" + str(word.dueDate) + '\n')
      
# Find the right getch() implementation
try:
  # POSIX system. Create and return a getch that manipulates the tty.
  import termios
  import sys, tty
  def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
      tty.setraw(fd)
      ch = sys.stdin.read(1)
    finally:
      termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
except ImportError:
  # Non-POSIX. Return msvcrt's (Windows') getch.
  import msvcrt
  getch = msvcrt.getch

# Read arrow keys correctly
def getKey():
  firstChar = getch()
  if firstChar == b'\xe0':
    return firstChar + getch()
  else:
    return firstChar

# Replace certain char in string
def strInsert(str, char, pos):
  parts = list()
  parts.append(str[:pos])
  parts.append(str[pos + 1:])
  return parts[0] + char + parts[1]

# Edits last line by printing \r without \n
def editLast(out):
  sys.stdout.write('\r' + out)
  sys.stdout.flush()

# Clear screen
def clear(): os.system('cls' if os.name == 'nt' else 'clear')

# Minimalistic arrow-key-controlled menu to select an object from a dict
def dictMenu(itms):
  menuStr = ''
  curItem = 0
  itmList = list()
  for key in itms.keys():
    itmList.append(key)
    menuStr += "  " + key
  editLast(strInsert(strInsert(menuStr, '>', 1), '<', len(itmList[0]) + 2))
  while True:
    pos = 0
    c = getKey()
    if c == b'\xe0K':
      curItem -= 1
    elif c == b'\xe0M':
      curItem += 1
    elif c == b'\r':
      print('')
      return itms[itmList[curItem]]
    for item in itmList[0:curItem]:
      pos += len(itmList[curItem])
    editLast(strInsert(strInsert(menuStr, '>', pos + curItem * 2 + 1), '<', pos + len(itmList[curItem]) + 2 * (curItem + 1)) + ' ')

# Generate a text progress bar
def progBar(current, total):
  return '[' + '#' * current + '-' * (total - current) + ']'

phaseToTime = [86400, 259200, 864000, 2592000, 7776000, 0]
db = {}
  
random.seed()

# Read and parse config file
clear()
print("Reading config file...")
configFile = open("trainr.conf", 'r', encoding="utf-8")
configRaw = configFile.read().splitlines()
config = dict()
for line in configRaw:
  tmpLst = line.split('=', 1)
  for i, v in enumerate(tmpLst):
    tmpLst[i] = v.strip()
  config[tmpLst[0]] = tmpLst[1]
configFile.close()
del configRaw

# Parse language configs
try:
  for language in config["languages"].split(';'):
    db[language.strip()] = _language(language.strip())
except KeyError:
  print("Oops... No languages found.")
  quit()

print("Choose language:")
language = dictMenu(db)
language.read()

clear()
print("Learn or add words?")
cmd = input("> ")
if cmd == 'l' or cmd == "learn":
  clear()
  print("Preparing...")
  dueWords = [[],[],[],[],[],[]]
  for word in language.words.values():
    if word.dueDate <= int(time.time()):
      dueWords[word.phase].append(word)
  clear()
  for i in range(20):
    print(progBar(i, 20) + ' (' + str(i) + '/20)')
    for i2 in range(5):
      try:
        wordIdx, word = random.choice(list(enumerate(dueWords[i2])))
      except IndexError:
        continue
      print(word.question)
      givenAnswer = input("> ")
      if givenAnswer == word.answer:
        print("Right. \"" + word.question + "\" is now in phase " + str(word.phase + 1) + '.')
        del dueWords[i2][wordIdx]
        language.words[word.question].phase += 1
        language.words[word.question].dueDate = int(time.time()) + phaseToTime[language.words[word.question].phase]
      else:
        if word.phase == 0:
          print("Wrong. \"" + word.question + "\" stays in phase 0. Try again:")
        else:
          print("Wrong. \"" + word.question + "\" is now in phase " + str(word.phase - 1) + ". Try again:")
          language.words[word.question].phase -= 1
        print("Right answer: " + word.answer)
        while True:
          givenAnswer = input("> ")
          if givenAnswer == word.answer:
            break
          else:
            print("Try again.")
      input()
      language.save()
      break
    clear()


elif cmd == 'a' or cmd == "add":
  while True:
    clear()
    print("Question:")
    givenQuestion = input("> ")
    if givenQuestion == 'q':
      break
    print("Answer:")
    givenAnswer = input("> ")
    db[givenQuestion] = _word(givenQuestion, givenAnswer)
    save(db)
  