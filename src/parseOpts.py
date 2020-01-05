import getopt
import sys

from termcolor import colored

shortOpts = "hi:o:f:"
longOpts = ["help", "input=", "output=", "factor=", "fontname=", "familyname=", "fullname="]


def parseOpts():
    """Parses, validates, and handles all script input arguments."""
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
            print(colored('    Font patcher to add line height to fonts', 'white'))
            print('')
            print(colored('Usage:', 'yellow'))
            print(colored('    main.py [arguments] [options]', 'white'))
            print('')
            print(colored('Required Arguments:', 'yellow'))
            print(colored('    -f, --factor           The factor by which to multiply the line height', 'green'))
            print(colored('    -i, --input            The original font file', 'green'))
            print(colored('    -o, --output           The path to the new font file', 'green'))
            print('')
            print(colored('Options:', 'yellow'))
            print(colored('    -h, --help             Display this help message', 'green'))
            print(colored('        --fontname         The name of the patched font', 'green'))
            print(colored('        --familyname       The family name of the patched font', 'green'))
            print(colored('        --fullname         The name for humans of the patched font', 'green'))
            print('')
            sys.exit(0)
        elif currentArgument in ("-i", "--input"):
            args["input"] = currentValue
        elif currentArgument in ("-o", "--output"):
            args["output"] = currentValue
        elif currentArgument in ("-f", "--factor"):
            args["factor"] = float(currentValue)
        elif currentArgument in ("--fontname", "--fullname", "--familyname"):
            args[currentArgument.strip('--')] = currentValue

    for arg in ['factor', 'input', 'output']:
        if arg not in args:
            print(colored("Missing required argument '{}'.".format(arg), 'red'))

    for option in ['fontname', 'familyname', 'fullname']:
        args[option] = args[option] if option in args else None

    if len(args) != 6:
        sys.exit(2)

    return args
