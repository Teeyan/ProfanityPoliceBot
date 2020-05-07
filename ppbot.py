import discord
import json
import random
import numpy as np
from profanity_check import predict_prob

IMAGE_NAME_LIST = "images/image_names.txt"
RESPONSE_FILE = "response.txt"
THRESHOLD = 0.6

class Color:
    RED = '\033[91M'
    BOLD = '\033[1m'
    END = '\033[0m'

class ProfanityPolice(discord.Client):

    def __init__(self):
        super().__init__()
        self.channel = ""
        with open(IMAGE_NAME_LIST, "r") as fp:
           self.image_names = fp.read().splitlines()
        with open(RESPONSE_FILE, "r") as fp:
            self.responses = fp.read().splitlines()

    def _get_response_image(self):
        """
        Randomly grab an image from the resources and return it for the bot to upload
        """
        rand_val = random.randint(0, len(self.image_names) - 1)
        return "images/%s" % self.image_names[rand_val]

    def _get_response_message(self):
        """
        Randomly grab a response from the resources and return it for the bot to upload
        """
        rand_val = random.randint(0, len(self.responses) - 1)
        return self.responses[rand_val]

    def _check_for_profanity(self, message):
        """
        Checks message content to see if it contains a blacklisted word
        :param message: content to be checked against blacklist
        :return True if content is flagged, False otherwise
        """
        return predict_prob(message)[0] > THRESHOLD

    async def on_ready(self):
        print('Logged on as ', self.user)
        self.channel = discord.utils.get(self.get_all_channels(), name="general")
        await self.change_presence(activity=discord.Game(name="these hoes cuz i'm a real nigga"))

    async def on_message(self, message):
        if message.author == self.user:
            return
        is_profanity = self._check_for_profanity([message.content])
        if is_profanity:
            print("profanity from %s: %s" % (message.author, message.content))
            image_path = self._get_response_image()
            message = "*WEE WOO WEE WOO*\n **%s** just said a no no word! " % message.author.display_name
            await self.channel.send(file=discord.File(image_path))
            await self.channel.send(message + self._get_response_message())


def _get_bot_token():
    """
    Gets and returns bot token from file token.txt
    """
    with open("token.txt", "r+") as fp:
        token = fp.readlines()[0].strip()
        return token


def main():
    token = _get_bot_token()
    ppbot = ProfanityPolice()
    ppbot.run(token)

if __name__ == "__main__":
    main()
