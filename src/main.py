import os
import fontforge

from termcolor import colored
from datetime import datetime
from parseOpts import parseOpts


def adjust(font, attribute, factor):
    """Adjust an attribute of a font by a given factor."""
    # Get the base metrics we need for calculation
    base_ascent = font.os2_typoascent
    base_descent = font.os2_typodescent
    
    print("\nCalculating adjustment for {}:".format(colored(attribute, 'yellow', attrs=['bold'])))
    print("  Base ascent: {}".format(colored(base_ascent, 'cyan')))
    print("  Base descent: {}".format(colored(base_descent, 'cyan')))
    
    # Calculate the base height
    base_height = base_ascent - base_descent
    print("  Base height: {}".format(colored(base_height, 'cyan')))
    
    # Calculate additional space
    additional_space = base_height * (factor - 1)
    print("  Additional space needed: {}".format(colored(additional_space, 'cyan')))
    print("  Half of additional space: {}".format(colored(additional_space / 2, 'cyan')))
    
    # Get the original value
    original = getattr(font, attribute)
    
    # Determine metric type and whether it uses positive or negative values
    is_ascent = 'ascent' in attribute.lower()
    is_windescent = attribute == 'os2_windescent'
    
    # Calculate new value
    if is_ascent:
        new = int(original + (additional_space / 2))
    else:
        if is_windescent:
            # windescent uses positive values
            new = int(original + (additional_space / 2))
        else:
            # typodescent and hhea_descent use negative values
            new = int(original - (additional_space / 2))

    print("  {} {} -> {}".format(
        "Increasing" if (is_ascent or is_windescent) else "Decreasing",
        colored(original, 'red'),
        colored(new, 'green')
    ))
    
    return new

# Main script
args = parseOpts()
font = fontforge.open(args["input"])

print(colored('\nFont Metrics Adjustment Preview', 'yellow', attrs=['bold']))
print(colored('--------------------------------', 'yellow'))
print("Input file: {}".format(colored(args["input"], 'cyan')))
print("Factor: {}".format(colored(args["factor"], 'cyan')))
print("Mode: {}".format(colored("DRY RUN - No changes will be made" if args["dry_run"] else "LIVE RUN - Font will be modified", 'yellow')))

adjustments = {}
print('')

for prop in ['os2_winascent', 'os2_typoascent', 'hhea_ascent']:
    adjustments[prop] = adjust(font, prop, args["factor"])

for prop in ['os2_windescent', 'os2_typodescent', 'hhea_descent']:
    adjustments[prop] = adjust(font, prop, args["factor"])

if not args["dry_run"]:
    print(colored('\nApplying changes...', 'yellow'))
    for prop, value in adjustments.items():
        setattr(font, prop, value)
        print("  Setting {}: {}".format(colored(prop, 'yellow'), colored(value, 'green')))

    for attr in ['fontname', 'familyname', 'fullname']:
        value = args[attr] or "{} {}".format(getattr(font, attr), args["factor"])
        setattr(font, attr, value)
        print("  Setting {}: {}".format(colored(attr, 'yellow'), colored(value, 'green')))

    font.copyright = "(c) {} Acme Corp. All Rights Reserved.".format(datetime.now().year)

    filename, extension = os.path.splitext(os.path.basename(args["input"]))
    newFileName = "{}Patched {}{}".format(filename, args["factor"], extension)
    print(colored('\nSaving new font as: ', 'yellow') + colored(newFileName, 'green'))
else:
    print(colored('\nDry run complete - no changes were made', 'yellow'))
