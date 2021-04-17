# I've tried sticking to PEP 8 guidelines but... camelCase rules🤘!
import os
from time import sleep
import simplejson as json
from tabulate import tabulate
from classes.utils import Budget, Formatting as Style


isFirstAction = True

def init():
    budget = {  }
    data = os.path.dirname(os.path.realpath(__file__)) + '\\' + 'budget.json'
    if os.path.isfile(data) and os.stat(data).st_size != 0:
        savedData = open(data, 'r+')
        budget = json.loads(savedData.read())
    else:
        newFile = open(data, 'w+')
        budget = { "categories": {}, "transfers": [] }
        newFile.write(json.dumps(budget))
    
    print('\n' + Style.BACKGROUND_BLACK + Style.COLOR_GREEN + Style.BOLD + '[ Welcome to Budgeteer™ ! ]' + Style.ENDF)
    print('═' * 27, '\n', end='')
    budgeteer = Budget(budget)

    return budgeteer


def saveData(budget):
    data = os.path.dirname(os.path.realpath(__file__)) + '\\' + 'budget.json'
    if os.path.isfile(data) and os.stat(data).st_size != 0:
        savedData = open(data, 'w+')
        savedData.write(json.dumps(budget))
    else:
        newFile = open(data, 'w+')
        newFile.write(json.dumps(budget))


def stringCheck(budget, string, stringInput, stringEmpty, stringNonExistent):
    while True:
        string = styledInput(stringInput)

        if not len(string):
            showMessage('error', f'Error: {stringEmpty}')
            continue
        if not budget.check_category(string):
            showMessage('error', f'Error: {stringNonExistent}')
            continue
        return string


def getAction():
    global isFirstAction
    i = 1; actions = ['Add Budget', 'Add Category', 'View Categories', 'View Budgets', 'Get Balances', 'Withdraw', 'Deposit', 'Transfer', 'View Transfers', 'About', 'Exit']
    
    if not isFirstAction:
        print('═' * (len(max(actions, key=len)) + 3))
    isFirstAction = False

    for action in actions:
        print(f'{Style.BOLDITALIC}{i}. {Style.COLOR_CYAN}{action}{Style.ENDF}')
        sleep(0.1)
        i += 1

    while True:
        action = None
        try:
            action = int(styledInput('Select an option'))
        except ValueError:
            showMessage('error', 'Error: Enter a valid option!')
            continue
        if action < 1 or action > len(actions):
            showMessage('error', 'Error: Enter a valid option!')
            continue
        else:
            break

    return action


def styledInput(content):
    exitHint = f'\n{Style.ITALIC}{Style.COLOR_YELLOW}** Hint: Type "quit" anywhere to exit the app instantly{Style.ENDF}'
    userInput = input(f'{exitHint}{Style.COLOR_PURPLE}{Style.ITALIC}\n{content}:{Style.ENDF}\n')
    if userInput.lower() == 'quit':
        quit()
    else:
        return userInput


def showMessage(state, content):
    if state.lower() == 'error':
        print(f'{Style.BOLDITALIC}{Style.COLOR_RED}{content}{Style.ENDF}')
    elif state.lower() == 'valid':
        print(f'{Style.BOLDITALIC}{Style.COLOR_WHITE}{content}{Style.ENDF}')
    sleep(0.75)


def addBudget(budget):
    # 1. Add Budget
    category = None; description = None
    category = stringCheck(budget, category, 'Enter the category', 'Category cannot be empty!', 'Category does not exist!')

    while True:
        description = styledInput('Enter its description')

        if not len(category):
            showMessage('error', 'Error: Category cannot be empty!')
            continue
        break

    budget.add_budget(category, description)
    showMessage('valid', 'Budget has been added successfully!')
    saveData(budget.data); showActions(budget)


def addCategory(budget):
    # 2. Add Category
    category = None

    while True:
        category = styledInput('Enter the category name')

        if not len(category):
            showMessage('error', 'Error: Category cannot be empty!')
            continue
        if budget.check_category(category):
            showMessage('error', f'Error: Category "{category}" already exists!')
            continue
        break
    
    budget.add_category(category)
    showMessage('valid', f'Category "{category}" has been added successfully!')
    saveData(budget.data); showActions(budget)


def viewCategories(budget):
    # 3. View Categories
    if len(budget.data['categories']):
        print(f'{Style.BOLD}{Style.COLOR_PURPLE}✱ All Categories ✱{Style.ENDF}')
        
        for category in budget.categories:
            print(f'-→ {category.capitalize()}')
    else:
        print(f'{Style.BOLDITALIC}{Style.COLOR_RED}No category created yet!{Style.ENDF}')
    print(); showActions(budget)


def viewBudgets(budget):
    # 4. View Budgets
    print(f'{Style.BOLD}{Style.COLOR_BLUE}✱ All Budgets ✱{Style.ENDF} \n')

    for category, data in budget.data['categories'].items():
        print(f"{Style.BOLD}{Style.COLOR_PURPLE}-→ {category.capitalize()} (₦{data['amount']}) {Style.ENDF}")
        
        # data['content'] = [item[1:] for item in data['content']]
        print(tabulate(data['content'], headers=['Description', 'Date Added', 'Time Added'], tablefmt='fancy_grid'), '\n')
        sleep(0.5)
    showActions(budget)


def getBalances(budget):
    # 5. Get Balances
    print(f'{Style.BOLD}{Style.COLOR_BLUE}✱ Balances ✱{Style.ENDF}')
    newData = budget.data['categories'].items()
    categories = [data[-0].capitalize() for data in newData]
    balances = [data['amount'] for data in [data[-1] for data in newData]]
    total = sum(balances)

    tableData = list(zip([*categories, f'{Style.BOLD}TOTAL{Style.ENDF}'], [*balances, f'₦{total}']))
    tableHeaders = [f'{Style.BOLDITALIC}Category{Style.ENDF}', f'{Style.BOLDITALIC}Balance{Style.ENDF}']
    
    print(tabulate(tableData, tableHeaders, tablefmt='fancy_grid'))
    showActions(budget)


def withdraw(budget):
    # 6. Withdraw
    category = None; amount = 0
    category = stringCheck(budget, category, 'Enter the category you want to withdraw from', 'Category cannot be empty!', 'Category does not exist!')
    
    while True:
        try:
            amount = int(styledInput('Enter the amount you want to withdraw'))
        except ValueError:
            showMessage('error', 'Error: Enter a valid amount!')
            continue
        if budget.withdraw(category, amount):
            sleep(0.5)
            showMessage('valid', f'You successfully withdrew ₦{amount} from the {category} category!')
            break
        else:
            showMessage('error', f'Please enter an amount greater than ₦0 & less than ₦{budget.data["categories"][category]["amount"]}!')
            continue
    saveData(budget.data); showActions(budget)


def deposit(budget):
    # 7. Withdraw
    category = None; amount = 0
    category = stringCheck(budget, category, 'Enter the category you want to deposit to', 'Category cannot be empty!', 'Category does not exist!')
    
    while True:
        try:
            amount = int(styledInput('Enter the amount you want to deposit'))
        except ValueError:
            showMessage('error', 'Error: Enter a valid amount!'); getAction()
            continue
        if budget.deposit(category, amount):
            sleep(0.5)
            showMessage('valid', f'You successfully deposited ₦{amount} to the {category} category!')
            break
        else:
            showMessage('error', 'Please enter an amount greater than ₦0!')
            continue
    saveData(budget.data); showActions(budget)


def transfer(budget):
    # 8. Transfer
    source = None; destination = None
    source = stringCheck(budget, source, "Enter the category you're transferring FROM", 'Source category cannot be empty!', 'Source category does not exist!')
    destination = stringCheck(budget, destination, "Enter the category you're transferring TO", 'Destination category cannot be empty!', 'Destination category does not exist!')

    while True:
        try:
            amount = int(styledInput('Enter the amount you want to transfer'))
        except ValueError:
            showMessage('error', 'Error: Enter a valid amount!')
            continue

        if amount == 0:
            showMessage('error', 'Error: Enter an amount greater than ₦0!')
            continue

        sourceAmount = budget.data['categories'][source]['amount']
        if sourceAmount == 0:
            showMessage('error', "Source category's balance is empty!")
            continue
        elif sourceAmount < amount:
            showMessage('error', f'Please enter an amount less than ₦{sourceAmount}!')
            continue
        else:
            budget.transfer(source, amount, destination)
            sleep(0.5)
            showMessage('valid', f'You successfully transferred ₦{amount} to the {destination} category!')
            break
    saveData(budget.data); showActions(budget)


def viewTransfers(budget):
    # 9. View Transfers
    if len(budget.data['transfers']):
        print(f'{Style.BOLD}{Style.COLOR_BLUE}✱ All Transfers ✱{Style.ENDF}')

        print(tabulate(budget.data['transfers'], headers=['Source', 'Destination', 'Amount', 'Date Transferred', 'Time Transferred'], tablefmt='fancy_grid'), '\n')
        sleep(0.5)
    else:
        print(f'{Style.BOLDITALIC}{Style.COLOR_BLUE}No transfer record yet!{Style.ENDF} \n')
    showActions(budget)


def about():
    print(f'{Style.BOLD}{Style.COLOR_BLUE}\n✱ About ✱{Style.ENDF}')
    print(f'{Style.BOLDITALIC}{Style.COLOR_PURPLE}\n➝  Task: Budget App (Budgeteer) \n➝  Author: Omezibe Obioha (@o_obioha) \n➝  Date: 2021-04-17T10:20:16.660Z{Style.ENDF}')
    print(f'{Style.BOLD}{Style.COLOR_BLUE}\n© 2021, Oʍʐɨ \n{Style.ENDF}')


def exit(budget):
    while True:
        option = input(f'{Style.BOLDITALIC}{Style.COLOR_RED}Are you sure you want to exit? ([Y]es / [N]o){Style.ENDF}\n')

        if option.upper() == 'Y':
            break
        elif option.upper() == 'N':
            showActions(budget)
        else:
            print('\nInvalid option. Reply Y for Yes & N for No')
    print('Hope you had a nice experience with Budgeteer! Have a nice day :)')


def showActions(data):
    action = getAction()
    if action == 1:
        addBudget(data)
    elif action == 2:
        addCategory(data)
    elif action == 3:
        viewCategories(data)
    elif action == 4:
        viewBudgets(data)
    elif action == 5:
        getBalances(data)
    elif action == 6:
        withdraw(data)
    elif action == 7:
        deposit(data)
    elif action == 8:
        transfer(data)
    elif action == 9:
        viewTransfers(data)
    elif action == 10:
        about(); showActions(data)
    elif action == 11:
        exit(data)


def app():
    data = init(); showActions(data)


app()
