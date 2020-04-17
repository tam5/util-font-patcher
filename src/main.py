import os
import fontforge

from termcolor import colored
from datetime import datetime
from parseOpts import parseOpts


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


args = parseOpts()
font = fontforge.open(args["input"])

print('')
for prop in ['os2_winascent', 'os2_typoascent', 'hhea_ascent']:
    adjust(font, prop, args["factor"])

for prop in ['os2_windescent', 'os2_typodescent', 'hhea_descent']:
    adjust(font, prop, args["factor"] * 2)

for attr in ['fontname', 'familyname', 'fullname']:
    value = args[attr] or "{} {}".format(getattr(font, attr), args["factor"])
    setattr(font, attr, value)

font.copyright = "(c) {} Acme Corp. All Rights Reserved.".format(datetime.now().year)

filename, extension = os.path.splitext(os.path.basename(args["input"]))
newFileName = "{}Patched {}{}".format(filename, args["factor"], extension)

print('')
print(colored('Successfully created patched font:', 'green'))
print(colored('                         Fontname: ', 'white', attrs=["bold"]) + colored(font.fontname, 'blue'))
print(colored('                      Family Name: ', 'white', attrs=["bold"]) + colored(font.familyname, 'blue'))
print(colored('                  Name for Humans: ', 'white', attrs=["bold"]) + colored(font.fullname, 'blue'))
print('')

sfnt = {}
for el in font.sfnt_names:
    sfnt[el[1]] = el

sfnt["UniqueID"] = ('English (US)', 'UniqueID', font.fontname)
sfnt["Preferred Family"] = ('English (US)', 'Preferred Family', font.familyname)

font.sfnt_names = tuple(sfnt.values())

font.save(args["outputDir"] + "/" + newFileName)
font.generate(args["outputDir"] + "/" + newFileName)

print(colored('Saved patched font file: {}'.format(colored(newFileName, 'blue')), 'green'))
