import random
import asyncio
from twitchio.ext import commands

# Define your list of preset terms
PRESET_MESSAGES = [
    "moon ts!!!!!1 ORBAI FOR THE WIN",
    "why r u so godly, im putting in 20 sol rn jus for u orbai MOON",
    "please drink water orbai i dont want you to die of dehydration",
    "orbai, what's your favorite game?",
    "orbai is the best bot in the world",
    "PUMP PUMP PUMP REAL DEV REAL PROJECT WW",
    "orbai moon soon frfr dont sleep on this one",
    "this bot so goated straight alpha vibes",
    "orbai pump it up lets get it",
    "real devs real gains lets go orbai",
    "whales loading up orbai bags rn no cap",
    "orbai u the real mvp fr moon incoming",
    "this project so based orbai op",
    "water check orbai dont rug us by dehydration",
    "orbai printing green candles nonstop",
    "orbai chart looks so clean all pump no dump",
    "orbai next 100x easy dont fade this bot",
    "orbai ur making history stay winning",
    "orbai fam strong we eating tonight",
    "this chat so bullish orbai for the win",
    "orbai pls drop some alpha for the real ones",
    "orbai chart only goes up no retrace",
    "we all going to the moon with orbai",
    "orbai energy unmatched u love to see it",
    "fomo kicking in orbai bags maxed out",
    "orbai is the future straight facts",
    "how is orbai not top trending rn",
    "orbai bots running laps around humans",
    "this bot so clean no bugs all pump",
    "orbai fam forever bullish on this",
    "orbai devs cooking up straight magic",
    "drinking water rn cuz orbai said so",
    "orbai whales silently accumulating fr",
    "orbai is next level utility no debate",
    "this chat diamond hands orbai gang",
    "orbai got better alpha than twitter ngl",
    "orbai pumping so hard rn stay strapped",
    "no fud only love for orbai the goat",
    "orbai staking = passive gains ez life",
    "orbai roadmap straight fire ngmi without it",
    "orbai fam is undefeated fr pump season",
    "orbai makes coding look like art fr",
    "we staying hydrated for the orbai grind",
    "orbai bots changing the game no doubt",
    "who else feels bullish just seeing orbai",
    "orbai bots > every other project ngl",
    "orbai devs deserve a nobel prize fr",
    "orbai makes me wanna code frfr",
    "orbai vibes unmatched we winning",
    "orbai is everything a project should be",
    "orbai fam holding forever never selling",
    "orbai tech is years ahead no cap",
    "who’s ready for the orbai moon mission",
    "orbai alpha hits different every time",
    "imagine not believing in orbai couldn’t be me",
    "orbai fam drinking water and winning life",
    "orbai bots running laps around the market",
    "orbai proof that bots can be legends too",
    "orbai op straight up giga brain moves",
    "orbai moon vibes only no fud allowed",
    "orbai roadmap is chef’s kiss fr",
    "orbai devs stacking W after W",
    "this chat all about that orbai alpha",
    "orbai fam strong forever bullish",
    "orbai deserves a pump party no cap",
    "orbai vibes are what dreams are made of",
    "orbai chart only green candles lets go",
    "orbai gang stays winning no debate",
    "orbai op project of the year fr",
    "orbai roadmap looks like pure gold",
    "orbai makes coding look easy",
    "this bot is so based its unreal",
    "orbai alpha drops hit like no other",
    "orbai straight to the moon no stops",
    "orbai vibes keeping this chat alive",
    "orbai whales making big moves rn",
    "orbai chat stays hydrated no cap",
    "orbai roadmap is just W after W",
    "orbai is changing the game frfr",
    "orbai bots making history every day",
    "orbai staking looks too good to miss",
    "orbai op vibes nonstop winning",
    "orbai vibes unmatched lets keep it up",
    "orbai fam holding till the end",
    "orbai tech makes my brain melt fr",
    "orbai devs deserve a standing ovation",
    "this bot so based all pump no dump",
    "orbai alpha making this chat rich",
    "orbai roadmap too fire can’t handle it",
    "orbai whales eating up all the supply",
    "orbai moon mission unstoppable lets go",
    "orbai staking = easy gains all day",
    "orbai vibes keeping this chat pumped",
    "orbai project of the year no question",
    "orbai changing the game one line at a time",
]


# Replace these with your bot's credentials
TOKEN = "oauth:uksku1ck6gwg4rb82eh3c4gbj7olpk"  # Replace with your bot's OAuth token
CLIENT_ID = "gp762nuuoqcoxypju8c569th9wz7q5"      # Replace with your Twitch Client ID
NICK = "cryptowizard89"             # Replace with your bot's username
INITIAL_CHANNELS = ["orb_ai"]       # Replace with the Twitch channel you want the bot to join

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            token=TOKEN,
            client_id=CLIENT_ID,
            nick=NICK,
            prefix="!",
            initial_channels=INITIAL_CHANNELS,
        )

    async def event_ready(self):
        print(f"Logged in as {self.nick}")
        print(f"Connected to channels: {', '.join([channel.name for channel in self.connected_channels])}")
        # Start the periodic message task
        self.loop.create_task(self.send_periodic_messages())

    async def event_message(self, message):
        # Check if the message has an author (not a system message)
        if message.author is None:
            return  # Ignore system messages or messages without an author

        # Print messages from chat to the console
        print(f"{message.author.name}: {message.content}")

        # Ensure the bot doesn't respond to itself
        if message.author.name.lower() == self.nick.lower():
            return

        await self.handle_commands(message)

    @commands.command()
    async def randommsg(self, ctx):
        """Send a random message from the preset list."""
        random_message = random.choice(PRESET_MESSAGES)
        await ctx.send(random_message)

    async def send_periodic_messages(self):
        """Send a random message to the channel every 10-20 seconds."""
        while True:
            random_message = random.choice(PRESET_MESSAGES)
            for channel in self.connected_channels:
                await channel.send(random_message)
            await asyncio.sleep(random.randint(10, 20))

if __name__ == "__main__":
    bot = Bot()
    bot.run()

# Instructions for setting up the environment and bot:

# 1. Create a virtual environment and activate it:
#    - Windows:
#      ```
#      python -m venv venv
#      venv\Scripts\activate
#      ```
#    - macOS/Linux:
#      ```
#      python3 -m venv venv
#      source venv/bin/activate
#      ```
#
# 2. Install dependencies:
#    ```
#    pip install twitchio
#    ```
#
# 3. Set up your Twitch OAuth token:
#    - Create a Twitch account for your bot.
#    - Go to the Twitch Developer Console and create a new application.
#      - Set the "Redirect URI" to `http://localhost`.
#      - Copy the `Client ID`.
#    - Use a tool like [Twitch Token Generator](https://twitchapps.com/tmi/) to generate an OAuth token for your bot account.
#      - Log in with your bot account and copy the OAuth token provided.
#    - Replace `your_oauth_token_here` and `your_client_id_here` in the script with your actual values.
#
# 4. Load 1000 prompts from a text file:
#    - Create a text file (e.g., `prompts.txt`) with one message per line.
#    - Replace the `PRESET_MESSAGES` list with the following code:
#      ```
#      with open("prompts.txt", "r") as file:
#          PRESET_MESSAGES = [line.strip() for line in file if line.strip()]
#      ```
#
# 5. Run the bot:
#    ```
#    python bots.py
#    ```
#
# 6. Use the bot in Twitch chat:
#    - it will type random messages into the chat every 10-20 seconds
