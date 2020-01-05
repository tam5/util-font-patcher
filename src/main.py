import fontforge
import sys

from termcolor import colored
from datetime import datetime
from parseOpts import parseOpts

args = parseOpts()


def adjust(font, attribute, factor):
    """Adjust an attribute of a font by a given factor."""
    original = getattr(font, attribute)
    new = int(getattr(font, attribute) * factor)

    print("Adjusting {}: {} -> {}".format(
        colored(attribute, 'yellow', attrs=['bold']),
        colored(original, 'red'),
        colored(new, 'green')
    ))
    setattr(font, attribute, new)


font = fontforge.open(args["input"])

props = [
    'os2_winascent',
    'os2_windescent',
    'os2_typoascent',
    'os2_typodescent',
    'hhea_ascent',
    'hhea_descent'
]

print('')
for prop in props:
    adjust(font, prop, args["factor"])

for attr in ['fontname', 'familyname', 'fullname']:
    value = args[attr] or "{} - Patched ({})".format(getattr(font, attr), args["factor"])
    setattr(font, attr, value)

font.copyright = "(c) {} Acme Corp. All Rights Reserved.".format(datetime.now().year)

print('')
print(colored('Successfully created patched font: {}'.format(colored(font.fontname, 'blue')), 'green'))

sys.exit()

# font.save("/home/NewFont.ttf")
