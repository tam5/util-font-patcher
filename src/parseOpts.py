import getopt
import sys

from termcolor import colored

shortOpts = "hi:o:f:d"
longOpts = ["help", "input=", "outputDir=", "factor=", "fontname=", "familyname=", "fullname=", "dry-run"]


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
            print(colored('    -f, --factor           The factor by which to adjust the line height', 'green'))
            print(colored('    -i, --input            The original font file', 'green'))
            print(colored('    -o, --outputDir        The path to the new font file', 'green'))
            print('')
            print(colored('Options:', 'yellow'))
            print(colored('    -h, --help             Display this help message', 'green'))
            print(colored('    -d, --dry-run          Preview changes without modifying the font', 'green'))
            print(colored('        --fontname         The name of the patched font', 'green'))
            print(colored('        --familyname       The family name of the patched font', 'green'))
            print(colored('        --fullname         The name for humans of the patched font', 'green'))
            print('')
            sys.exit(0)
        elif currentArgument in ("-d", "--dry-run"):
            args["dry_run"] = True
        elif currentArgument in ("-i", "--input"):
            args["input"] = currentValue
        elif currentArgument in ("-o", "--outputDir"):
            args["outputDir"] = currentValue
        elif currentArgument in ("-f", "--factor"):
            args["factor"] = float(currentValue)
        elif currentArgument in ("--fontname", "--fullname", "--familyname"):
            args[currentArgument.strip('--')] = currentValue

    # Set dry_run to False if not specified
    if "dry_run" not in args:
        args["dry_run"] = False

    for arg in ['factor', 'input', 'outputDir']:
        if arg not in args:
            print(colored("Missing required argument '{}'.".format(arg), 'red'))

    for option in ['fontname', 'familyname', 'fullname']:
        args[option] = args[option] if option in args else None

    if len(args) != 7:  # Updated to account for dry_run
        sys.exit(2)

    return args
