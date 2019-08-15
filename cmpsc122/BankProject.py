class Bank:  
  	def __init__(self, lst=[]):
      	self.listOfPeople=lst
    
    def getList(self):
      	return self.listOfPeople
    
    def addPersonToList(self, person):
      	'''adds the specified person to the list of people
        raises an exception if the specified person is not an instance of Person (including its subclasses)'''
        if (isinstance(person,Person)):
          	self.listOfPeople.append(person)
        else:
          	raise TypeError("Please specify a Person to add to the Bank")
        
    def removePersonFromList(self, person):
      	'''removes the specified person from the list of people
        
        raises an exception if the specified person is not an instance of Person (including its subclasses)
        raises an exception if the specified person is not in the Banks listOfPeople'''
        if not (isinstance(person,Person)):
          	raise TypeError("person must be a Person object")
        if (person in self.listOfPeople):
          	self.listOfPeople.remove(person)
        else:
          	raise Exception("The specified person is not a member of this Bank")
        
    def removePersonFromListByID(self, ID):
      	'''searches through the list of people until it finds a person with the specified ID
        If the person is found, prints done and removes the person
        If the person is not found, it prints an error message
        always returns None'''
      	temp = self.listOfPeople[:]
      	for person in temp:
          	if person.returnID() == ID:
            	self.listOfPeople.remove(person)
                print("done")
                return
        print("There is no person in this Bank with that ID")
        return

    
class Account:
    
    def __init__(self):
        pass
      
    def getBalance(self):
      	raise NotImplementedError("Subclass must implement abstract method")
      
    def deposit(self, amount):
      	raise NotImplementedError("Subclass must implement abstract method")
    
    def withdraw(self, amount):
      	raise NotImplementedError("Subclass must implement abstract method")
    
    
    def __str__(self):
      	return "This is an abstract account"

    __repr__ = __str__


class Checking(Account):
    Number_of_Accounts = 0

    def __init__(self, balance=0, apr=5.0, cashback=0):
        '''Initializes each account with an account number (starts at 0 and increases with every account created)
        Defines the balance of the account in dollars - Default = $0
        Defines the annual percentage rate of the checking account in percent - Default = 5.0%
        Defines the percent cashback with each purchase (withdraw) - Default = 0.0%
        
        All arguments must be ints or floats
        raises a TypeError if any argument is not an int or a float'''
        if not (isinstance(balance, int) or isinstance(balance,float)):
          	raise TypeError("Balance must be an int or a float")
        if not (isinstance(apr, int) or isinstance(apr,float)):
          	raise TypeError("APR must be an int or a float")
        if not (isinstance(cashback, int) or isinstance(cashback,float)):
          	raise TypeError("Cashback must be an int or a float")
        
        self.number=self.createNumber()
        self.balance=balance
        self.apr=apr
        self.cashback=cashback

    def createNumber(self):
        '''Creates a number to be used to identify the account
        The first account created has number 1, the second has number 2, etc.'''
        Checking.Number_of_Accounts += 1
        return Checking.Number_of_Accounts

    def getBalance(self):
        return self.balance

    def deposit(self, amount):
        '''Increments the balance of the account by the amount specified
        raises a TypeError if the amount is not an int or a float'''
        if not (isinstance(amount, int) or isinstance(amount,float)):
          	raise TypeError("Amount must be an int or a float")
        
        self.balance += amount

    def purchase(self,amount):
        '''processes a purchase from the checking account,
        decrements the balance by the amount indicated
        adds cashback into the account
        
        raises a TypeError if the amount is not an int or a float'''
        if not (isinstance(amount, int) or isinstance(amount,float)):
          	raise TypeError("Amount must be an int or a float")
        
        self.balance -= amount
        self.balance += (self.cashback / 100) * amount

    def incurPenalty(self):
        '''determines if this checking account is overdue and needs to pay a penalty
        if it has a positive balance, then no penalty is incurred 
        if the balance is negative, then interest is applied to the account'''
        if (self.balance >= 0):
            return
        else:
            self.balance += (self.apr / 100) * self.balance


    def __str__(self):
        return "Account Number {0} has a balance of {1}".format(self.number, self.balance)

    __repr__ = __str__


class Savings(Account):
    Number_of_Accounts = 0

    def __init__(self, balance, interest=0.5):
        '''Initializes each account with an account number (starts at 0 and increases with every account created)
        Each Savings account must have an initial deposit, raises an Exception if this initial value is zero or less
        Defines the interest rate of the checking account in percent - Default = 0.5%
        
        raises a Type Error if balance or interest are not floats or ints'''
        if not (isinstance(balance, int) or isinstance(balance,float)):
          	raise TypeError("Balance must be an int or a float")
        if not (isinstance(interest, int) or isinstance(interest,float)):
          	raise TypeError("Interest must be an int or a float")
        
        self.number=self.createNumber()

        if(balance <= 0):
            raise Exception("A Savings Account must have an initial deposit")
        else:
            self.balance = balance

        self.interest=interest

    def createNumber(self):
        '''Creates a number to be used to identify the account
        The first account created has number 1, the second has number 2, etc.'''
        Savings.Number_of_Accounts += 1
        return Savings.Number_of_Accounts

    def getBalance(self):
        return self.balance

    def deposit(self, amount):
        '''Increments the balance of the account by the amount specified
        raises a TypeError if the amount is not an int or a float'''
        if not (isinstance(amount, int) or isinstance(amount,float)):
          	raise TypeError("Amount must be an int or a float")
        
        self.balance += amount
    
    def withdraw(self, amount):
        '''Decrements the balance of the account by the amount specified
        
        Raises an Exception if the withdraw would create a negative balance
        Raises a TypeError if the amount is not an int or float'''
        if not (isinstance(amount, int) or isinstance(amount,float)):
          	raise TypeError("Amount must be an int or a float")
        if (self.balance <= amount):
            raise Exception("Insufficient Funds")
        
        self.balance -= amount

    def accrueInterest(self):
        '''Calculates the interest and adds it to the current balance'''
        self.balance += (self.balance * (self.interest / 100))


    def __str__(self):
        return "Account Number {0} has a balance of {1}".format(self.number, self.balance)

    __repr__ = __str__
      
      
class Loan:
    Number_of_Loans=0

    def __init__(self, loanAmount=1000, interest=8, paymentAmount=100):
        '''Initializes each loan with a loan number (starts at 0 and increases with every account created)
        Defines the amount of the loan in dollars - Default = $1000
        Defines the monthly interest rate of the loan in percent - Default = 8%
        Defines the amount the customer will pay monthly in dollars - Default = $100
        Defines the number of payments that have to be made, and the amount of the final payment in dollars, 
        	by calling the method calculateNumOfPayments
        
        all arguments must be ints or floats,
        raises a TypeError if any argument is not an int or float'''
        if not (isinstance(loanAmount, int) or isinstance(loanAmount,float)):
          	raise TypeError("Loan Amount must be an int or a float")
        if not (isinstance(interest, int) or isinstance(interest,float)):
          	raise TypeError("Interest must be an int or a float")
        if not (isinstance(paymentAmount, int) or isinstance(paymentAmount,float)):
          	raise TypeError("Payment Amount must be an int or a float")
        
        self.number=self.createNumber()
        self.loanAmount=loanAmount
        self.interest=interest
        self.paymentAmount=paymentAmount
        self.paymentNum, self.finalPayment = self.calculateNumOfPayments(loanAmount, interest, paymentAmount)

    def createNumber(self):
        '''Creates a number to be used to identify the loan
        The first loan created has number 1, the second has number 2, etc.'''
        Loan.Number_of_Loans += 1
        return Loan.Number_of_Loans

    def getLoanAmount(self):
        return float("%.2f" % self.loanAmount)

    def calculateNumOfPayments(self, loanAmount, interest, paymentAmount):
        '''While the loan amount that has yet to be paid is greater than or equal to the payment amount, the loan accumulates monthly interest,
        and then decreases by the monthly payment amount. After each iteration, the number of payments needed increases by 1. This continues 
        until the remaining balance of the loan is less than the monthly payment amount; that remaining balance then becomes the final payment. 
        The method returns the number of payments needed, and the final payment.
        
        all arguments must be ints or floats,
        raises a TypeError if any argument is not an int or float'''
        if not (isinstance(loanAmount, int) or isinstance(loanAmount,float)):
          	raise TypeError("Loan Amount must be an int or a float")
        if not (isinstance(interest, int) or isinstance(interest,float)):
          	raise TypeError("Interest must be an int or a float")
        if not (isinstance(paymentAmount, int) or isinstance(paymentAmount,float)):
          	raise TypeError("Payment Amount must be an int or a float")
        
        paymentNum=0
        while loanAmount>=paymentAmount:
            loanAmount+=(loanAmount * (interest / 100))
            loanAmount-=paymentAmount
            paymentNum+=1
        finalPayment=float("%.2f" % loanAmount)
        paymentNum+=1
        return paymentNum, finalPayment

    def makePayment(self):
        '''If more than one payment remains, accrue interest and then decrease by the payment amount; finally, decrement the number
        of payments remaining
        If one payment remains, it is paid and both the loan value and payments remaining are set to 0
        If no payments remain, the user is told that they have already paid off their loan '''
        if self.paymentNum > 1:
            self.loanAmount+=(self.loanAmount * (self.interest / 100))
            self.loanAmount-=self.paymentAmount
            self.paymentNum-=1
            print("You have %d payment(s) remaining." % self.paymentNum)
        elif self.paymentNum == 1:
            self.loanAmount=0
            self.paymentNum=0
            print("You have made your final payment!")
        elif self.paymentNum == 0:
            print("You have already paid off your loan!")
  
class Person:
    def __init__(self,name):
      	'''Creates a Person object with the Name attribute
        
        name must be a string, raises a TypeError if it is not'''
        if not (isinstance(name, str)):
        	raise TypeError("Name must be a string")
        
        self.name=name

    def __createID(self):
        '''this abstract private method must be implemented by each subclass
        it is private so users cannot make their own (or fake) IDs; only the program is supposed to assign an ID'''
        raise NotImplementedError("Subclass must implement abstract method")
        
    def speak(self):
      	print('Hello there.')
  
  
class Customer(Person):
    currentID = 1000

	def __init__(self, name):
      '''Creates a Customer object with the specified name
      ID is generated by the __createID() method
      
      raises a TypeError if name is not a string'''
      if not (isinstance(name, str)):
        	raise TypeError("Name must be a string") 
      
      Person.__init__(self, name)
      self.ID = self.__createID()
      self.checkingaccount=None
      self.savingsaccount=None

    def __createID(self):
      	'''Creates an ID for use in the __init__ method, each new Customer will have
        an ID that is one greater than the last Customer'''
      	Customer.currentID += 1
      	return Customer.currentID
      
    def returnID(self):
     	  return self.ID
        
    def addChecking(self, balance=0, apr=5.0, cashback=0.0):
        '''creates a Checking object and saves it to the Customer as a class attribute called:
        checkingaccount 
        this checking account has the values:
        balance of the account in dollars - Default = $0
        annual percentage rate of the checking account in percent - Default = 5.0%
        percent cashback with each purchase (withdraw) in percent - Default = 0.0%
        
        All arguments must be floats or ints, but the __init__ method for Checking ensures this is the case'''
        self.checkingaccount=Checking(balance, apr, cashback)

    def addSavings(self, balance, interest=0.5):
        '''creates a Savings object and saves it to the Customer as a class attribute called:
        savingsaccount 
        this checking account has the values:
        balance of the account in dollars
        interest rate of the checking account in percent - Default = 0.5%
        
        All arguments must be floats or ints, but the __init__ method for Checking ensures this is the case'''
        self.savingsaccount=Savings(balance, interest)
        
    def addLoan(self, loanAmount=1000, interest=8, paymentAmount=100):
        '''creates a Loan object and saves it to the Customer as a class attribute called: loan 
        a conditional statement ensures that it is possible for the loan to be paid back with the inputted values
        
        the Loan.__init__ method ensures that all arguments are either floats or ints'''
        if (loanAmount * (interest / 100)) >= paymentAmount:
            raise ValueError("With your inputted values it would be impossible for you to pay back your loan.")
        self.loan=Loan(loanAmount, interest, paymentAmount)

    def makeLoanPayment(self):
        '''if the loan attribute exists, calls the loan method makePayment '''
        if (self.loan == None):
            raise AttributeError("You have no loan to pay off.")
        else:
            self.loan.makePayment()
	
    def __str__(self):
        return '{} is a customer with bank ID {}'.format(self.name, self.ID)
      
    __repr__=__str__
        
    def speak(self):
      	print('LET ME WITHDRAW MY MONEY RIGHT NOW!!!')

        
class Manager(Person):
    currentID = 0

    def __init__(self, name):
      	'''Creates a Manager object with the specified name
     	ID is generated by the __createID() method
      
      	raises a TypeError if name is not a string'''
      	if not (isinstance(name, str)):
        	raise TypeError("Name must be a string") 
      
     	Person.__init__(self, name)
      	self.ID = self.__createID()

    def __createID(self):
        '''Creates an ID for use in the __init__ method, each new Manager will have
        an ID that is one greater than the last Manager'''
        if Manager.currentID == 200:
          raise ValueError("You have reached the maximum number of managers allowed.")
      	else:
          Manager.currentID += 1
          return Manager.currentID
      
    def returnID(self):
      	return self.ID
      
    def deleteAccount(self, bank, ID):
      	'''Removes a person with the given ID from the bank list by calling the removePersonFromListByID method
        
        raises a TypeError if bank is not a Bank object
        raises a TypeError if ID is not an int
        
        raises an exception if the manager is not a part of the bank (doesnt have the authority to delete from other banks)'''
        if not (isinstance(bank, Bank)):
          	raise TypeError("Bank must be a Bank object")
      	if not (isinstance(ID, int)):
          	raise TypeError("ID must be an int")
      	if not self in bank.getList():
          	raise Exception("You cannot delete a person from this bank")
            
      	bank.removePersonFromListByID(ID)
      
    def hire(self, bank, employee):
      	'''Adds a person to the list of people in the bank
        
        raises a TypeError if bank is not a Bank object
        raises a TypeError if employee is not a Teller, Assistant, or Manager object
        
        raises an Exception if the manager is not a part of the bank (cant hire a teller to another bank)'''
        if not isinstance(bank, Bank):
          	raise TypeError("Bank must be a Bank object")
        if not self in bank.getList():
          	raise Exception("You cannot hire an employee to this bank")
        if (isinstance(employee, Teller) or isinstance(employee, Assistant) or isinstance(employee, Manager)): 	
      		bank.addPersonToList(employee)
        else:
          	raise TypeError("Employee must be a Teller, Assistant, or a Manager")
        
    def findPerson(self, bank, ID):
      	'''Searches through the bank's list of people
        returns the person with ID that matches the specified parameter
        
        Prints an error message and returns None if the correct person has not been found
        
        raises a TypeError is bank is not a Bank or Id is not an int
        a Manager can call this method even if they are not a part of the bank being searched'''
        if not (isinstance(bank, Bank) and isinstance(ID, int)):
          	raise TypeError("bank must be a Bank and ID must be an int")
        
        for person in bank.getList():
          	if (person.ID == ID):
              	return person
        print("There is no person in this bank with that ID")
        return 
    
    def updateAccounts(self, bank):
      	'''Finds each customer in the banklist and then updates each of their accounts.
        If it is a savings account, the accrueInterest() method is called
        If it is a checking account, the incurPenalty() method is called
        
        bank must be a bank object
        the manager must be a member of the bank being updated'''
        if not isinstance(bank,Bank):
          	raise TypeError("bank must be a Bank")
        if not self in bank.getList():
          	raise Exception("You cannot update the accounts of this bank")
        
      	for person in bank.getList():
          	if (type(person) == Customer):
              	if (person.savingsaccount != None):
                  	person.savingsaccount.accrueInterest()
                if (person.checkingaccount != None):
                  	person.checkingaccount.incurpenalty()
    
    def speak(self):
      	print('Excuse me, but I am going to have to ask you to leave. No one speaks to my employees that way.')
        
    def __str__(self):
        return '{} is a manager with bank ID {}'.format(self.name, self.ID)
      
    __repr__=__str__

    
    
class Teller(Person):
    currentID = 200

    def __init__(self, name):
      	'''Creates a Teller object with the specified name
      	ID is generated by the __createID() method
      
      	raises a TypeError if name is not a string'''
      	if not (isinstance(name, str)):
        	raise TypeError("Name must be a string") 
      
      	Person.__init__(self, name)
      	self.ID = self.__createID()

    def __createID(self):
        '''Creates an ID for use in the __init__ method, each new Teller will have
      	an ID that is one greater than the last Teller'''
        if Teller.currentID == 600:
          raise ValueError("You have reached the maximum number of tellers allowed.")
      	else:
          Teller.currentID += 1
          return Teller.currentID
      
    def returnID(self):
      	return self.ID
      
    def addCustomer(self, customer, bank):
      	'''adds a customer to the list of people in the bank
        
        customer must be a Customer object
        bank must be a Bank object
        the teller must be a part of the bank'''
        if not isinstance(customer,Customer):
          	raiseTypeError("Customer must be a Customer object")
        if not isinstance(bank,Bank):
          	raiseTypeError("Bank must be a Bank object")
        
      	bank.getList().append(customer)
      
      
    def deposit(self, customer, amount, checkOrSave):
      	'''adds the amount specified to this Customer's checking or saving account
        
        Raises an AttributeError if an account has not yet been created for this Customer
        Raises a TypeError if customer is not a Customer or amount is not an int or float'''
        if not isinstance(customer,Customer):
          	raise TypeError("Customer must be a Customer object")
        if not (isinstance(amount,int) or isinstance(amount,float)):
          	raise TypeError("Amount must be an int or a float")
        
        if (checkOrSave == "check" or checkOrSave == "Check"):
          	if customer.checkingaccount == None:
              	raise AttrubiteError("You do not have an account to deposit into")
            else:
              	customer.checkingaccount.deposit(amount)
        if (checkOrSave == "save" or checkOrSave == "Save"):
          	if customer.savingsaccount == None:
              	raise AttrubiteError("You do not have an account to deposit into")
            else:
              	customer.savingsaccount.deposit(amount)
        


    def withdraw(self, customer, amount, checkOrSave):
      	'''removes the amount specified to this Customer's checking or saving account
        
        Raises an AttributeError if an account has not yet been created for this Customer
        Raises a TypeError if customer is not a Customer or amount is not an int or float'''
        if not isinstance(customer,Customer):
          	raise TypeError("Customer must be a Customer object")
        if not (isinstance(amount,int) or isinstance(amount,float)):
          	raise TypeError("Amount must be an int or a float")
        
        if (checkOrSave == "check" or checkOrSave == "Check"):
          	if customer.checkingaccount == None:
              	raise AttrubiteError("You do not have an account to deposit into")
            else:
              	customer.checkingaccount.purchase(amount)
        if (checkOrSave == "save" or checkOrSave == "Save"):
          	if customer.savingsaccount == None:
              	raise AttrubiteError("You do not have an account to deposit into")
            else:
              	customer.savingsaccount.withdraw(amount)

    def findPerson(self, bank, ID):
      	'''Searches through the bank's list of people
        returns the person with ID that matches the specified parameter
        
        Prints an error message and returns None if the correct person has not been found
        Raises a TypeError if bank is not a Bank or Id is not an int
        Raises an Exception if the Teller is not a part of the Bank (Tellers can only search through their bank)'''
        if not isinstance(bank,Customer):
          	raise TypeError("Bank must be a Bank object")
        if not isinstance(ID,int):
          	raise TypeError("ID must be an int")
        if not self in bank.getList():
          	raise Exception("You cannot search through the people in this Bank")
        
        for person in bank.getList():
          	if (person.getID() == ID):
              	return person
        print("There is no person in this bank with that ID")
        return 
    
    def speak(self):
      	print('Is there anything that I can help you with today? :)')
    
    def __str__(self):
        return '{} is a teller with bank ID {}'.format(self.name, self.ID)
      
    __repr__=__str__

        
class Assistant(Person):
  	currentID = 600
    
    def __init__(self, name):
      	'''Creates an Assistant object with the specified name
      	ID is generated by the __createID() method
      
      	raises a TypeError if name is not a string'''
      	if not (isinstance(name, str)):
        	raise TypeError("Name must be a string") 
      
      	Person.__init__(self, name)
      	self.ID = self.__createID()
        
    def __createID(self):
      	'''Creates an ID for use in the __init__ method, each new Assistant will have
        an ID that is one greater than the last Assistant'''
        if Assistant.currentID == 1000:
          raise ValueError("You have reached the maximum number of assistants allowed.")
      	else:
          Assistant.currentID += 1
          return Assistant.currentID
      
    def returnID(self):
      	return self.ID  
      
    def getCoffee(self):
      '''coffee from http://www.ascii-art.de/ascii/c/coffee.txt'''
      coffee = "  .-~~-.\n,|`-__-'|\n||      |\n`|      |\n  `-__-'"   
      print (coffee)
    
    def speak(self):
      	print('The list of accounts have been updated and placed on your desk.')
    
    def __str__(self):
        return '{} is an assistant with bank ID {}'.format(self.name, self.ID)
      
    __repr__=__str__
