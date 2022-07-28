import os
from fx_rate_repository import FxRateRepository


#decalaring global variable
global fx_rate
fx_rate = None

fxRateRepository = FxRateRepository()

# displaying current rate
def display_rate():
    print(
    '''
            +======================+
            ||  List of FX Rate   ||
            +======================+
    '''
        )
    for entry in fxRateRepository.get_fx_rate().get("currencies"):
        print("-" * 20)
        print("+ {} | {} | {} +".format(
            entry.get("baseCurr"), 
            entry.get("foreign"), 
            entry.get("rate")))
        print("-" * 20)

# adding a new rate data
def add_rate():
    print("------------------------")
    print("----- ADD NEW RATE -----")
    baseCurr = input("Base currency: ")
    foreign = input("Foreign currency: ")
    rate = float(input("FX Rate: "))
    new_entry = {
        "baseCurr" : baseCurr,
        "foreign" : foreign,
        "rate" : rate
    }
    fxRateRepository.add_new_fx_rate(new_entry)

# seach
def search_fx_rate(operation):
    print("Search fx rate: ")
    base_curr = input("\tBase currency: ")
    foreign_curr = input("\tForeign currency: ")
    result = fxRateRepository.find_fx_rate(base_curr, foreign_curr)
    
    if len(result) > 1:
        display_search_result(result)
        while True:
            id = int(input("Enter fx ID to {} [1-{}]:".format(operation, len(result))))
            if id > len(result):
                print("Invalid selection, try again")
            else:
                record_for_edit = result[id -1]
                break
    elif len(result) == 1:
        record_for_edit = result[0]
    else:
        print("-----ERROR: CURRENCY NOT FOUND!")
    
    return record_for_edit

# update exising rate
def update_rate():
    print("------------------------")
    print("---- UPDATE A RATE -----")
    display_edit_screen(search_fx_rate("Edit"))
    
#Edit screen and functions
def display_edit_screen(record_for_edit):
    get_user_input = lambda input, default : input if input != "" else default
    base_curr = record_for_edit.get("baseCurr")
    foreign_curr = record_for_edit.get("foreign")
    fx_rate = record_for_edit.get("rate")
    
    #  edit fx details screen
    print("-----Edit FX Rate-----")
    
    base_curr = get_user_input(input("New base currency [{}]: ".format(base_curr)), base_curr)
    print(base_curr)
    
    foreign_curr = get_user_input(input("New foreign currency [{}]: ".format(foreign_curr)), foreign_curr)
    print(foreign_curr)
    
    fx_rate = float(get_user_input(input("New FX rate [{}]: ".format(fx_rate)), fx_rate))
    print(fx_rate)
    
    record_for_edit["baseCurr"] = base_curr
    record_for_edit["foreign"] = foreign_curr
    record_for_edit["rate"] = fx_rate
    
    fxRateRepository.update_fx_rate(record_for_edit)
    
# deleting existing rates
def delete_rate():
    print("Delete fx rate")
    result = search_fx_rate("Delete")
    
    if result != None:
        while True:
            response = input("Delete FX rate (Y/N)?")
            if response.lower() == "y":
                print("Record for deletion -> {}".format(result))
                fxRateRepository.delete_fx_rate(result)
                print("Deleted succesfully!")
                break
            elif response.lower()=="n":
                input("User cancelled, press enter key to quit.")
                break
            else:
                print("Invalid selection.")
    
    
#displaying search results           
def display_search_result(result):
    index = 1
    for entry in result:
        print("{} | {}\t | {}\t | {}".format(index, entry.get("baseCurr"), entry.get("foreign"), entry.get("rate")))
        index = index + 1

#clear screen in terminal
def clear_screen():
    os.system("cls")

#displaying main screen and input 
def display_menu():
    print("\t-----FOREX APP-----")
    print("\t[1] Display all fx rates.")
    print("\t[2] Add new rate")
    print("\t[3] Update existing rate")
    print("\t[4] Delete existing rate")
    selection = input("Enter choice: ")
    
    if selection == "1":
        clear_screen()
        display_rate()
    elif selection == "2":
        add_rate()
    elif selection == "3":
        clear_screen()
        update_rate()
    elif selection == "4":
        clear_screen()
        delete_rate()
    else:
        clear_screen()
    
display_menu()
# add_rate()