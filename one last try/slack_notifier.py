import os
from slack_sdk import WebClient
from dotenv import load_dotenv

load_dotenv()

slack_client = WebClient(token=os.getenv("SLACK_API_TOKEN"))
channel_id = os.getenv("SLACK_CHANNEL_ID")

def send_slack_message(text):
    """ Sends a message to a Slack channel """
    slack_client.chat_postMessage(channel=channel_id, text=text)

def send_action_items_to_slack(action_items):
    """ Sends extracted action items to Slack """
    message = f"*Meeting Action Items*:\n{action_items}"
    send_slack_message(message)

def send_meeting_summary_to_slack(summary):
    """ Sends summarized meeting notes to Slack """
    message = f"*Meeting Summary*:\n{summary}"
    send_slack_message(message)
