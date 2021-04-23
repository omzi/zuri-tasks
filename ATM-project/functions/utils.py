import os
import re
from time import sleep
from rich import print
import simplejson as json
from rich.console import Console
console = Console()


def ordinal(n):
    # Add ordinal suffix for the day of the month; i.e. 'st', 'nd', 'rd' or 'th'
    return str(n) + ('th' if 4 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th'))


def saveData(data):
    # Saves a user's bank details to a JSON file
    dataFile = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '\\' + 'data.json'
    open(dataFile, 'w+').write(json.dumps(data))


def printMessage(state, content):
    # Prints a message and styles it based on a specified state
    if state.lower() == 'invalid':
        console.print(f'Error: {content}', style='bold red')
    elif state.lower() == 'valid':
        console.print(content, style='bold green')
    sleep(.75)


def validateInput(question, type, inputEmpty, inputInvalid, inputHidden):
    input = None

    while True:
        input = console.input(f'\n[bold blue]{question}[/bold blue]\n❯❯ ', password = inputHidden)

        if not len(input) or re.match(r'\s', input):
            printMessage('invalid', inputEmpty)
            continue

        if type == str and not isinstance(input, str):
            printMessage('invalid', inputInvalid)
            continue
        elif type == int:
            try:
                input = int(input)
            except ValueError:
                printMessage('invalid', inputInvalid)
                continue
        return input


def exit(data):
    saveData(data)
    print('[bold blue_violet]Thank you for banking with us! Have a nice day :)[/bold blue_violet]')
    quit()

def checkExitIntent(message, data, action, bankOperations, accountNumber):
    isValidOption = True

    while isValidOption:
        option = console.input(f'[bold yellow]{message}[/bold yellow]' + '\n❯❯ ')
      
        if option.upper() == 'Y':
            isValidOption = False
            action(data)
        elif option.upper() == 'N':
            isValidOption = False
            bankOperations(data, accountNumber)
        else:
            printMessage('invalid', 'Invalid option. Reply Y for [Y]es & N for [N]o')
