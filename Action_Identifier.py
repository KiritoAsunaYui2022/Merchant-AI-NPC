import re
import runpy

filename = "Pond.txt"

def load_initial_values():
    global Merchant_Gold_Coins, Merchant_Ruka_Amount, Player_Gold_Coins, Player_Ruka_Amount, filtered_player_commands, filtered_merchant_commands
    with open(filename, 'r') as file:
        content = file.read()

        Merchant_Gold_Coins_search = re.search(r'Mercali Gold Coins: (\d+)', content, re.M)
        Merchant_Ruka_Amount_search = re.search(r'Mercali Ruka Stock: (\d+)', content, re.M)
        Player_Gold_Coins_search = re.search(r'Player Gold Coins: (\d+)', content, re.M)
        Player_Ruka_Amount_search = re.search(r'Player Ruka Stock: (\d+)', content, re.M)
        filtered_player_commands_search = re.search(r'Player Commands: (.*)', content, re.M)
        filtered_merchant_commands_search = re.search(r'Mercali Commands: (.*)', content, re.M)

        Merchant_Gold_Coins = int(Merchant_Gold_Coins_search.group(1)) if Merchant_Gold_Coins_search else 100
        Merchant_Ruka_Amount = int(Merchant_Ruka_Amount_search.group(1)) if Merchant_Ruka_Amount_search else 100
        Player_Gold_Coins = int(Player_Gold_Coins_search.group(1)) if Player_Gold_Coins_search else 100
        Player_Ruka_Amount = int(Player_Ruka_Amount_search.group(1)) if Player_Ruka_Amount_search else 0
        filtered_player_commands = filtered_player_commands_search.group(1).strip() if filtered_player_commands_search else 'E'
        filtered_merchant_commands = filtered_merchant_commands_search.group(1).strip() if filtered_merchant_commands_search else 'E'

def update_file():
    with open(filename, 'r') as file:
        content = file.read()

    content = re.sub(r'Mercali Gold Coins: \d+', f'Mercali Gold Coins: {Merchant_Gold_Coins}', content)
    content = re.sub(r'Mercali Ruka Stock: \d+', f'Mercali Ruka Stock: {Merchant_Ruka_Amount}', content)
    content = re.sub(r'Player Gold Coins: \d+', f'Player Gold Coins: {Player_Gold_Coins}', content)
    content = re.sub(r'Player Ruka Stock: \d+', f'Player Ruka Stock: {Player_Ruka_Amount}', content)

    with open(filename, 'w') as file:
        file.write(content)

def categorize_command(command):
    global Merchant_Gold_Coins, Player_Gold_Coins, Merchant_Ruka_Amount, Player_Ruka_Amount

    # Ensure amount is defined even if the try block fails
    amount = 0  # Default to 0 or another appropriate value

    try:
        action = command[command.find("<")+1 : command.find(">")]
        amount = int(command[command.find("|")+1 : command.rfind("|")])
    except ValueError:
        #print("No Commands") 
        category = "Unknown"
    else:
        # Honestly, probably don't need category unless it is used for a specific reason 
        category = "Unknown"
        if "<Accepted>" in filtered_merchant_commands: 
            if action == "Hands The Merchant Gold Coins":
                category = "Gold Coins"
                Merchant_Gold_Coins += amount
                Player_Gold_Coins -= amount
                Merchant_Ruka_Amount -= (amount // 20)
                Player_Ruka_Amount += (amount // 20)
            elif action == "Hands The Player Gold Coins":
                category = "Gold Coins"
                Merchant_Gold_Coins -= amount
                Player_Gold_Coins += amount
            elif action == "Hands The Player Grams of Ruka":
                category = "Ruka"
                Merchant_Ruka_Amount -= amount
                Player_Ruka_Amount += amount
            elif action == "NULL":
                category = "NULL"
        else:
            print("Denied")             
    
    update_file()
    return category, amount

# Initialize variables with defaults
Merchant_Gold_Coins = 100
Merchant_Ruka_Amount = 100
Player_Gold_Coins = 100
Player_Ruka_Amount = 0
filtered_player_commands = ''
filtered_merchant_commands = ''

# Load the initial values from the file
load_initial_values()

# No longer using input for commands, using filtered_player_commands instead
if filtered_player_commands != 'E':  # Check if there are commands to process
    commands = [cmd.strip() for cmd in filtered_player_commands.split(",")]

    for cmd in commands:
        category, amount = categorize_command(cmd)
        #print(f"Action: {category}, Amount: {amount}")
else:
    print("No player commands found or default command used.")

print("__________________________________________________" + "\n") 

runpy.run_path("Filter_Fish.py") #Back to start
