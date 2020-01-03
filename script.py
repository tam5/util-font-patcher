import fontforge
import getopt
import sys

from termcolor import colored
from datetime import datetime

shortOpts = "hi:"
longOpts = ["help", "input="]

try:
    arguments, values = getopt.getopt(sys.argv[1:], shortOpts, longOpts)
except getopt.error as err:
    print(str(err))
    sys.exit(2)

for currentArgument, currentValue in arguments:
    if currentArgument in ("-h", "--help"):
        print("displaying help")
    elif currentArgument in ("-i", "--input"):
        print(("enabling special output mode (%s)") % (currentValue))

print('--- Opening up a file')
print(colored('hello', 'green'))

font = fontforge.open("/home/Arial.ttf")
factor = 1.5


def adjust(font, attribute, factor):
    original = getattr(font, attribute)
    new = int(getattr(font, attribute) * factor)

    print("Adjusting {}: {} -> {}".format(attribute, original, new))
    setattr(font, attribute, new)


props = [
    'os2_winascent',
    'os2_windescent'
    'os2_typoascent',
    'os2_typodescent',
    'hhea_ascent',
    'hhea_descent'
]

for prop in props:
    adjust(font, prop, factor)

# print("Ascent: {}".format(font.ascent))
# print("Descent: {}".format(font.descent))

# print("Win Ascent: {} -> {}".format(font.os2_winascent, 1.1 * font.os2_winascent))
# print("Win Descent: {} -> {}".format(font.os2_windescent, 1.1 * font.os2_windescent))

# print(getattr(font, 'os2_winascent'))
# adjust(font, 'os2_windescent', factor)

# Fontname
font.fontname = "NewFont2"
# Family Name
font.familyname = "NewFont"
# Name For Humans
font.fullname = "NewFont1"
# Copyright
font.copyright = "(c) {} Acme Corp. All Rights Reserved.".format(datetime.now().year)

# font.save("/home/NewFont.ttf")
