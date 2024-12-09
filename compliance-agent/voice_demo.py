import os
from dotenv import load_dotenv
from src.agents.voice_handler import VoiceHandler
from src.agents.compliance_checker import ComplianceChecker
from colorama import init, Fore, Style
import time

init()  # Initialize colorama

def print_header():
    print(f"\n{Fore.BLUE}{'='*50}")
    print(f"{Fore.WHITE}Interactive Call Center Compliance Demo")
    print(f"{Fore.BLUE}{'='*50}{Style.RESET_ALL}\n")

def main():
    print_header()
    
    # Initialize voice handler
    print(f"{Fore.CYAN}Initializing voice system...{Style.RESET_ALL}")
    voice_handler = VoiceHandler()
    
    print(f"\n{Fore.CYAN}Starting interactive call session...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Instructions:{Style.RESET_ALL}")
    print("1. You will play the role of the customer")
    print("2. Press Enter when ready to respond")
    print("3. Speak after the beep")
    print("4. Recording will stop automatically after 5 seconds")
    print("\nPress Enter to start the call...")
    input()
    
    # Simulated call script
    call_steps = [
        "Good morning sir. My name is James Wilson from ABC Bank. May I speak with Mr. Robert Smith?",
        "Thank you. To ensure I'm speaking with the correct person, may I confirm the last 4 digits of your IC number please?",
        "Thank you for confirming. This call may be recorded for quality and compliance purposes. I'm calling regarding your loan payment for this month.",
        "I see that your payment was due on the 15th. Would you be able to make the payment this week?",
        "That's excellent. I'll note down your commitment. Is there anything else I can help you with today?",
        "Thank you for your time. Have a great day!"
    ]
    
    # Start conversation
    for step in call_steps:
        # Play caller's part
        print(f"\n{Fore.GREEN}Caller:{Style.RESET_ALL}")
        voice_handler.text_to_speech(step)
        voice_handler.add_to_conversation("Caller", step)
        
        # Get customer's response
        print(f"\n{Fore.YELLOW}Your turn (Press Enter when ready):{Style.RESET_ALL}")
        input()
        audio_path = voice_handler.record_audio()
        if audio_path:
            response = voice_handler.transcribe_audio(audio_path)
            print(f"{Fore.CYAN}You said: {Style.RESET_ALL}{response}")
            voice_handler.add_to_conversation("Customer", response)
        else:
            print(f"{Fore.RED}Failed to record audio{Style.RESET_ALL}")
            voice_handler.add_to_conversation("Customer", "...")
        time.sleep(1)  # Brief pause between turns
    
    # Save and analyze transcript
    print(f"\n{Fore.CYAN}Saving and analyzing conversation...{Style.RESET_ALL}")
    transcript_path = os.path.join("data", "transcripts", "live_transcript.txt")
    voice_handler.save_transcript(transcript_path)
    
    checker = ComplianceChecker('config/config.yaml')
    results = checker.check_compliance(transcript_path)
    
    # Print results
    print(f"\n{Fore.CYAN}Compliance Analysis Results:{Style.RESET_ALL}")
    print(f"\nOverall Score: {Fore.YELLOW}{results['overall_score']:.2f}{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}Section Scores:{Style.RESET_ALL}")
    for section, score in results['compliance_scores'].items():
        color = Fore.GREEN if score >= checker.config['compliance_thresholds'][section] else Fore.RED
        print(f"{color}▶ {section.capitalize():12} : {score:.2f}{Style.RESET_ALL}")
    
    if results['issues']:
        print(f"\n{Fore.RED}Issues Found:{Style.RESET_ALL}")
        for issue in results['issues']:
            print(f"❌ {issue}")
    else:
        print(f"\n{Fore.GREEN}✓ No compliance issues found{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Demo terminated by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}") 