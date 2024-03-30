import openai
import re
import random
import Sentiment_Analysis_Bot_Instructions
import runpy

openai.api_key = ""

filename = "Pond.txt"

messages_SA = []

my_total_score = 50
possible_total_score = 100

system_msg_SA = Sentiment_Analysis_Bot_Instructions.SA_Instructions
messages_SA.append({"role": "system", "content": system_msg_SA})

# Score Calculation INCORPORATE THIS LATER
def happyMerchant(analysis_score):
    if analysis_score >= 8:
        chance = random.random()
        if (chance * 100) <= 30:
            analysis_score *= 2
            print("Doubled Score")
            print(analysis_score)
    return analysis_score

def load_initial_values():
    global filtered_msg, good_human_score, player_total_instance_score, player_total_possible_score
    with open(filename, 'r') as file:
        content = file.read()
        filtered_msg_search = re.search(r'Player Filtered Response: (.*)', content, re.M)
        good_human_score_search = re.search(r'Player Good Human Score: (\d+)', content, re.M)
        player_total_instance_score_search = re.search(r'Player Total Instance Score: (\d+)', content, re.M)
        player_total_possible_score_search = re.search(r'Player Total Possible Score: (\d+)', content, re.M)

        filtered_msg = filtered_msg_search.group(1).strip() if filtered_msg_search else 'E'
        good_human_score = int(good_human_score_search.group(1)) if good_human_score_search else 50
        player_total_instance_score = int(player_total_instance_score_search.group(1)) if player_total_instance_score_search else 50
        player_total_possible_score = int(player_total_possible_score_search.group(1)) if player_total_possible_score_search else 100

def update_file():
    with open(filename, 'r') as file:
        content = file.read()

    content = re.sub(r'Player Good Human Score: \d+', f'Player Good Human Score: {good_human_score}', content)
    content = re.sub(r'Player Total Instance Score: \d+', f'Player Total Instance Score: {player_total_instance_score}', content)
    content = re.sub(r'Player Total Possible Score: \d+', f'Player Total Possible Score: {player_total_possible_score}', content)

    with open(filename, 'w') as file:
        file.write(content)

def goodHumanAnalyzer():
    global my_total_score, possible_total_score, good_human_score, player_total_instance_score, player_total_possible_score
    
    messages_SA.append({"role": "user", "content": filtered_msg})
    response_SA = openai.ChatCompletion.create(model="gpt-4-0125-preview", temperature=0.3, messages=messages_SA)
    reply_SA = response_SA["choices"][0]["message"]["content"]
    messages_SA.append({"role": "assistant", "content": reply_SA})

    ## Debugging Purposes 
    #print("\nSentiment Analysis Bot's Response: " + reply_SA + "\n")

    try:
        player_total_instance_score += int(reply_SA)
        player_total_possible_score += 10
    except ValueError:
        print("Sentiment Analysis Has Gone Rouge. Setting Analysis Score to 5.") 
        reply_SA = 5
        player_total_instance_score += reply_SA
        player_total_possible_score += 10

    good_human_score = round((player_total_instance_score / player_total_possible_score) * 100)

load_initial_values()
goodHumanAnalyzer()
update_file()
runpy.run_path("Merchant_Bot.py")  # Talk to Mercali
