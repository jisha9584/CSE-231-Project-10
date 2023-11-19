###########################################################
#  Computer Project #10
#
#    define functions
#       1. intialize
#       2. display
#       3. stock to waste
#       4. waste to foundation 
#       5. waste to tableau
#       6. tableau to foundation
#       7. tableau to tableau
#       8. parse_option
#       9. check win 
#    define main
#       start by initializing the board (tableau, stock, foundation, waste)
#       Display the MENU
#       Display the starting board
#       Prompt for an option and check the validity of the input using the parse option function.
#       options:
#           if option == ‘XX s d’:
#               If the move was a failure, print an error message: "\nInvalid move!\n"
#               If a move was to the foundation and it was successful, check to see if the user won; if so print, “You won!”, display the winning board, and stop the game. 
#               If the user did not win and the move was successful just display the board. 
#               If a move was to tableau, just display the board.
#           if option == 'WX N':
#               If the move was a failure, you should print an error message: "\nInvalid move!\n".
#               If a move was to the foundation and it was successful, check to see if the user won; if so print, “You won!”, display the winning board, and stop the game.
#               If the user did not win and the move was successful just display the board. • If a move was to tableau, just display the board.
#           if option == 'SW':
#               If a move is successful, display the board.
#               If the move was a failure, print an error message: "\nInvalid move!\n".
#           if option == 'R':
#               Restart the game by initializing the board (after shuffling). Display the MENU and display the board.
#           if option == 'H':
#               display the menu of choices.
#           if option == 'Q':
#               Quit the program
#           The program should repeat until the user won or quit the game.
###########################################################

from cards import Card, Deck

MENU ='''Prompt the user for an option and check that the input has the 
       form requested in the menu, printing an error message, if not.
       Return:
    TT s d: Move card from end of Tableau pile s to end of pile d.
    TF s d: Move card from end of Tableau pile s to Foundation d.
    WT d: Move card from Waste to Tableau pile d.
    WF d: Move card from Waste to Foundation pile d.
    SW : Move card from Stock to Waste.
    R: Restart the game (after shuffling)
    H: Display this menu of choices
    Q: Quit the game        
    '''
def initialize():
    '''
    The function has no parameters and returns the starting state of the game\
        with the four data structures initialized as described above.
    Parameters: None
    Returns: tableau_list, stock, foundation_list, waste
    '''
    foundation_list = [[],[],[],[]]
    tableau_list = [[],[],[],[],[],[],[]]
    stock = Deck() #stock is of type Class Deck
    stock.shuffle() #shuffle the stock when you create it
    for i in range(7):
        for j in range(i,7):
            tableau_list[j].append(stock.deal())
    
    for i in range(len(tableau_list)):
        for card in tableau_list[i]:
            card.flip_card()
        #all tableau cards face down except last cards in each column
        tableau_list[i][-1].flip_card() 
        
    waste = []
    waste.append(stock.deal())
    return tableau_list, stock, foundation_list, waste
    
def display(tableau, stock, foundation, waste):
    """ display the game setup """
    stock_top_card = "empty"
    found_top_cards = ["empty","empty","empty","empty"]
    waste_top_card = "empty"
    if len(waste):
        waste_top_card = waste[-1] 
    if len(stock):
        stock_top_card = "XX" #stock[-1]
    for i in range(4):
        if len(foundation[i]):
            found_top_cards[i] = foundation[i][-1]
    print()
    print("{:5s} {:5s} \t\t\t\t\t {}".format("stock","waste","foundation"))
    print("\t\t\t\t     ",end = '')
    for i in range(4):
        print(" {:5d} ".format(i+1),end = '')
    print()
    print("{:5s} {:5s} \t\t\t\t".format(str(stock_top_card), \
                                        str(waste_top_card)), end = "")
    for i in found_top_cards:
        print(" {:5s} ".format(str(i)), end = "")
    print()
    print()
    print()
    print()
    print("\t\t\t\t\t{}".format("tableau"))
    print("\t\t ", end = '')
    for i in range(7):
        print(" {:5d} ".format(i+1),end = '')
    print()
    # calculate length of longest tableau column
    max_length = max([len(stack) for stack in tableau])
    for i in range(max_length):
        print("\t\t    ",end = '')
        for tab_list in tableau:
            # print card if it exists, else print blank
            try:
                print(" {:5s} ".format(str(tab_list[i])), end = '')
            except IndexError:
                print(" {:5s} ".format(''), end = '')
        print()
    print()

def stock_to_waste( stock, waste ):
    '''
    moves the card from stock to waste
    stock: the data structure representing the stock
    waste: the data structure representing the waste
    return: bool
    '''
    #check that there are cards in the stock before trying to move one to the waste
    if not stock.is_empty(): #stock is of type Class Deck
        waste.append(stock.deal())
        return True #True if the move was done successfully
    else:
        return False
  
    
def is_red(card):
    '''
    checks if the card is red in color 
    card: the card being color checked
    return: bool
    '''
    if card.suit() == 2 or card.suit() == 3:
        return True
    return False

def is_black(card):
    '''
    checks if the card is black in color 
    card: the card being color checked
    return: bool
    '''
    if card.suit() == 1 or card.suit() == 4:
        return True
    return False
          
    
def waste_to_tableau( waste, tableau, t_num ):
    '''
    moves the card from waste to tableau 
    waste: the data structure representing the waste
    tableau: the data structure representing the tableau 
    t_num: a column number (the correct index in the tableau)
    return bool
    '''
    if len(waste) != 0:
        card = waste[-1]
        #if the tableau is empty, only king can be placed in it 
        if tableau[t_num] == []:
            if card.rank() == 13:
                tableau[t_num].append(card)
                waste.remove(card)
                return True
            else:
                return False
        else:
    #check if the colors are different, defined two functions for that reason. 
            card_2 = tableau[t_num][-1]
            if ((is_red(card) and is_black(card_2)) or (is_red(card_2) and \
                                                        is_black(card))) and \
                card.rank() + 1 == card_2.rank() :
                tableau[t_num].append(card)
                waste.remove(card)
                return True
            else:
                return False
    else: 
        return False

def waste_to_foundation( waste, foundation, f_num ):
    '''
    moves the card from waste to foundation
    waste: the data structure representing the waste
    foundation: the data structure representing the foundations
    f_num: a foundation number (the correct index in the foundation)
    return: bool 
    '''
    
    if len(waste) != 0:
        card = waste[-1]
        if foundation[f_num] == []:
        #if foundation is empty, ace should be placed in the foundation 
            if card.rank() == 1:
                foundation[f_num].append(card)
                waste.remove(card)
                return True
            else:
                return False
        elif len(foundation[f_num]) > 0 :
        #makes sure that the suits are same and that the rank is only one above
            if card.suit() == foundation[f_num][-1].suit() and card.rank() - 1\
                == foundation[f_num][-1].rank():
                foundation[f_num].append(card)
                waste.remove(card)
                return True
            else:
                return False
    else: 
        return False
        
def tableau_to_foundation( tableau, foundation, t_num, f_num ):
    '''
    moves the cards from tableau to foundation.
    tableau: the data structure representing the tableau, 
    foundation: the data structure representing the foundations
    t_num: a column number
    f_num: a foundation number
    return: bool
    '''
    if len(tableau[t_num]) != 0: #for normal cards
        card_tableau = tableau[t_num][-1]
        if len(foundation[f_num]) != 0:
            card_foundation = foundation[f_num][-1]
            if card_tableau.rank() - 1 == card_foundation.rank() and \
                card_tableau.suit() == card_foundation.suit():
                foundation[f_num].append(card_tableau)
                tableau[t_num].remove(card_tableau)
                #check if tablea is not empty and face up 
                if tableau[t_num] != [] and not \
                    tableau[t_num][-1].is_face_up():
                    card_tableau = tableau[t_num][-1]
                    card_tableau.flip_card() #flip the new last card
                return True

            else:
                return False
        elif foundation[f_num] == []: #checking for ace conditions
            if card_tableau.rank() == 1:
                foundation[f_num].append(card_tableau)
                tableau[t_num].remove(card_tableau)
                #check if tablea is not empty and face up 
                if tableau[t_num] != [] and not \
                    tableau[t_num][-1].is_face_up():
                    card_tableau = tableau[t_num][-1]
                    card_tableau.flip_card() #flip the new last card
                return True
            else:
                return False    
        else: 
            return False
    else:
        return False

def tableau_to_tableau( tableau, t_num1, t_num2 ):
    '''
    moving a card from tableau to tableau 
    tableau: the data structure representing the tableau, 
    t_num1: a source column number,
    t_num2: a destination column number.
    return: bool 
    '''
    #if tableau is not empty, check for colors being different.     
    if len(tableau[t_num2]) != 0:
        card_2 = tableau[t_num2][-1]
        if tableau[t_num1] != []:
            card = tableau[t_num1][-1]
            if ((is_red(card) and is_black(card_2)) or (is_red(card_2) and \
                                                        is_black(card))) and \
                card.rank() + 1 == card_2.rank() : #rank needs to be one higher
                tableau[t_num2].append(card) #add card to new location 
                tableau[t_num1].remove(card) #remove card from old location 
                if tableau[t_num1] != [] and not \
                    tableau[t_num1][-1].is_face_up():
                    card_tableau = tableau[t_num1][-1]
                    card_tableau.flip_card() #flip the new last card
                return True
            else:
                return False
        else:
            return False
        
    elif len(tableau[t_num2]) == 0:
        if tableau[t_num1] != []:
            card = tableau[t_num1][-1]
            #codition for king
            if card.rank() == 13:
                tableau[t_num2].append(card) #add card to new location 
                tableau[t_num1].remove(card) #remove card from old location
                if tableau[t_num1] != [] and not \
                    tableau[t_num1][-1].is_face_up():
                    card_tableau = tableau[t_num1][-1]
                    card_tableau.flip_card() #flip the new last card
                return True
            else:
                return False
        else:
            return False     

def check_win (stock, waste, foundation, tableau):
    '''
    checks if the user won the game
    stock: the data structure representing the stock
    waste: the data structure representing the waste
    foundation: the data structure representing the foundation
    tableau: the data structure representing the tableau
    return: bool
    '''
    #can use .is_empty for stock becasue it is type Class Deck
    if len(waste) == 0 and stock.is_empty() and len(tableau[0]) == 0:
        return True
    else:
        return False

def parse_option(in_str):
    '''Prompt the user for an option and check that the input has the 
           form requested in the menu, printing an error message, if not.
           Return:
        TT s d: Move card from end of Tableau pile s to end of pile d.
        TF s d: Move card from end of Tableau pile s to Foundation d.
        WT d: Move card from Waste to Tableau pile d.
        WF d: Move card from Waste to Foundation pile d.
        SW : Move card from Stock to Waste.
        R: Restart the game (after shuffling)
        H: Display this menu of choices
        Q: Quit the game        
        '''
    option_list = in_str.strip().split()
    
    opt_char = option_list[0][0].upper()
    
    if opt_char in 'RHQ' and len(option_list) == 1:  # correct format
        return [opt_char]
    
    if opt_char == 'S' and len(option_list) == 1:
        if option_list[0].upper() == 'SW':
            return ['SW']
    
    if opt_char == 'W' and len(option_list) == 2:
        if option_list[0].upper() == 'WT' or option_list[0].upper() == 'WF':
            dest = option_list[1] 
            if dest.isdigit():
                dest = int(dest)
                if option_list[0].upper() == 'WT' and (dest < 1 or dest > 7):
                    print("\nError in Destination")
                    return None
                if option_list[0].upper() == 'WF' and (dest < 1 or dest > 4):
                    print("\nError in Destination")
                    return None
                opt_str = option_list[0].strip().upper()
                return [opt_str,dest]
                               
    if opt_char == 'T' and len(option_list) == 3 and option_list[1].isdigit() \
        and option_list[2].isdigit():
        opt_str = option_list[0].strip().upper()
        if opt_str in ['TT','TF']:
            source = int(option_list[1])
            dest = int(option_list[2])
            # check for valid source values
            if opt_str in ['TT','TF'] and (source < 1 or source > 7):
                print("\nError in Source.")
                return None
            #elif opt_str == 'MFT' and (source < 0 or source > 3):
                #print("Error in Source.")
                #return None
            # source values are valid
            # check for valid destination values
            if (opt_str =='TT' and (dest < 1 or dest > 7)) \
                or (opt_str == 'TF' and (dest < 1 or dest > 4)):
                print("\nError in Destination")
                return None
            return [opt_str,source,dest]

    print("\nError in option:", in_str)
    return None   # none of the above


def main():   
    #start by initializing the board
    tableau, stock, foundation, waste = initialize() 
    print(MENU) #Display the MENU
    
    while True:
        #starting board (use the display() function).
        display(tableau, stock, foundation, waste)
        #Prompt for an option and check the validity of the input using the parse_option function.
        prompt = input("\nInput an option (TT,TF,WT,WF,SW,R,H,Q): ")
        prompt = parse_option(prompt)
        
        if prompt is None:
            continue 

        #move a card from source s to destination d depending on what is
        elif prompt[0] == 'TT':
            s = prompt[1] - 1
            d = prompt[2] - 1
            TT = tableau_to_tableau( tableau, s, d )
            #If the move was a failure, print an error message
            if TT != True:
                print("\nInvalid move!\n")
        
        #move a card from waste to a destination N depending on what is
        elif prompt[0] == 'WT':
            N = prompt[1] - 1
            WT = waste_to_tableau( waste, tableau, N )
            #If the move was a failure, print an error message
            if WT == False:
                print("\nInvalid move!\n")
        
        #move a card from waste to a destination N depending on what is
        elif prompt[0] == 'WF':
            N = prompt[1] - 1
            WF = waste_to_foundation( waste, foundation, N )
            if WF == False:
                #If the move was a failure, print an error message
                print("\nInvalid move!\n")
            #If a move was to the foundation and it was successful, check to see if the user won
            elif check_win(stock, waste, foundation, tableau) == True: 
                print("You won!")
                display(tableau, stock, foundation, waste)
                break

        #move a card from Stock to Waste
        elif prompt[0] == 'SW':
            option = stock_to_waste(stock, waste)
            #If the move was a failure, print an error message
            if option == False:
                print("\nInvalid move!\n") 

        #move a card from source s to destination d depending on what is
        elif prompt[0] == 'TF':
            s = prompt[1] - 1
            d = prompt[2] - 1
            TF = tableau_to_foundation( tableau, foundation, s, d )
            #If the move was a failure, print an error message
            if TF != True:
                print("\nInvalid move!\n")
            #If a move was to the foundation and it was successful, check to see if the user won
            elif check_win(stock, waste, foundation, tableau) == True: 
                print("You won!")
                display(tableau, stock, foundation, waste)
                break
        #restart the game by initializing the board (after shuffling)
        elif prompt[0] == 'R':
            tableau, stock, foundation, waste = initialize()
            print(MENU)

        #display the menu of choices
        elif prompt[0] == 'H':
            print(MENU)

        #quit the game
        elif prompt[0] == 'Q':
            break
                
            
            
        
if __name__ == '__main__':
     main()