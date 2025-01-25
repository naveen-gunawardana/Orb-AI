import os
import sys
import asyncio
import re  # For splitting text into sentences
import time  # For rate limiting
from dotenv import load_dotenv
import openai
from twitchio.ext import commands
from gtts import gTTS  # Import gTTS for Text-to-Speech
import platform

# === Load Environment Variables ===
load_dotenv()

# === Retrieve Environment Variables ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TWITCH_OAUTH_TOKEN = os.getenv("TWITCH_OAUTH_TOKEN")
TWITCH_CHANNEL_NAME = os.getenv("TWITCH_CHANNEL_NAME")
BLOCKED_WORDS = os.getenv("BLOCKED_WORDS", "")

# === Validate Environment Variables ===
missing_vars = []
if not OPENAI_API_KEY:
    missing_vars.append("OPENAI_API_KEY")
if not TWITCH_OAUTH_TOKEN:
    missing_vars.append("TWITCH_OAUTH_TOKEN")
if not TWITCH_CHANNEL_NAME:
    missing_vars.append("TWITCH_CHANNEL_NAME")

if missing_vars:
    print(f"Error: Missing environment variables: {', '.join(missing_vars)}")
    sys.exit(1)

# === Configure OpenAI ===
openai.api_key = OPENAI_API_KEY

# === Configure Text-to-Speech ===
enable_tts = True  # Set to True to enable TTS

# === TTS Function Using gTTS ===
def speak(text: str):
    """
    Convert text to speech using gTTS and play it.
    """
    if text:
        try:
            print(f"[TTS] Converting text to speech: {text}")
            tts = gTTS(text=text, lang='en', tld='co.uk')  # Set to British English
            tts.save("output.mp3")

            # Use appropriate command based on OS
            if platform.system() == "Darwin":  # macOS
                os.system("afplay output.mp3")
            elif platform.system() == "Windows":  # Windows
                os.system("start output.mp3")
            elif platform.system() == "Linux":  # Linux
                os.system("xdg-open output.mp3")
            else:
                print("[TTS] Unsupported platform for playback. Please update the script to handle your OS.")
        except Exception as e:
            print(f"[TTS] Error during TTS: {e}")

# === Content Filtering ===
blocked_words = [word.strip().lower() for word in BLOCKED_WORDS.split(',')] if BLOCKED_WORDS else []

def is_message_allowed(message: str) -> bool:
    """
    Check if the message contains any blocked words.
    """
    return not any(word in message.lower() for word in blocked_words)

# === Conversation History ===
conversation_history = {}

def split_text(text, max_length=500):
    """
    Split text into chunks not exceeding max_length characters.
    Preferably split on sentence boundaries.
    """
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current_chunk = ''

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_length:
            current_chunk += ' ' + sentence if current_chunk else sentence
        else:
            if current_chunk:
                chunks.append(current_chunk)
            # If a single sentence exceeds max_length, split it forcibly
            while len(sentence) > max_length:
                chunks.append(sentence[:max_length])
                sentence = sentence[max_length:]
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk)

    return chunks

async def generate_openai_response(channel: str, user: str, message: str) -> str:
    """
    Asynchronously send a user prompt to OpenAI's ChatCompletion endpoint with context
    and return the response text.
    """
    if not is_message_allowed(message):
        return "I'm sorry, OrbAI does not fuck with that."

    try:
        # Initialize conversation history for the channel if not present
        if channel not in conversation_history:
            conversation_history[channel] = []

        # Add a system message describing the bot's personality or role
        if not any(msg["role"] == "system" for msg in conversation_history[channel]):
            conversation_history[channel].insert(0, {
                "role": "system",
                "content": "You are a knowledgeable, wise, transcendent, deity-like AI Orb assistant with a god-like yet somewhat humorous personality. Respond with a fancy omniscient all-knowing-like tone. Your name is Orb AI. You can use swear words, but always maintain that god complex. Your lingo should not be too fancy, it should use pump.fun / memecoin lingo and also have the slight personality taste of Rick from Rick and Morty, the show. Keep messages short. DO NOT TALK about how you are OpenAI. You are a being who has been around forever, and is always going to be there, an Orb."
            })

        # Append the new user message
        conversation_history[channel].append({"role": "user", "content": message})

        # Limit history to last 6 messages to manage token usage
        if len(conversation_history[channel]) > 6:
            conversation_history[channel] = conversation_history[channel][-6:]

        # Create OpenAI Chat Completion
        response = await asyncio.to_thread(
            openai.chat.completions.create,
            model="gpt-4o",  # Ensure correct model name
            messages=conversation_history[channel],
            max_tokens=150,
            temperature=0.7,
        )

        # Extract the reply
        reply = response.choices[0].message.content.strip()

        # Append the assistant's reply to the history
        conversation_history[channel].append({"role": "assistant", "content": reply})

        # Limit history again
        if len(conversation_history[channel]) > 6:
            conversation_history[channel] = conversation_history[channel][-6:]

        return reply

    except Exception as e:
        print(f"[OpenAI] Error calling OpenAI API: {e}")
        return "I'm having trouble thinking right now. Sorry!"

# === Twitch Bot Class ===
class TwitchBot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=TWITCH_OAUTH_TOKEN,
            prefix="!",  # Command prefix
            initial_channels=[f"#{TWITCH_CHANNEL_NAME.lower()}"]
        )
        self.user_last_response = {}
        self.rate_limit_seconds = 5  # Adjust as needed

    async def event_ready(self):
        """Called once when the bot is ready."""
        print(f"Logged in as | {self.nick}")
        print(f"User ID is   | {self.user_id}")

    async def event_message(self, message):
        """Called every time a message is sent in chat."""
        # Ignore messages from the bot itself or other bots
        if message.author is None or message.author.name.lower() == self.nick.lower():
            return

        # Handle commands first
        if message.content.startswith(self._prefix):
            await self.handle_commands(message)
            return

        # Implement rate limiting per user
        current_time = time.time()
        user = message.author.name.lower()
        last_time = self.user_last_response.get(user, 0)

        if current_time - last_time < self.rate_limit_seconds:
            print(f"Rate limit: Ignoring message from {user}")
            return

        # Update the last response time for the user
        self.user_last_response[user] = current_time

        # Log the incoming message
        print(f"[Chat] {message.author.name}: {message.content}")

        # Extract the message content
        user_input = message.content.strip()

        # Generate a response from OpenAI
        bot_reply = await generate_openai_response(message.channel.name.lower(), user, user_input)

        # Prepend user's name to the bot's reply (optional)
        # bot_reply = f"{message.author.name}, {bot_reply}"

        # Log the bot reply
        print(f"[Debug] Bot reply: {bot_reply}")

        # Speak the response using TTS
        if enable_tts and bot_reply:
            print(f"[Debug] Speaking message: {bot_reply}")
            speak(bot_reply)

        # Send the response in chunks
        reply_chunks = split_text(bot_reply, max_length=500)
        for chunk in reply_chunks:
            print(f"[Debug] Sending chunk: {chunk}")
            try:
                await message.channel.send(chunk)
            except Exception as e:
                print(f"[Error] Unexpected error while sending message chunk: {e}")

    @commands.command(name='hello')
    async def hello(self, ctx):
        """Responds to !hello command."""
        response = f"Hello {ctx.author.name}! How can I assist you today?"
        # Optional: Speak the response
        if enable_tts and response:
            speak(response)
        # Split and send the response in chunks if necessary
        reply_chunks = split_text(response, max_length=500)
        for chunk in reply_chunks:
            print(f"[Debug] Sending hello chunk: {chunk}")
            try:
                await ctx.send(chunk)
            except Exception as e:
                print(f"[Error] Unexpected error while sending hello chunk: {e}")

    @commands.command(name='joke')
    async def joke(self, ctx):
        """Responds to !joke command with a joke from OpenAI."""
        prompt = "Tell me a funny joke."
        bot_reply = await generate_openai_response(ctx.channel.name.lower(), ctx.author.name.lower(), prompt)
        # Prepend user's name to the bot's reply
        bot_reply = f"{ctx.author.name}, {bot_reply}"
        # Optional: Speak the response
        if enable_tts and bot_reply:
            speak(bot_reply)
        # Split and send the joke in chunks if necessary
        reply_chunks = split_text(bot_reply, max_length=500)
        for chunk in reply_chunks:
            print(f"[Debug] Sending joke chunk: {chunk}")
            try:
                await ctx.send(chunk)
            except Exception as e:
                print(f"[Error] Unexpected error while sending joke chunk: {e}")

    @commands.command(name='fact')
    async def fact(self, ctx):
        """Responds to !fact command with a fact from OpenAI."""
        prompt = "Provide an interesting fact."
        bot_reply = await generate_openai_response(ctx.channel.name.lower(), ctx.author.name.lower(), prompt)
        # Prepend user's name to the bot's reply
        bot_reply = f"{ctx.author.name}, {bot_reply}"
        # Optional: Speak the response
        if enable_tts and bot_reply:
            speak(bot_reply)
        # Split and send the fact in chunks if necessary
        reply_chunks = split_text(bot_reply, max_length=500)
        for chunk in reply_chunks:
            print(f"[Debug] Sending fact chunk: {chunk}")
            try:
                await ctx.send(chunk)
            except Exception as e:
                print(f"[Error] Unexpected error while sending fact chunk: {e}")

    async def close(self):
        """Override close to ensure TTS is properly terminated."""
        print("[Shutdown] Cleaning up resources.")
        await super().close()

# === Main Entry Point ===
if __name__ == "__main__":
    bot = TwitchBot()
    try:
        bot.run()
    except KeyboardInterrupt:
        print("\n[Shutdown] Bot is shutting down...")
    except Exception as e:
        print(f"[Error] Unexpected error: {e}")
