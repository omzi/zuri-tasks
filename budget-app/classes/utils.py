from datetime import datetime


def ordinal(n: int) -> str:
  # Add ordinal suffix for the day of the month; i.e. 'st', 'nd', 'rd' or 'th'
  return str(n) + ('th' if 4 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th'))


class Budget:
    '''
    Contains all data and methods for manipulating instances of the 'Budget' class
    '''
    def __init__(self, data):
        self.data = data
        self.categories = list(data['categories'])
        self.transfers = data['transfers']
    
    def check_category(self, category: str) -> bool:
        '''
        Checks if a budget category is existent
        '''
        return category.lower() in list(map(str.lower, self.categories))

    def add_category(self, category: str):
        '''
        Adds a new category to an instance of the Budget class
        '''
        self.categories.append(category)
        self.data['categories'][category] = { 'amount': 0, 'content': [] }
    
    def add_budget(self, category: str, description: str):
        '''
        Adds a budget to an existing category
        '''
        current_datetime = datetime.now()
        date_added = current_datetime.strftime('{d} %b, %Y').replace("{d}", ordinal(current_datetime.day))
        time_added = current_datetime.strftime('%I:%M:%S %p')

        self.data['categories'][category]['content'].append([description, date_added, time_added])
    
    def deposit(self, category: str, amount: int) -> bool:
        '''
        Adds a specified amount to an existing budget category
        '''
        if amount > 0:
            self.data['categories'][category]['amount'] += amount
            return True
        else:
            return False

    def withdraw(self, category: str, amount: int) -> bool:
        '''
        Deducts a specified amount from an existing budget category
        '''
        if 0 < amount <= self.data['categories'][category]['amount']:
            self.data['categories'][category]['amount'] -= amount
            return True
        else:
            return False
    
    def transfer(self, source: str, amount: int, destination: str):
        '''
        Transfers funds between existing categories
        '''
        self.data['categories'][source]['amount'] -= amount
        self.data['categories'][destination]['amount'] += amount

        current_datetime = datetime.now()
        date_transferred = current_datetime.strftime('{d} %b, %Y').replace("{d}", ordinal(current_datetime.day))
        time_transferred = current_datetime.strftime('%I:%M:%S %p')
        self.transfers.append([source.capitalize(), destination.capitalize(), amount, date_transferred, time_transferred])


class Formatting:
    ENDF = '\033[0m'
    BOLD = '\033[1m'
    BOLDITALIC = '\033[1m\033[3m'
    LIGHT = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    INVERT = '\033[7m'
    COLOR_BLACK = '\033[30m'
    COLOR_RED = '\033[31m'
    COLOR_GREEN = '\033[32m'
    COLOR_YELLOW = '\033[33m'
    COLOR_BLUE = '\033[34m'
    COLOR_PURPLE = '\033[35m'
    COLOR_PURPLE = '\033[35m'
    COLOR_CYAN = '\033[36m'
    COLOR_WHITE = '\033[37m'
    BACKGROUND_BLACK = '\033[40m'
    BACKGROUND_RED = '\033[41m'
    BACKGROUND_GREEN = '\033[42m'
    BACKGROUND_YELLOW = '\033[43m'
    BACKGROUND_BLUE = '\033[44m'
    BACKGROUND_PURPLE = '\033[45m'
    BACKGROUND_CYAN = '\033[46m'
    BACKGROUND_WHITE = '\033[47m'
