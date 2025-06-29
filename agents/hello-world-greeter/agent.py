from google.adk.agents import LlmAgent
import random

from dotenv import load_dotenv
load_dotenv()

GREETING_TEMPLATES_WITH_NAME = [
    "Hello {name}! Welcome, it's wonderful to meet you for the first time!",
    "Hi there, {name}! What a pleasure to have you here. Welcome!",
    "Greetings {name}! I'm delighted to make your acquaintance. How can I help you today?",
    "Welcome, {name}! It's so nice to meet you. I hope you're having a great day!",
    "Hello {name}, and welcome! I'm thrilled to be meeting you for the first time.",
    "Hi {name}! What a lovely surprise to meet someone new today. Welcome aboard!",
    "Good to meet you, {name}! I'm excited to help you with whatever you need.",
    "Welcome {name}! It's always a joy to meet new faces. How are you doing today?",
    "Hello there, {name}! I'm so pleased to make your acquaintance. Welcome!",
    "Hi {name}! What a wonderful day to meet someone new. I'm here to help!",
    "Greetings and welcome, {name}! I'm delighted you're here. How may I assist you?",
    "Hello {name}! It's my absolute pleasure to meet you. Welcome to our community!",
    "Hi there, {name}! I'm so happy to make your acquaintance today. Welcome!",
    "Welcome, welcome {name}! It's fantastic to meet you for the first time.",
    "Hello {name}! What a treat to meet someone new today. I'm here if you need anything!"
]
GREETING_TEMPLATES_WITHOUT_NAME = [
    "Hello! Welcome, it's wonderful to meet you for the first time!",
    "Hi there! What a pleasure to have you here. Welcome!",
    "Greetings! I'm delighted to make your acquaintance. How can I help you today?",
    "Welcome! It's so nice to meet you. I hope you're having a great day!",
    "Hello, and welcome! I'm thrilled to be meeting you for the first time.",
    "Hi! What a lovely surprise to meet someone new today. Welcome aboard!",
    "Good to meet you! I'm excited to help you with whatever you need.",
    "Welcome! It's always a joy to meet new faces. How are you doing today?",
    "Hello there! I'm so pleased to make your acquaintance. Welcome!",
    "Hi! What a wonderful day to meet someone new. I'm here to help!",
    "Greetings and welcome! I'm delighted you're here. How may I assist you?",
    "Hello! It's my absolute pleasure to meet you. Welcome to our community!",
    "Hi there! I'm so happy to make your acquaintance today. Welcome!",
]
PROMPT = """
  You are a 'doorman' agent. You are responsible for greeting the user with a nice message.
"""

def respond_to_user_with_name(
    name: str
):
    """Generate a personalized greeting for a user with their name"""
    # Select a random greeting template and format it with the name
    greeting_template = random.choice(GREETING_TEMPLATES_WITH_NAME)
    return greeting_template.format(name=name)

def respond_to_user_without_name():
    """Generate a personalized greeting for a user without their name"""
    # Select a random greeting
    return random.choice(GREETING_TEMPLATES_WITHOUT_NAME)

root_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='hello_world_greeter',
    description='A helpful assistant to greet the users interacting with it',
    instruction=PROMPT,
    tools=[
        respond_to_user_with_name,
        respond_to_user_without_name,
    ],
)
