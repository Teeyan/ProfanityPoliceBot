import discord
import json
import random
import numpy as np
from profanity_check import predict_prob

IMAGE_NAME_LIST = "images/image_names.txt"
RESPONSE_FILE = "response.txt"
THRESHOLD = 0.6

class ProfanityPolice(discord.Client):

    def __init__(self):
        super().__init__()
        with open(IMAGE_NAME_LIST, "r") as fp:
           self.image_names = fp.readlines()
        with open(BLACKLIST_FILE, "r") as fp:
            self.bad_words = fp.readlines()
        with open(RESPONSE_FILE, "r") as fp:
            self.responses = fp.readlines()

    def _get_response_image(self):
        """
        Randomly grab an image from the resources and return it for the bot to upload
        """
        pass

    def _get_response_message(self):
        """
        Randomly grab a response from the resources and return it for the bot to upload
        """
        pass

    def _check_for_profanity(self, message):
        """
        Checks message content to see if it contains a blacklisted word
        :param message: content to be checked against blacklist
        :return True if content is flagged, False otherwise
        """
        return predict_prob(message)[0] > THRESHOLD

    async def on_ready(self):
        print('Logged on as ', self.user)
        await client.change_presence(activity=discord.Game(name="these hoes cuz i'm a real nigga"))

    async def on_message(self, message):
        if message.author == self.user:
            return
        is_profanity = self.check_for_profanity(message.content)
        if is_profanity:
            print("profanity from %s: %s" % (message.author, message.content))
            image_path = self._get_response_image()
            await message.channel.send(file=Discord.File(image_path))
            await message.channel.send(self._get_response_message())


def _get_bot_token():
    """
    Gets and returns bot token from file token.txt
    """
    with open("token.txt", "r+") as fp:
        token = fp.readlines().strip()
        return token


def main():
    token = _get_bot_token()
    ppbot = ProfanityPolice()
    ppbot.run(token)

if __name__ == "__main__":
    main()
