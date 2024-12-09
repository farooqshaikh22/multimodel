import os
from dotenv import load_dotenv
from src.agents.compliance_checker import ComplianceChecker

def main():
    # Load environment variables
    load_dotenv()
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Initialize compliance checker with absolute path
    config_path = os.path.join(current_dir, 'config', 'config.yaml')
    checker = ComplianceChecker(config_path)
    
    # Check compliance for sample transcript
    transcript_path = os.path.join(current_dir, 'data', 'transcripts', 'sample_transcript.txt')
    results = checker.check_compliance(transcript_path)
    
    # Print results
    print("\nCompliance Check Results:")
    print("------------------------")
    print(f"Overall Score: {results['overall_score']:.2f}")
    print("\nSection Scores:")
    for section, score in results['compliance_scores'].items():
        print(f"{section}: {score:.2f}")
    print("\nIssues Found:")
    for issue in results['issues']:
        print(f"- {issue}")

if __name__ == "__main__":
    main() 