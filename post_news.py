import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import commands
import json
import openai
import os
from dotenv import load_dotenv
from datetime import datetime
from telegram import Bot


load_dotenv()
openai.api_key = os.getenv('OPEN_AI_KEY')

#extract stories
def extract_stories(json_data):
    try:
        data = json.loads(json_data)
        stories = data.get("props", {}).get("pageProps", {}).get("stories", [])
        return stories
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []

# parse html file for tldr
def tldr_parse_html(date):
    url = f'https://tldr.tech/tech/{date}'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

    url_values = {}
    for script_tag in soup.find_all('script', {'type': 'application/json'}):
        # Extracting content from the script tag
        content = script_tag.string
        return extract_stories(content)
        

     
    return url_values

def create_reword_prompt(title):
    prompt = f"You are a technology and strategy consultant. Please reword the Title and TLDR and return Title, URL, TLDR: {title}"
    return prompt

def create_select_prompt(title):
    prompt = f"We are a technology strategy, engineering, data & AI company. Please select only 3 appropriate stories, reword the Title, and TLDR and return Title, URL, TLDR in your own words: {title}"
    return prompt

def print_stories(stories):
    for index, story in enumerate(stories, start=1):
        print(f"\nStory {index}:")
        print(f"Title: {story.get('title')}")
        print(f"URL: {story.get('url')}")
        print(f"TLDR: {story.get('tldr')}")
        print(f"Date: {story.get('date')}")
        print(f"Category: {story.get('category')}")
        print(f"Newsletter: {story.get('newsletter')}")

##telegram posting


### MAIN ###
def send_tg_message_to_group(token, chat_id, message):
    bot = Bot(token=token)
    #print('chat id ', bot.get_chat(chat_id))
    bot.send_message(chat_id=chat_id, text=message)


### MAIN #####
#use parse function
today_date = datetime.today().strftime('%Y-%m-%d')
#today_date = "2024-01-05"
stories = tldr_parse_html(today_date)
print_stories(stories)

#Select stories
prompt_str = create_select_prompt(stories)
response = openai.Completion.create(
    model = "gpt-3.5-turbo-instruct-0914",
    prompt = prompt_str,
    temperature = 0.7,
    max_tokens = 1000)

#Send TG message
#TG send a message
bot_token = os.getenv('TG_TOKEN')
bot_chat_id = os.getenv('TG_CHAT_ID')

content = response['choices'][0]['text']
post_str = f"Rayze Top 3 story stream for {today_date}\n"
send_tg_message_to_group(bot_token,bot_chat_id, post_str)
post_arr = content.split('Title:')
print(len(post_arr), "/// ",post_arr)
ix = 0
for item in post_arr:
    if (item == '\n\n'):
        continue
    ix = ix+1
    item = item.replace("URL:","\nURL:")
    item = item.replace("TLDR:","\nSUMMARY:")
    item = f"\nStory {ix}:\n{item}\n"
    send_tg_message_to_group(bot_token,bot_chat_id, item)
    if ix >=3:
        break
  


# # Discord bot setup
# bot_token = os.getenv('DISCORD_PUB_KEY')
# bot_prefix = '!'
# bot = commands.Bot(command_prefix=bot_prefix)

# @bot.event
# async def on_ready():
#     print(f'Logged in as {bot.user.name}')

# # # Command to scrape, reword, and post summaries to a Discord channel
# async def post_summaries(ctx, stories):
#     await ctx.send(stories)


# # # Run the Discord bot
# bot.command(name='post_summaries')
# bot.run(bot_token)

###PROMPTS
# User
# given the following json - find all of the stories in this json