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

# font = fontforge.open("/home/Arial.ttf")

# print(font.familyname)

# # font.fontname = "NewFont"
# # font.familyname =
# # font.save("/home/NewFont.ttf")

# # Fontname
# font.fontname = "NewFont2"
# # Family Name
# font.familyname = "NewFont"
# # Name For Humans
# font.fullname = "NewFont1"
# # Copyright
# font.copyright = "(c) {} Acme Corp. All Rights Reserved.".format(datetime.now().year)

# font.save("/home/NewFont.ttf")
