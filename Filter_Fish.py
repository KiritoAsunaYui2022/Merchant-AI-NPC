import re
import runpy

filename = "Pond.txt"

def find_bracket_contents(user_msg):
    bracket_list = []  
    pattern = r'<(.*?)>'
    matches = re.findall(pattern, user_msg)
    for match in matches:
        bracket_list.append(f'<{match}>')
    return bracket_list 

def find_vertical_contents(user_msg):
    vertical_list = [] 
    pattern = r'\|(.*?)\|'
    matches = re.findall(pattern, user_msg)
    for match in matches:
        vertical_list.append(f'|{match}|')
    return vertical_list 

def combine_contents(bracket_list, vertical_list):
    combined_list = ','.join([b + v for b, v in zip(bracket_list, vertical_list)])
    return combined_list

def main(user_msg):
    bracket_list = find_bracket_contents(user_msg) 
    vertical_list = find_vertical_contents(user_msg)
    commands_input = combine_contents(bracket_list, vertical_list)
    return commands_input

def load_initial_values():
    global filtered_msg, filtered_paid_msg, filtered_commands
    with open(filename, 'r') as file:
        content = file.read()
        filtered_msg_search = re.search(r'Player Filtered Response: (.*)', content, re.M)
        filtered_paid_msg_search = re.search(r'Player Filtered With Paid Response: (.*)', content, re.M)
        filtered_commands_search = re.search(r'Player Commands: (.*)', content, re.M)

        filtered_msg = filtered_msg_search.group(1).strip() if filtered_msg_search else 'E'
        filtered_paid_msg = filtered_paid_msg_search.group(1).strip() if filtered_paid_msg_search else 'E'
        filtered_commands = filtered_commands_search.group(1).strip() if filtered_commands_search else 'E'

def update_file():
    with open(filename, 'r') as file:
        content = file.read()

    content = re.sub(r'Player Filtered Response: .*', f'Player Filtered Response: {filtered_msg}', content, flags=re.M)
    content = re.sub(r'Player Filtered With Paid Response: .*', f'Player Filtered With Paid Response: {filtered_paid_msg}', content, flags=re.M)
    content = re.sub(r'Player Commands: .*', f'Player Commands: {filtered_commands}', content, flags=re.M)

    with open(filename, 'w') as file:
        file.write(content)

def remove_bra_ver_and_if_paid(user_msg):
    global filtered_msg, filtered_paid_msg 
    
    pattern = r'<.*?>|\|.*?\|'  # Pattern to match both <...> and |...| contents
    
    action = "<Hands The Merchant Gold Coins>" in user_msg  # Detecting specific action
    
    filtered_msg = re.sub(pattern, '', user_msg)  # Removing patterns to create filtered_msg
    if action:
        filtered_paid_msg = filtered_msg + "<Paid>"
    else:
        filtered_paid_msg = filtered_msg

#if __name__ == "__main__":
load_initial_values()
user_msg = input("Your message: ")
filtered_commands = main(user_msg)  # Extract commands

remove_bra_ver_and_if_paid(user_msg)  # Update filtered messages based on user input

## Debugging purposes
#print("Filtered Player Input: " + filtered_msg)
#print("Filtered Commands: " + filtered_commands) 
#print("Filtered Message With Paid: " + filtered_paid_msg)

update_file()

runpy.run_path("Sentiment_Analysis_bot.py") #Run Sentiment Analysis 
