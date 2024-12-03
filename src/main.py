import fontforge
import getopt
import os
import sys

from termcolor import colored
from datetime import datetime

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 1)

shortOpts = "hdi:o:"
longOpts = ["help", "dryRun", "input=", "outputDir=", "factor="]

args = {}

try:
    arguments, values = getopt.getopt(sys.argv[1:], shortOpts, longOpts)
except getopt.error as err:
    print(str(err))
    sys.exit(2)

for currentArgument, currentValue in arguments:
    if currentArgument in ("-h", "--help"):
        print('')
        print(colored('Description:', 'yellow'))
        print(colored('    Font patcher to adjust line height by manipulating ascent and descent metrics', 'white'))
        print('')
        print(colored('Usage:', 'yellow'))
        print(colored('    main.py [arguments] [options]', 'white'))
        print('')
        print(colored('Required Arguments:', 'yellow'))
        print(colored('    -f, --factor           The factor by which to adjust the line height, ex: 1.2', 'green'))
        print(colored('    -i, --input            The original font file', 'green'))
        print(colored('    -o, --outputDir        The path to the new font file', 'green'))
        print('')
        print(colored('Options:', 'yellow'))
        print(colored('    -h, --help             Display this help message', 'green'))
        print(colored('    -d, --dryRun           Preview changes without modifying the font', 'green'))
        print('')
        sys.exit(0)
    elif currentArgument in ("-d", "--dryRun"):
        args["dryRun"] = True
    elif currentArgument in ("-i", "--input"):
        args["input"] = currentValue
    elif currentArgument in ("-o", "--outputDir"):
        args["outputDir"] = currentValue
    elif currentArgument in ("-f", "--factor"):
        args["factor"] = float(currentValue)

if "dryRun" not in args:
    args["dryRun"] = False

for arg in ['factor', 'input', 'outputDir']:
    if arg not in args:
        print(colored("Missing required argument '{}'.".format(arg), 'red'))
        sys.exit(2)


#
#
#
#
#
def calculate_padding(base_ascent, base_descent, factor):
    base_height = abs(base_ascent) + abs(base_descent)
    desired_height = base_height * args["factor"]
    padding_to_add = int((desired_height - base_height) / 2)

    print("  Base ascent: {}".format(colored(base_ascent, 'cyan')))
    print("  Base descent: {}".format(colored(base_descent, 'cyan')))
    print("  Base height: {}".format(colored(base_height, 'cyan')))
    print("  Padding to add: {}".format(colored(padding_to_add, 'cyan')))

    return padding_to_add

def print_font_info(font):
    attributes = [
        'fontname', 'familyname', 'fullname', 'copyright',
        'os2_winascent', 'os2_windescent',
        'os2_typoascent', 'os2_typodescent',
        'hhea_ascent', 'hhea_descent'
    ]
    print(colored('Fontname: ', 'white') + colored(font.fontname, 'blue'))
    print(colored('Family Name: ', 'white') + colored(font.familyname, 'blue'))
    print(colored('Name for Humans: ', 'white') + colored(font.fullname, 'blue'))
    # for attr in attributes:
    #     print("    {}: {}".format(colored(attr), colored(getattr(font, attr), 'white')))

print("Running font patcher thing...")

#
#
#
#
#
input_file = args["input"]
print(colored('==>', 'green') + colored(' Reading file: ', 'white', attrs=['bold']) + colored(input_file, 'green'))
font = fontforge.open(input_file)

print(colored('==>', 'blue') + colored(' Reading font info', 'white', attrs=['bold']))
print_font_info(font)

factor = args["factor"]
print(colored('==>', 'green') + colored(' Adjusting ascent and descent by a factor of: ', 'white', attrs=['bold']) + colored(factor, 'green'))

print(colored('==>', 'blue') + colored(' Adjusting OS/2 Windows metrics', 'white', attrs=['bold']))
win_padding = calculate_padding(font.os2_winascent, font.os2_windescent, factor)
font.os2_winascent += win_padding
font.os2_windescent += win_padding

print("> adjusting OS/2 Typography metrics...")
typo_padding = calculate_padding(font.os2_typoascent, font.os2_typodescent, factor)
font.os2_typoascent += typo_padding
font.os2_typodescent -= typo_padding

print("> adjusting hhea metrics...")
hhea_padding = calculate_padding(font.hhea_ascent, font.hhea_descent, factor)
font.hhea_ascent += hhea_padding
font.hhea_descent -= hhea_padding

#
#
#
# modify the font info attributes
#
font.copyright = "(c) {} Acme Corp. All Rights Reserved.".format(datetime.now().year)

for attr in ['fontname', 'familyname', 'fullname']:
    value = args[attr] or "{} {}".format(getattr(font, attr), factor)
    setattr(font, attr, value)

sfnt = {}
for el in font.sfnt_names:
    sfnt[el[1]] = el

sfnt["UniqueID"] = ('English (US)', 'UniqueID', font.fontname)
sfnt["Preferred Family"] = ('English (US)', 'Preferred Family', font.familyname)

font.sfnt_names = tuple(sfnt.values())

# https://learn.microsoft.com/en-us/typography/opentype/spec/hhea
# https://learn.microsoft.com/en-us/typography/opentype/spec/os2#os2-table-and-opentype-font-variations

# print("Mode: {}".format(colored("DRY RUN - No changes will be made" if args["dryRun"] else "LIVE RUN - Font will be modified", 'yellow')))

print_font_info(font)

# if not args["dryRun"]:
#     print(colored('\nApplying changes...', 'yellow'))
#     for prop, value in adjustments.items():
#         setattr(font, prop, value)
#         print("  Setting {}: {}".format(colored(prop, 'yellow'), colored(value, 'green')))

#     for attr in ['fontname', 'familyname', 'fullname']:
#         value = args[attr] or "{} {}".format(getattr(font, attr), args["factor"])
#         setattr(font, attr, value)
#         print("  Setting {}: {}".format(colored(attr, 'yellow'), colored(value, 'green')))

#     font.copyright = "(c) {} Acme Corp. All Rights Reserved.".format(datetime.now().year)

#     filename, extension = os.path.splitext(os.path.basename(args["input"]))
#     newFileName = "{}Patched {}{}".format(filename, args["factor"], extension)
#     print(colored('\nSaving new font as: ', 'yellow') + colored(newFileName, 'green'))
# else:
#     print(colored('\nDry run complete - no changes were made', 'yellow'))
