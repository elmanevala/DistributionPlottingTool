# init.py

import sys
from core_functions import read_data, sizes, classification_probs, argument_categories, argument_class_compare, by_gender, uk_lc, uk_selected, ua_parties, sl_parties


def main():
    # load data
    meta, arguments = read_data()
    print("Data loaded successfully!")
    print('List all commands with c')

    while True:
        print('')
        # Get user input
        command = input("Enter a command: ").strip().lower()

        if command == "sizes":
            try:
                threshold = float(input("Enter a threshold value for cleaning data: "))
                sizes(threshold, arguments)  # Call the sizes function from core_functions.py
            except ValueError:
                print("Please enter a valid numeric threshold.")
        
        elif command == 'c':
            print('')
            print('arg_class (GB, UA, SI) - save a pie chart of argument class distribution from a chosen country')
            print('arg_comparison - save a bar chart somparing the argument class distributions between different countries')
            print('c - list all commands')
            print('gender - save a bar chat comparing argument classes between genders')
            print('party (GB_lc, GB_selected, UA, SI) - distribution of argument classes by parties')
            print('pred_probs - save an image of the mean and standard deviations of the argument dataset prediction probalities')
            print('sizes - show the sizes of arguments dataset for different countries with a specified prediction probability threshold')
            print('quit - quit the program')
            print('')

        elif command == "party":
            try:
                option = input("Enter country/parties of interest (GB_lc, GB_selected, UA, SI): ")
                if (option == 'GB_lc'):
                    save_str = input("Enter a filename: ")
                    uk_lc(meta, save_str)  
                    print('The bar chart is saved in the figure directory as ' + save_str + '.png')
                elif (option == 'GB_selected'):
                    save_str = input("Enter a filename: ")
                    uk_selected(meta, save_str)  
                    print('The bar chart is saved in the figure directory as ' + save_str + '.png')
                elif (option == 'UA'):
                    save_str = input("Enter a filename: ")
                    ua_parties(meta, save_str)  
                    print('The bar chart is saved in the figure directory as ' + save_str + '.png')
                elif (option == 'SI'):
                    save_str = input("Enter a filename: ")
                    sl_parties(meta, save_str)  
                    print('The bar chart is saved in the figure directory as ' + save_str + '.png')
            except ValueError:
                print("Please enter a valid country and file name.") 

        elif command == "gender":
            try:
                save_str = input("Enter a filename: ")
                by_gender(meta, save_str)  
                print('The bar chart is saved in the figure directory as ' + save_str + '.png')
            except ValueError:
                print("Please enter a valid file name.")   


        elif command == "arg_comparison":
            try:
                save_str = input("Enter a filename: ")
                argument_class_compare(save_str, arguments)   
                print('The bar chart is saved in the figure directory as ' + save_str + '.png')
            except ValueError:
                print("Please enter a valid file name.")   

        elif command == "arg_class":
            try:
                country = input('Enter country (GB, UA, SI): ')
                save_str = input("Enter a filename: ")
                argument_categories(country, save_str, arguments)   
                print('The figure for ' + country + ' is saved in the figure directory as ' + save_str + '.png')
            except ValueError:
                print("Please enter a valid country and file name.")    

        elif command == "pred_probs":
            try:
                save_str = input("Enter a filename: ")
                classification_probs(arguments, save_str)  
                print('The figure is saved in the figure directory as ' + save_str + '.png')
            except ValueError:
                print("Please enter a valid file name.")

        elif command == "quit":
            print("Exiting the program.")
            sys.exit()

        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()
