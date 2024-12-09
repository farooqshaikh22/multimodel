import os
from dotenv import load_dotenv
from src.agents.compliance_checker import ComplianceChecker
from colorama import init, Fore, Style
import time

# Initialize colorama for colored output
init()

def print_header():
    print(f"\n{Fore.BLUE}{'='*50}")
    print(f"{Fore.WHITE}Call Center Compliance Checker Demo")
    print(f"{Fore.BLUE}{'='*50}{Style.RESET_ALL}\n")

def print_analyzing_animation():
    print(f"\n{Fore.YELLOW}Analyzing transcript", end='')
    for _ in range(3):
        time.sleep(0.5)
        print(".", end='', flush=True)
    print(f"{Style.RESET_ALL}\n")

def print_section_score(section: str, score: float, threshold: float):
    color = Fore.GREEN if score >= threshold else Fore.RED
    print(f"{color}▶ {section.capitalize():12} : {score:.2f} / {threshold:.2f}{Style.RESET_ALL}")

def demo_compliance_check():
    print_header()
    
    # Load environment variables
    load_dotenv()
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    print(f"{Fore.CYAN}Loading compliance checker...{Style.RESET_ALL}")
    config_path = os.path.join(current_dir, 'config', 'config.yaml')
    checker = ComplianceChecker(config_path)
    
    # Show available transcripts
    transcript_dir = os.path.join(current_dir, 'data', 'transcripts')
    transcripts = [f for f in os.listdir(transcript_dir) if f.endswith('.txt')]
    
    print(f"\n{Fore.CYAN}Available Call Transcripts:{Style.RESET_ALL}")
    for i, transcript in enumerate(transcripts, 1):
        print(f"{i}. {transcript}")
    
    # Get user input
    choice = input(f"\n{Fore.WHITE}Select transcript to analyze (1-{len(transcripts)}): {Style.RESET_ALL}")
    selected_transcript = transcripts[int(choice)-1]
    
    # Show transcript content
    transcript_path = os.path.join(transcript_dir, selected_transcript)
    with open(transcript_path, 'r') as f:
        content = f.read()
    
    print(f"\n{Fore.CYAN}Selected Transcript Content:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{content}{Style.RESET_ALL}")
    
    # Analyze transcript
    print_analyzing_animation()
    results = checker.check_compliance(transcript_path)
    
    # Print detailed results
    print(f"{Fore.CYAN}Compliance Analysis Results:{Style.RESET_ALL}")
    print(f"\n{Fore.WHITE}Overall Compliance Score: {Fore.YELLOW}{results['overall_score']:.2f}{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}Section Scores:{Style.RESET_ALL}")
    thresholds = checker.config['compliance_thresholds']
    for section, score in results['compliance_scores'].items():
        print_section_score(section, score, thresholds[section])
    
    if results['issues']:
        print(f"\n{Fore.RED}Issues Found:{Style.RESET_ALL}")
        for issue in results['issues']:
            print(f"❌ {issue}")
    else:
        print(f"\n{Fore.GREEN}✓ No compliance issues found{Style.RESET_ALL}")
    
    # Show recommendations
    print(f"\n{Fore.CYAN}Recommendations:{Style.RESET_ALL}")
    for section, score in results['compliance_scores'].items():
        if score < thresholds[section]:
            print(f"• Improve {section} compliance by following the standard script")
            if section == 'verification':
                print("  - Always verify customer identity using IC number or DOB")
            elif section == 'greeting':
                print("  - Use proper greeting with name and bank identification")
            elif section == 'disclosure':
                print("  - Ensure call recording disclosure is clearly stated")

if __name__ == "__main__":
    try:
        demo_compliance_check()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Demo terminated by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}") 