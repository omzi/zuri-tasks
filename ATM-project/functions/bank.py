import sys
import random
from . import utils
from time import sleep
from rich import print
from datetime import datetime
from rich.console import Console
console = Console()


def generateAccountNumber():
    initials = [901, 902, 903, 904, 905]
    accountNumberPrefix = initials[random.randrange(0, len(initials))]
    accountNumber = f'{accountNumberPrefix}{random.randrange(1111111, 9999999)}'

    return int(accountNumber)


def generateBVN():
    initials = [i for i in range(10) if not i == 0]
    BVNPrefix = initials[random.randrange(0, len(initials))]
    BVN = f'{BVNPrefix}{random.randrange(1111111111, 9999999999)}'

    return int(BVN)


def withdraw(bankOperations, accountNumber, user):
    print('[bold purple]\n⚞| Withdrawal ][/bold purple]')

    while True:
        withdrawalAmount = utils.validateInput('How much would you like to withdraw?', int, 'Amount cannot be blank!', 'Invalid amount provided!', False)
        balance = user[accountNumber]['balance']

        if balance == 0:
            utils.printMessage('invalid', 'Your balance is ₦0. Please make a deposit before you can withdraw.')
            break
        elif withdrawalAmount > balance:
            utils.printMessage('invalid', f'Insufficient funds :(. Enter an amount less than ₦{balance}.')
            continue
        else:
            user[accountNumber]['balance'] -= withdrawalAmount
            utils.printMessage('valid', f"Transaction successful! You just withdrew ₦{withdrawalAmount} & your balance is ₦{user[accountNumber]['balance']} \n")
            break
    utils.checkExitIntent('Do you want to terminate this session? ([Y]es / [N]o)', user, utils.exit, bankOperations, accountNumber)


def deposit(bankOperations, accountNumber, user):
    print('[bold purple]\n⚞| Deposit ][/bold purple]')

    while True:
        depositAmount = utils.validateInput('How much would you like to deposit?', int, 'Amount cannot be blank!', 'Invalid amount provided!', False)

        if depositAmount > 0:
            user[accountNumber]['balance'] += depositAmount
            utils.printMessage('valid', f"Money deposited successfully! Your current balance is ₦{user[accountNumber]['balance']} \n")
            break
        else:
            utils.printMessage('invalid', 'Please enter an amount greater than 0!')
            continue
    utils.checkExitIntent('Do you want to terminate this session? ([Y]es / [N]o)', user, utils.exit, bankOperations, accountNumber)


def balanceEnquiry(bankOperations, accountNumber, userData):
    with console.status('Fetching your account balance. Please wait', spinner='point', refresh_per_second=5):
        sleep(4.5)
    
    currentDateTime = datetime.now()
    currentDate = currentDateTime.strftime('{d} %b, %Y').replace("{d}", utils.ordinal(currentDateTime.day))
    currentTime = currentDateTime.strftime('%I:%M:%S %p')
    print(f"Your balance as at {currentDate} [{currentTime}] is ₦{userData[accountNumber]['balance']}")

    utils.checkExitIntent('\nDo you want to exit? ([Y]es / [N]o)', userData, utils.exit, bankOperations, accountNumber)


def userProfile(bankOperations, accountNumber, userData):
    print('[bold purple]\n⚞| Your Profile ][/bold purple]', end = '\n\n')

    print(f"Name: {userData[accountNumber]['firstName']} {userData[accountNumber]['lastName']}")
    print(f"Email: {userData[accountNumber]['emailAddress']}")
    print(f"Account Balance: ₦{userData[accountNumber]['balance']}")
    print(f"BVN: {userData[accountNumber]['BVN']}")
    print(f"Account Number: {accountNumber}")
    print(f"Date Registered: {userData[accountNumber]['dateRegistered']}")

    utils.checkExitIntent('\nDo you want to exit? ([Y]es / [N]o)', userData, utils.exit, bankOperations, accountNumber)


def about(bankOperations, accountNumber, userData):
    info = '''
♦ ♦ ♦ ♦ ♦ ♦ ♦ ♦ ♦ ♦ ♦ ♦ ♦ ♦ ♦ ♦ ♦ ♦ ♦
                                
      {f}1m{f}35m♦♦  About Pearl Bank  ♦♦{f}0m     

    Pearl Bank was established in
    the  early {f}1m{f}34m2000{f}0m's by the then
    & current CEO, {f}33m{f}3mObioha Omezibe{f}0m
    (B.Sc, M.Sc & Ph.D).


    We're social! Follow us :)
    F: {f}1m{f}34m/PearlBank{f}0m
    T: {f}1m{f}34m@PearlBank{f}0m
    I: {f}1m{f}34m@PearlBank{f}0m

    {f}1m{f}35mContact Us:{f}0m
    {f}1m{f}35mTel: {f}1m{f}34m+2349000009999{f}0m
    {f}1m{f}35mAddress: {f}1m{f}34m1 Pearl Street{f}0m
    '''.replace('{f}', '\033[')
    
    for char in info:
        sleep(.05)
        sys.stdout.write(char)
        sys.stdout.flush()
    utils.checkExitIntent('\nDo you want to exit? ([Y]es / [N]o)', userData, utils.exit, bankOperations, accountNumber)
