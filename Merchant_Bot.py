import re
import openai
import random
import Mercali_Bot_Instructions 
import Hippocampus 
import runpy

filename = "Pond.txt"

gpt4_unlazy = "gpt-4-0125-preview"
gpt4_ruleFollower = "gpt-4-1106-preview"

openai.api_key = ""

short_term_memory_instructions = "All the text beyond this point are previous conversations that The Player and You have had. Take this as a memory of sorts. 'You: ' is your responses and 'The Player :' is The Player's responses. "

messages_M = []

system_msg_M = Mercali_Bot_Instructions.Mercali_Instructions 

with open('short_term_memory.txt', 'r') as file:
    short_term_memory_contents = file.read()

ultimate_response = system_msg_M + short_term_memory_instructions + short_term_memory_contents 

messages_M.append({"role": "system", "content": ultimate_response})
#messages_M.append({"role": "system", "content": short_term_memory_contents}) #Short Term Memory. Doubles up on responses since it recognizes that it is another bot

def load_initial_values():
    global good_human_score, filtered_paid_response, merchant_gold_coins, merchant_ruka_stock, unfiltered_merchant_response, filtered_merchant_response, filtered_merchant_commands 
    with open(filename, 'r') as file:
        content = file.read()
        
        #Player's stock and response 
        filtered_paid_response_search = re.search(r'Player Filtered With Paid Response: (.*)', content, re.M)
        good_human_score_search = re.search(r'Player Good Human Score: (\d+)', content, re.M)

        filtered_paid_response = filtered_paid_response_search.group(1).strip() if filtered_paid_response_search else 'E'
        good_human_score = int(good_human_score_search.group(1)) if good_human_score_search else 50 

        #Mercali's stock
        merchant_gold_coins_search = re.search(r'Mercali Gold Coins: (\d+)', content, re.M)
        merchant_ruka_stock_search = re.search(r'Mercali Ruka Stock: (\d+)', content, re.M)

        merchant_gold_coins = merchant_gold_coins_search.group(1).strip() if merchant_gold_coins_search else 100
        merchant_ruka_stock = merchant_ruka_stock_search.group(1).strip() if merchant_ruka_stock_search else 100

        #Mercali's response 
        unfiltered_merchant_response_search = re.search(r'Mercali Unfiltered Response: (.*)', content, re.M)
        filtered_merchant_response_search = re.search(r'Mercali Filtered Response: (.*)', content, re.M)
        filtered_merchant_commands_search = re.search(r'Mercali Commands: (.*)', content, re.M)

        unfiltered_merchant_response = unfiltered_merchant_response_search.group(1).strip() if unfiltered_merchant_response_search else 'E'
        filtered_merchant_response = filtered_merchant_response_search.group(1).strip() if filtered_merchant_response_search else 'E'
        filtered_merchant_commands = filtered_merchant_commands_search.group(1).strip() if filtered_merchant_commands_search else 'E'


def update_file():
    with open(filename, 'r') as file:
        content = file.read()

    content = re.sub(r'Mercali Unfiltered Response: .*', f'Mercali Unfiltered Response: {unfiltered_merchant_response}', content)
    content = re.sub(r'Mercali Filtered Response: .*', f'Mercali Filtered Response: {filtered_merchant_response}', content)
    content = re.sub(r'Mercali Commands: .*', f'Mercali Commands: {filtered_merchant_commands}', content)

    with open(filename, 'w') as file:
        file.write(content)


# Have a conversation with Mercali 
def merchantResponse():
    global gpt4_unlazy, gpt4_ruleFollower, good_human_score, filtered_paid_response, merchant_gold_coins, merchant_ruka_stock, unfiltered_merchant_response, filtered_merchant_commands, filtered_merchant_response

    player_ultimate_response = f"Player Good Human Score: {good_human_score}" + " ; " + f"Mercali Gold Coins: {merchant_gold_coins}" + " ; " + f"Mercali Ruka Stock: {merchant_ruka_stock}\n" + f"\n{filtered_paid_response}"
    #print(player_ultimate_response)
    
    # Generate a response from Mercali bot
    messages_M.append({"role": "user", "content": player_ultimate_response}) 
    response_M = openai.ChatCompletion.create(model=gpt4_ruleFollower,messages=messages_M)
    unfiltered_merchant_response = response_M["choices"][0]["message"]["content"]
    messages_M.append({"role": "assistant", "content": unfiltered_merchant_response})

    unfiltered_merchant_response = unfiltered_merchant_response.replace('\n', '').replace('\r', '')

    pattern = r'<(.*?)>'
    match = re.search(pattern, unfiltered_merchant_response)
    if match:
        filtered_merchant_commands = f'<{match.group(1)}>'
    else:
        filtered_merchant_commands = ""

    filtered_merchant_response = re.sub(pattern, '', unfiltered_merchant_response)

    # Mercali's Response
    #print("\nMercali's Unfiltered Response: " + unfiltered_merchant_response + "\n")
    print("\n" + "Mercali's Response: " + filtered_merchant_response + "\n") # Mercali's Filtered Response 
    print("Purchase Agreement: " + filtered_merchant_commands + "\n") 
    
#load_initial_instructions() # This is if I need to have more control over when the instructions are initialized 
load_initial_values()
merchantResponse()
update_file()
runpy.run_path("Hippocampus.py")
runpy.run_path("Action_Identifier.py") #Action Identifier 

