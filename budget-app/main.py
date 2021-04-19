# I've tried sticking to PEP 8 guidelines but... camelCase rules🤘!
import os
from time import sleep
import simplejson as json
from tabulate import tabulate
from classes.utils import Budget, Formatting as Style


isFirstAction = True
dataFile = os.path.dirname(os.path.realpath(__file__)) + '\\' + 'budget.json'

def init():
    budget = {  }
    global dataFile
    
    # Loads data from the budget.json file & creates a new one if non-existent
    if os.path.isfile(dataFile) and os.stat(dataFile).st_size != 0:
        savedData = open(dataFile, 'r+')
        budget = json.loads(savedData.read())
    else:
        budget = { "categories": {}, "transfers": [] }
        open(dataFile, 'w+').write(json.dumps(budget))
    
    # Instantiates the budget class and returns the object
    print('\n' + Style.BACKGROUND_BLACK + Style.COLOR_GREEN + Style.BOLD + '[ Welcome to Budgeteer™ ! ]' + Style.ENDF)
    print('═' * 27, '\n', end='')
    budgeteer = Budget(budget)

    return budgeteer


def saveData(budget):
    # Saves a user's budgets data to a JSON file
    global dataFile

    open(dataFile, 'w+').write(json.dumps(budget))


def stringCheck(budget, string, stringInput, stringEmpty, stringNonExistent):
    while True:
        string = styledInput(stringInput, budget)

        if not len(string):
            printMessage('error', f'Error: {stringEmpty}')
            continue
        if not budget.check_category(string):
            printMessage('error', f'Error: {stringNonExistent}')
            continue
        return string


def getAction(budget):
    # Shows the list of possible options to a user and returns the chosen option
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
            action = int(styledInput('Select an option', budget))
        except ValueError:
            printMessage('error', 'Error: Enter a valid option!')
            continue
        if action < 1 or action > len(actions):
            printMessage('error', 'Error: Enter a valid option!')
            continue
        else:
            break

    return action


def styledInput(content, budget):
    # Styles the user input prompt and exits the app if the input == "quit" or goes to the main menu if input == "menu"
    exitHint = f'\n{Style.ITALIC}{Style.COLOR_YELLOW}** Hint: Type "menu" to access the main menu or "quit" to exit the app instantly{Style.ENDF}'
    userInput = input(f'{exitHint}{Style.COLOR_PURPLE}{Style.ITALIC}\n{content}:{Style.ENDF}\n❯❯ ')
    if userInput.lower() == 'quit':
        quit()
    elif userInput.lower() == 'menu':
        showActions(budget)
    else:
        return userInput


def printMessage(state, content):
    # Prints a message and styles it based on a specified state
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
        description = styledInput('Enter its description', budget)
        if not len(category):
            printMessage('error', 'Error: Category cannot be empty!')
            continue
        break

    budget.add_budget(category, description)
    printMessage('valid', 'Budget has been added successfully!')
    saveData(budget.data); showActions(budget)


def addCategory(budget):
    # 2. Add Category
    category = None

    while True:
        category = styledInput('Enter the category name', budget)
        if not len(category):
            printMessage('error', 'Error: Category cannot be empty!')
            continue
        if budget.check_category(category):
            printMessage('error', f'Error: Category "{category}" already exists!')
            continue
        break
    
    budget.add_category(category)
    printMessage('valid', f'Category "{category}" has been added successfully!')
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
        print(f"{Style.BOLD}{Style.COLOR_PURPLE}❯❯ {category.capitalize()} (₦{data['amount']}) {Style.ENDF}")
        
        print(tabulate(data['content'], headers=['Description', 'Date Added', 'Time Added'], tablefmt='fancy_grid'), '\n')
        sleep(0.5)
    showActions(budget)


def getBalances(budget):
    # 5. Get Balances
    # TODO: Add an addComma() function to format the balances before printing
    print(f'{Style.BOLD}{Style.COLOR_BLUE}✱ Balances ✱{Style.ENDF}')
    newData = budget.data['categories'].items()
    categories = [data[-0].capitalize() for data in newData]
    balances = [data['amount'] for data in [data[-1] for data in newData]]
    balancesFormatted = ["{:,}".format(balance) for balance in balances]
    total = sum(balances)

    tableData = list(zip([*categories, f'{Style.BOLD}TOTAL{Style.ENDF}'], [*balancesFormatted, f'₦{"{:,}".format(total)}']))
    tableHeaders = [f'{Style.BOLDITALIC}Category{Style.ENDF}', f'{Style.BOLDITALIC}Balance{Style.ENDF}']
    
    print(tabulate(tableData, tableHeaders, tablefmt='fancy_grid'))
    showActions(budget)


def withdraw(budget):
    # 6. Withdraw
    category = None; amount = 0
    category = stringCheck(budget, category, 'Enter the category you want to withdraw from', 'Category cannot be empty!', 'Category does not exist!')
    
    while True:
        try:
            amount = int(styledInput('Enter the amount you want to withdraw', budget))
        except ValueError:
            printMessage('error', 'Error: Enter a valid amount!')
            continue
        if budget.withdraw(category, amount):
            sleep(0.5)
            printMessage('valid', f'You successfully withdrew ₦{amount} from the {category} category!')
            break
        else:
            printMessage('error', f'Please enter an amount greater than ₦0 & less than ₦{budget.data["categories"][category]["amount"]}!')
            continue
    saveData(budget.data); showActions(budget)


def deposit(budget):
    # 7. Withdraw
    category = None; amount = 0
    category = stringCheck(budget, category, 'Enter the category you want to deposit to', 'Category cannot be empty!', 'Category does not exist!')
    
    while True:
        try:
            amount = int(styledInput('Enter the amount you want to deposit', budget))
        except ValueError:
            printMessage('error', 'Error: Enter a valid amount!'); getAction(budget)
            continue
        if budget.deposit(category, amount):
            sleep(0.5)
            printMessage('valid', f'You successfully deposited ₦{amount} to the {category} category!')
            break
        else:
            printMessage('error', 'Please enter an amount greater than ₦0!')
            continue
    saveData(budget.data); showActions(budget)


def transfer(budget):
    # 8. Transfer
    source = None; destination = None
    source = stringCheck(budget, source, "Enter the category you're transferring FROM", 'Source category cannot be empty!', 'Source category does not exist!')
    destination = stringCheck(budget, destination, "Enter the category you're transferring TO", 'Destination category cannot be empty!', 'Destination category does not exist!')

    while True:
        try:
            amount = int(styledInput('Enter the amount you want to transfer', budget))
        except ValueError:
            printMessage('error', 'Error: Enter a valid amount!')
            continue

        if amount == 0:
            printMessage('error', 'Error: Enter an amount greater than ₦0!')
            continue

        sourceAmount = budget.data['categories'][source]['amount']
        if sourceAmount == 0:
            printMessage('error', "Source category's balance is empty!")
            continue
        elif sourceAmount < amount:
            printMessage('error', f'Please enter an amount less than ₦{"{:,}".format(sourceAmount)}!')
            continue
        else:
            budget.transfer(source, amount, destination)
            sleep(0.5)
            printMessage('valid', f'You successfully transferred ₦{"{:,}".format(amount)} to the {destination} category!')
            break
    saveData(budget.data); showActions(budget)


def viewTransfers(budget):
    # 9. View Transfers
    if len(budget.data['transfers']):
        print(f'{Style.BOLD}{Style.COLOR_BLUE}✱ All Transfers ✱{Style.ENDF}')
        tableData = [[f'₦{"{:,}".format(item)}' if isinstance(item, int) else item for item in data] for data in budget.data['transfers']]

        print(tabulate(tableData, headers=['Source', 'Destination', 'Amount', 'Date Transferred', 'Time Transferred'], tablefmt='fancy_grid'), '\n')
        sleep(0.5)
    else:
        print(f'{Style.BOLDITALIC}{Style.COLOR_BLUE}No transfer record yet!{Style.ENDF} \n')
    showActions(budget)


def about():
    print(f'{Style.BOLD}{Style.COLOR_BLUE}\n✱ About ✱{Style.ENDF}')
    print(f'{Style.BOLDITALIC}{Style.COLOR_PURPLE}\n➝  Task: Budget App (Budgeteer) \n➝  Author: Omezibe Obioha (@o_obioha) \n➝  Date: 2021-04-17T10:20:16.660Z{Style.ENDF}')
    print(f'{Style.BOLD}{Style.COLOR_BLUE}\n© 2021, Oʍʐɨ \n{Style.ENDF}')
    sleep(5)


def exit(budget):
    # Confirms a user's choice to exit the app
    while True:
        option = input(f'{Style.BOLDITALIC}{Style.COLOR_RED}Are you sure you want to exit?{Style.ENDF} ([Y]es / [N]o)\n')

        if option.upper() == 'Y':
            break
        elif option.upper() == 'N':
            showActions(budget)
        else:
            print('\nInvalid option. Reply Y for Yes & N for No')
    print('Hope you had a nice experience with Budgeteer! Have a nice day :)')


def showActions(data):
    action = getAction(data)
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
