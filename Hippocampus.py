import re

summarization_counter = 0
summarized_interactions = "" 

def count_lines(short_memory):
    with open(short_memory, 'r') as file:
        return sum(1 for line in file)
    

def append_input_to_short(filename="short_term_memory.txt"):
    global merchant_response, player_response
    with open(filename, "a") as file:
        file.write("The Player: " + player_response + "\n\n")
        file.write("You: " + merchant_response + "\n\n")

def short_lose_memory(filename="short_term_memory.txt"):
    with open(filename, 'r') as file:
        lines = file.readlines()

    distant = lines[:4]
    with open(filename, 'w') as file:
        file.writelines(lines[4:])

    return distant

def summarized_long_memory(filename="long_term_memory.txt"):
    global summarized_interactions 
    with open(filename, 'r') as file:
        lines = file.readlines()

    summarized_interactions = ''.join(lines[:24]).replace('\n', ' ') # Replace this with the Summarization Bot with a specific format in the future. 
    # Bot instructions here that take in summarization_interactions

    
    with open(filename, 'w') as file: # I think I don't need to write this to a file, as it can just be stored, interpreted by the bot, and then stored within a file
        file.writelines(lines[24:])
        file.write(summarized_interactions + '\n')
    return summarized_interactions

def short_to_long(distant, filename='long_term_memory.txt'):
    global summarization_counter 
    with open(filename, 'a') as file:
        file.writelines(distant)
    count_to_summarization(filename='Pond.txt') 
    #print("APPENDED")

def load_values(filename='Pond.txt'):
    global player_response, merchant_response
    with open(filename, 'r') as file:
        content = file.read()

        player_response_search = re.search(r'Player Filtered Response: (.*)', content, re.M)
        player_response = player_response_search.group(1).strip() if player_response_search else 'E'

        merchant_response_search = re.search(r'Mercali Filtered Response: (.*)', content, re.M)
        merchant_response = merchant_response_search.group(1).strip() if merchant_response_search else 'E'


def count_to_summarization(filename='Pond.txt'):
    global summarization_counter
    with open(filename, 'r') as file:
        content = file.read()
        summarization_counter_search = re.search(r'Count To Summarization: (\d+)', content, re.M)
        summarization_counter = int(summarization_counter_search.group(1)) if summarization_counter_search else 5

    summarization_counter += 1

    if summarization_counter >= 5:
        summarized_long_memory()
        summarization_counter = 0
        #print("SUMMARIZED") 
    
    content = re.sub(r'Count To Summarization: \d+', f'Count To Summarization: {summarization_counter}', content)

    with open(filename, 'w') as file:
        file.write(content) 


## Debugging Purposes 
#clear_txt = input("Clear Files? y, n: ")
#if clear_txt == "y":
#    open('short.txt', 'w').close()
#    open('long.txt', 'w').close()
#    print("Files Cleared")
#elif clear_txt == "n":
#    print("File NOT Cleared")
#else:
#    print("Input wrong.")

#merchant_response = input("Mercali: ")
#player_response = input("Player: ")

load_values() 
append_input_to_short()

short_memory = 'short_term_memory.txt'
#print(f'The file {short_memory} has {count_lines(short_memory)} lines.')
total_short_interactions = (count_lines(short_memory) // 2)
#print(f'The file {short_memory} has {total_short_interactions} total interactions.')

## The earliest interaction gets transfered to the long term memory 
#if total_short_interactions >= 12: # Each interaction has 4 lines; was set to 4 
#    distant_lines = short_lose_memory()
#    short_to_long(distant_lines)
#    print("Transferred")
#    print(f'Suma Counter: {summarization_counter}') 
#else:
#    print("Not enough lines to transfer.")
    
    
    
    
    
