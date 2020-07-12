import patent_search as ps

# Welcomes user, gives them options.
print("""\
Hello! Welcome to Patent Word Count v0.1.0-alpha

This program can:
    • Find patent information
    • Find the most used words in a patent
    • Find patent numbers and other information from given criteria\

Remember you can press ctrl+c at any time to end operations.
""")
fields = ps.search_for({"fields"})
valid_response = False
# This asks the user which they want to do of the above choices.
while valid_response == False:
    do_choice = input("Which of these would you like to do?\n\
Enter 1, 2, or 3.\n")
    # Response validation:
    try:
        do_choice = int(do_choice)
        if do_choice in [1, 2, 3]:
            valid_response = True
        else:
            raise ValueError
    except ValueError:
        print("Invalid response, please try again.")
# This function allows the user to enter whatever they want for whichever
# fields they want. Set as a function so I can use it multiple times.
# Returns a dictionary of criteria.
def enter_data():
    """Asks the user to enter data relevant to patents.
    Accepts no arguments."""
    # Setting values before the loop.
    enter_data = True
    criteria = dict()
    # Prints fields, asks user to select one. Also displays chosen values.
    while enter_data == True:
        # Prints the options, and their set values.
        print(f"Please select from the following field options:")
        for field in fields:
            if field in criteria:
                print(f"    {fields.index(field) + 1}. {field:.<20}{criteria[field]}")
            else:
                print(f"    {fields.index(field) + 1}. {field:}")
        print("You can select by either typing the name of the field,",\
              "or its number in the list.")
        # Response validation:
        valid_response = False
        while valid_response == False:
            choice = input("\n").lower()
            try:
                choice = int(choice)
                selected_field = fields[choice - 1]
                valid_response = True
            except ValueError:
                try:
                    selected_field = fields[fields.index(choice)]
                    valid_response = True
                except ValueError:
                    print(f"\"{choice}\" is not an option. Please try again.")
                pass
        # Tells the user what the field is set to, or simply which field they
        # selected.
        if selected_field in criteria:
            print(f"You have selected {selected_field}, which is currently",\
                  f"set to: {criteria[selected_field]}.\nWhat would you like to",\
                   "change it to?")
        else:
            print(f"You have selected \"{selected_field}\".",\
                    "What would you like to set it to?", sep='\n')
        # More response validation:
        valid_response = False
        while valid_response == False:
            choice = input(f"Set \"{selected_field}\" to: ")
            while True:
                print(f"You have chosen to set \"{selected_field}\" to ",\
                      f"\"{choice}\".")
                ans = input("Are you sure? (\"y\"/\"n\")\n")
                if ans == "y":
                    valid_response = True
                    break
                elif ans == "n":
                    break
                else:
                    print("You must enter \"y\" or \"n\".")
        # Saves their changes:
        criteria.update({selected_field:choice})
        # Asks if they'd like to make more changes.
        while True:
            print("Enter more criteria? (y/n)")
            ans = input("")
            if ans == "y":
                break
            elif ans == "n":
                enter_data = False
                break
            else:
                print("You must enter \"y\" or \"n\".")
        # Returns the dictionary of what the user set.
    return criteria

# If the user asked to find patent information...
if do_choice == 1:
    print("Would you like to enter a patent number, a document ID, or search",\
          "for something else? Enter ")
    criteria = enter_data()
    print("Getting patent numbers...")
    # Gets the numbers.
    try:
        numbers = ps.get_numbers(criteria)
        # For some reason, not always was no numbers returning an error,
        # so I added this which will just say so.
        if len(numbers) == 0:
            raise ValueError
    except KeyboardInterrupt:
        print("Cancelling now...")
        exit()
    except:
        print(f"No patents were found for: {criteria}.")
        exit()
    print("Getting patent pages... This may take a while - especially if",\
          "you found a lot of patents. It also may use up a large",\
          "amount of memory.")
    patent_results = []
    # Gets every patent via Google Patents.
    try:
        for number in numbers:
            print(f"Downloading page #{numbers.index(number)+1}",\
                  f"of {len(numbers)}...")
            patent = ps.get_patent(document_ID = number)
            patent_results.append(patent)
    except KeyboardInterrupt:
        # If the user cancels the process, this will still return what data it
        # has gathered. I chose this, as sometimes searches will return 100s
        # of numbers.
        print("Cancelling...\nPrinting results...")
        for patent in patent_results:
            print(f"Patent #{patent_results.index(patent)+1} of",\
                  f"{len(patent_results)}")
            for section in patent:
                section_title = str(section)
                section_content = str(patent[section]).replace('\n','')
                print(f"{section_title:15}: {section_content}")
        exit()
    print("Finished. Printing results. If you searched for a large number,",\
          "this may take a while and could use up a lot of memory.")
    # Prints each result -- "Patent #x of y" and then each {section:15}:
    # {content}.
    for patent in patent_results:
        print(f"Patent #{patent_results.index(patent)+1} of",\
              f"{len(patent_results)}")
        for section in patent:
            section_title = str(section)
            section_content = str(patent[section]).replace('\n','')
            print(f"{section_title:15}: {section_content}")
    # Ends the program.
    exit()
# If the user asked to get most used words...
elif do_choice == 2:
    # Asks if they'd like to search multiple, or just one.
    valid_response = False
    while valid_response == False:
        print("Would you like to use a specific patent,",\
              "or search for multiple?")
        do_choice = input("Enter 1, or 2.\n")
        try:
            do_choice = int(do_choice)
            if do_choice == 1:
                while valid_response == False:
                    # Asks for patent number - barely validates.
                    number = input("Please input the number of the patent you'd "\
                                   "like to use.\n")
                    if number[:2] != "US":
                        number = "US" + my_st
                    if number != "":
                        numbers = [number]
                        valid_response = True
                    else:
                        print("Please enter a number.")
            elif do_choice == 2:
                print("Please enter your criteria: ")
                criteria = enter_data()
                numbers = ps.get_numbers(criteria)
                valid_response = True
            else:
                raise ValueError
        except ValueError:
            print("Please enter 1 for a specific patent, or 2 to search for",\
                  "many patents.")
            valid_response = False
    section = input("Would you like to search a specific section? "\
                    "If so, enter the name below. Otherwise, press enter.\n")
    min_return = input("What would you like to be the minimum number of "\
                       "occurances to be recorded?\n")
    counts = {}
    # Prints "counting" and the percent complete just to signal to the user
    # that something is happening.
    print("\nCounting...\n")
    for number in numbers:
        try:
            patent = ps.get_patent(document_ID = number)
        except:
            print(f"The patent corresponding to the number {number}",\
                   "could not be found.")
            continue
        if section != '':
            try:
                patent_counts = ps.count_words(str(patent[section]))
                for word in patent_counts:
                    if word in counts:
                        counts[word] += patent_counts[word]
            except KeyError:
                print(f"The section \"{section}\" does not exist.")
                break
        else:
            for section in patent:
                section_counts = ps.count_words(str(patent[section]))
                for word in section_counts:
                    if word in counts:
                        counts[word] += section_counts[word]
                    else:
                        counts.update({word:section_counts[word]})
        print(f"Counting... {int((numbers.index(number)/len(numbers))*100)}% complete.")
    # Sorts the counts in order of greatest to least.
    counts = {k: v for k, v in sorted(counts.items(),\
                                      key=lambda item: item[1], reverse=True)}
    # Finds the longest word... This was oddly difficult lol.
    max_length = len(max(counts, key = lambda word: len(word)))
    for word in counts:
        if word == "Total words":
            print(f"{word:{max_length}}: {counts[word]:<6,}")
            continue
        if counts[word] > int(min_return):
            print(f"{word:{max_length}} appears {counts[word]:^6,} times.")
    exit()
# If the user asked to find numbers etc. ...
elif do_choice == 3:
    criteria = enter_data()
    results = ps.search_for(criteria)
    print(f"Here are the results of your search for: {criteria}.")
    for item in results:
        print(f"{f'Result: {str(results.index(item))} of {str(len(results))}.':-^120}")
        for field in item:
            print(f"{(field+':'):20}{item[field]}")
    exit()
else:
    print(f"Your input, \"{do_choice}\", was invalid. Please try again,",\
           "inputing only 1, 2, or 3.")
    exit()
