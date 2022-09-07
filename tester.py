'''
# Import the library
import argparse
# Create the parser
parser = argparse.ArgumentParser()
# Add an argument
parser.add_argument('--name', type=str, required=True)
# Parse the argument
args = parser.parse_args()
# Print "Hello" + the user input argument
print('Hello,', args.name)

'''

import shlex
argString = '-vvvv -c "yes" --foo bar --some_flag'
args = parser.parse_args(shlex.split(argString))