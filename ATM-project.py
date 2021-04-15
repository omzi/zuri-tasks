from datetime import datetime

username = input('Enter your username: \n')
allowedUsers = ['Omzi', 'Hagin', 'Seyi', 'femi', 'TheRealChiefDaddy']
allowedPassword = ['0'*4, '1'*4, '2'*4, '3'*4, '4'*4]


def ordinal(n):
  # Add ordinal suffix for the day of the month; i.e. 'st', 'nd', 'rd' or 'th'
  return str(n) + ('th' if 4 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th'))

def checkExitIntent(message, exitFirst):
  # Brought out that functionality here to DRY out my code
  global isSessionActive

  while True:
    option = input(message + ' \n')

    if option.upper() == 'Y':
      isSessionActive = False if exitFirst else True
      break
    elif option.upper() == 'N':
      isSessionActive = True if exitFirst else False
      break
    else:
      print('\nInvalid option. Reply Y for Yes & N for No')

# Creates a new list of users lowercased for password & case-insensitive user checking
users = list(map(str.lower, allowedUsers))

if username.lower() in users:
  password = input('Enter your password: \n')
  userId = users.index(username.lower())

  if password == allowedPassword[userId]:
    balance = 0; isSessionActive = True
    
    while isSessionActive:
      currentDateTime = datetime.now()

      print(f'\nHi, {allowedUsers[userId]}!', end='')
      print('''
╔╦╦╦═╦╗╔═╦═╦══╦═╗
║║║║╩╣╚╣═╣║║║║║╩╣
╚══╩═╩═╩═╩═╩╩╩╩═╝
      ''')
      print("DATE:", currentDateTime.strftime("{d} %b, %Y").replace("{d}", ordinal(currentDateTime.day)), end=' / ')
      print("TIME:", currentDateTime.strftime("%I:%M:%S %p"))
      print('\n1. Withdrawal \n2. Cash Deposit \n3. Complaint \n4. About \n5. Exit \n')

      try:
        selectedOption = int(input('Please select an option: '))

        if selectedOption == 1:
          # 1. Withdrawal
          print('How much would you like to withdraw? \n')

          while True:
            try:
              withdrawalAmount = int(input('Amount: '))
            except ValueError:
              print('Please enter a valid amount!')
              continue

            if balance == 0:
              print('Your balance is ₦0. Please make a deposit before you can withdraw. \n')
              break
            elif withdrawalAmount > balance:
              print(f'Insufficient funds :(. Withdraw an amount less than ₦{balance}.')
              continue
            else:
              balance -= withdrawalAmount
              print(f'Transaction successful! You just withdrew ₦{withdrawalAmount} & your balance is ₦{balance} \n')
              break
          
          checkExitIntent('Do you want to perform another transaction? ([Y]es / [N]o)', False)

        elif selectedOption == 2:
          # 2. Deposit
          print('How much would you like to deposit? \n')

          while True:
            try:
              depositAmount = int(input('Amount: '))
            except ValueError:
              print('Please enter a valid amount!')
              continue

            if depositAmount > 0:
              balance += depositAmount
              print(f'Money deposited successfully! Your current balance is ₦{balance} \n')
              break
            else:
              print('Please enter an amount greater than 0!')
              continue

          checkExitIntent('Do you want to perform another transaction? ([Y]es / [N]o)', False)

        elif selectedOption == 3:
          # 3. Compliants
          complaint = input('What issue would you like to report? \n➝ ')

          # Send complaint to wherever
          print(f'\nYour Complaint: \n➝ {complaint} \n')
          print('Thank you for contacting us! We will get back to you shortly.\n')

          checkExitIntent('Do you want to exit? ([Y]es / [N]o)', True)
        elif selectedOption == 4:
          # 4. About
          print('\n✱ About ✱')
          print('\n ➝ Task: Mock ATM \n ➝ Author: Omezibe Obioha (@o_obioha) \n ➝ Date: 2021-03-30T21:05:13.710Z')
          print('\n© 2021, Oʍʐɨ \n')

          checkExitIntent('Do you want to exit? ([Y]es / [N]o)', True)
        elif selectedOption == 5:
          # 5. Exit
          checkExitIntent('Are you sure you want to exit? ([Y]es / [N]o)', True)
        else:
          print('Error: Invalid option! Please try again :(')
      except ValueError:
        print('Please enter a valid option!')
        continue

    print('Thank you for banking with us! Have a nice day :)')
  else:
    print('Incorrect password! Please try again :(')

else:
  print(f'Username "{username}" not found in system! Please try again :(')

# THE END