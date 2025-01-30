import whisper
import os
import sys
import warnings
from dotenv import load_dotenv
from summarizer import summarize_text, extract_action_items, extract_dates, identify_speakers
from slack_notifier import send_meeting_summary_to_slack, send_action_items_to_slack

# Load environment variables
load_dotenv()

# Suppress warnings
warnings.simplefilter("ignore")

def transcribe_audio(audio_file):
    """ Transcribes audio using OpenAI Whisper """
    if not os.path.exists(audio_file):
        print(f"Error: File '{audio_file}' not found.")
        sys.exit(1)

    print("Transcribing meeting audio...")
    model = whisper.load_model("base")  # Options: "tiny", "small", "medium", "large"
    
    try:
        result = model.transcribe(audio_file, fp16=False)  # Avoids FP16 warnings
        return result["text"]
    except Exception as e:
        print(f"Error in transcription: {e}")
        sys.exit(1)

def process_meeting(audio_file):
    """ Full pipeline: Transcribes, summarizes, and extracts action items """

    transcription = transcribe_audio(audio_file)
    print("Transcription complete!")

    print("Summarizing meeting notes...")
    summary = summarize_text(transcription)
    
    print("Extracting action items...")
    action_items = extract_action_items(transcription)
    
    print("Extracting important dates...")
    meeting_dates = extract_dates(transcription)
    
    print("Identifying speakers...")
    labeled_speakers = identify_speakers(transcription)

    # Save output to text file
    summary_file = "meeting_summary.txt"
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(f"Summary:\n{summary}\n\n")
        f.write(f"Action Items:\n{action_items}\n\n")
        f.write(f"Dates Identified:\n{meeting_dates}\n\n")
        f.write(f"Speaker Identification:\n{labeled_speakers}\n")

    print(f"Meeting summary saved to {summary_file}")

    # Send to Slack
    print("Sending meeting summary to Slack...")
    send_meeting_summary_to_slack(summary)
    
    print("Sending action items to Slack...")
    send_action_items_to_slack(action_items)

    print("Meeting processed and sent to Slack!")

    return summary, action_items, meeting_dates, labeled_speakers

if __name__ == "__main__":
    # Automatically detect file path instead of hardcoding it
    default_audio_file = os.path.join(os.path.expanduser("~"), "Downloads", "EarningsCall.wav")

    # Use command-line argument if provided, otherwise use default path
    audio_file = sys.argv[1] if len(sys.argv) > 1 else default_audio_file

    summary, action_items, meeting_dates, labeled_speakers = process_meeting(audio_file)
