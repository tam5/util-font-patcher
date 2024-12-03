import getopt
import sys

from termcolor import colored

shortOpts = "hdi:o:"
longOpts = ["help", "dryDrun", "input=", "outputDir=", "factor="]


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
            args["dry_run"] = True
        elif currentArgument in ("-i", "--input"):
            args["input"] = currentValue
        elif currentArgument in ("-o", "--outputDir"):
            args["outputDir"] = currentValue
        elif currentArgument in ("-f", "--factor"):
            args["factor"] = float(currentValue)

    # Set dry_run to False if not specified
    if "dry_run" not in args:
        args["dry_run"] = False

    for arg in ['factor', 'input', 'outputDir']:
        if arg not in args:
            print(colored("Missing required argument '{}'.".format(arg), 'red'))
            sys.exit(2)

    return args
