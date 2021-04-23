# Register
# - first name, last name, email address & password
# - Generate user account number & ID
# - Generate account number and BVN

# Login
# - Account number & password

# Bank Operations

import os
import uuid
import random
from time import sleep
from rich import print
import simplejson as json
from functions import bank
from functions import utils
from datetime import datetime
from rich.console import Console


console = Console()
dataFile = os.path.dirname(os.path.realpath(__file__)) + '\\' + 'data.json'

def init():
    data = {  }
    # Loads data from the budget.json file & creates a new one if non-existent
    if os.path.isfile(dataFile) and os.stat(dataFile).st_size != 0:
        savedData = open(dataFile, 'r+')
        data = json.loads(savedData.read())
    else:
        open(dataFile, 'w+').write(json.dumps(data))


    print('[bold purple]♦♦♦ Welcome To Pearl Bank ♦♦♦\n[/bold purple]')
    
    isValidOption = False
    while not isValidOption:
        haveAccount = console.input('[?] Do you have an account? ([Y]es / [N]o)\n❯❯ ')
    
        if haveAccount.lower() == 'y':
            isValidOption = True
            login(data)
        elif haveAccount.lower() == 'n':
            isValidOption = True
            register(data)
        else:
            utils.printMessage('invalid', 'Invalid option selected! \n')
            continue


def login(data):
    print('[bold purple]\n⚞| Login To Your Account ][/bold purple]')

    isLoginSuccessful = False

    while not isLoginSuccessful:
        accountNumberFromUser = utils.validateInput('Enter your account number:', int, 'Account number cannot be blank!', 'Invalid account number provided!', False)
        password = utils.validateInput('Enter your password:', str, 'Password cannot be blank!', 'Invalid password provided!', True)
                                
        for accountNumber, userDetails in data.items():
            if int(accountNumber) == accountNumberFromUser:
                if userDetails['password'] == password:
                    isLoginSuccessful = True
                    print(f"[bold purple]\nHi, {data[accountNumber]['firstName']}![/bold purple]")
                    bankOperations(data, accountNumber)
        utils.printMessage('invalid', 'Invalid user credentials!')
        continue


def register(data):
    print('[bold purple]⚞| Create A New Account ][/bold purple]')
    firstName = utils.validateInput('Hello there! Enter your first name:', str, 'First name cannot be blank!', 'Invalid first name provided!', False)
    lastName = utils.validateInput('Enter your last name:', str, 'Last name cannot be blank!', 'Invalid last name provided!', False)
    emailAddress = utils.validateInput('Enter your email address:', str, 'Email address cannot be blank!', 'Invalid email address provided!', False)
    password = utils.validateInput('Enter a unique password:', str, 'Password cannot be blank!', 'Invalid password provided!', True)

    accountNumber = bank.generateAccountNumber()
    BVN = bank.generateBVN()
    currentDateTime = datetime.now()
    currentDate = datetime.now().strftime('{d} %b, %Y').replace("{d}", utils.ordinal(currentDateTime.day))
    
    data[accountNumber] = { 'userId': str(uuid.uuid4()), 'accountNumber': accountNumber, 'firstName': firstName, 'lastName': lastName, 'emailAddress': emailAddress, 'password': password, 'balance': 0, 'BVN': BVN, 'dateRegistered': currentDate }
    utils.saveData(data)

    print('Account created successfully! Here are your details:')
    print(f'➵  Account Number: {accountNumber}')
    print(f'➵  BVN: {BVN}')
    print('➵  Password: [dim blue]Your chosen password[/dim blue]')
    console.print('[bold yellow]** Tip: Ensure to store your details safely.[/bold yellow]')
    login(data)


def bankOperations(userData, accountNumber):
    utils.saveData(userData)

    currentDateTime = datetime.now()
    print("DATE:", currentDateTime.strftime("{d} %b, %Y").replace("{d}", utils.ordinal(currentDateTime.day)), end=' / ')
    print("TIME:", currentDateTime.strftime("%I:%M:%S %p"))

    print("\n[bold purple]What would you like to do today?[/bold purple]")
    action = getAction()
    
    if action == 1:
        bank.withdraw(bankOperations, accountNumber, userData)
    elif action == 2:
        bank.deposit(bankOperations, accountNumber, userData)
    elif action == 3:
        bank.balanceEnquiry(bankOperations, accountNumber, userData)
    elif action == 4:
        bank.userProfile(bankOperations, accountNumber, userData)
    elif action == 5:
        bank.about(bankOperations, accountNumber, userData)
    elif action == 6:
        utils.checkExitIntent('\nAre you sure you want to sign out? ([Y]es / [N]o)', userData, login, bankOperations, accountNumber)
    elif action == 7:
        utils.checkExitIntent('\nAre you sure you want to exit? ([Y]es / [N]o)', userData, utils.exit, bankOperations, accountNumber)


def getAction():
    # Shows the list of possible options to a user and returns the chosen option
    i = 1; actions = ['Withdraw', 'Deposit', 'Balance Enquiry', 'View Profile', 'About', 'Sign Out', 'Exit']
    print('═' * (len(max(actions, key=len)) + 3))

    for action in actions:
        print(f'[bold]{i}. [cyan]{action}[/cyan][/bold]')
        sleep(.1)
        i += 1

    while True:
        action = int(utils.validateInput('Select an option:', int, 'Option cannot be empty!', 'Enter a valid option!', False))
        if action < 1 or action > len(actions):
            utils.printMessage('invalid', 'Enter a valid option!')
            continue
        else:
            break

    return action


init()
