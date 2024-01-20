from telegram import Bot
import os

def get_chat_id_by_username(token, username):
    """
    Get the chat ID associated with a Telegram username.

    Parameters:
    - token (str): Your Telegram bot token.
    - username (str): The username of the target user.

    Returns:
    - int: The chat ID of the user.
    """
    print(f"token is {token}")
    bot = Bot(token=token)
    chat = bot.get_chat(username)
    return chat.id if chat else None

# Example usage:
bot_token = os.getenv("TG_TOKEN")
bot_token = "6732676851:AAEH0pEJ1lmcn4CpIbG_iANDwTH5mXTkA10"
target_username = "@jc212"

chat_id = get_chat_id_by_username(bot_token, target_username)

if chat_id:
    print(f"Chat ID for {target_username}: {chat_id}")
else:
    print(f"User not found or username is incorrect.")

