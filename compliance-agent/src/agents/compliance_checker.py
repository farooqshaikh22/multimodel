from typing import Dict, List, Optional
from langchain_groq import ChatGroq
import yaml
import logging
import os
from datetime import datetime
from .transcript_parser import TranscriptParser
from .script_matcher import ScriptMatcher
from .compliance_evaluator import ComplianceEvaluator

class ComplianceChecker:
    def __init__(self, config_path: str):
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(self.config['logging']['file_path'])
        os.makedirs(log_dir, exist_ok=True)
        
        # Setup logging
        logging.basicConfig(
            level=self.config['logging']['level'],
            filename=self.config['logging']['file_path']
        )
        
        # Initialize LLM
        self.llm = ChatGroq(
            api_key=self.config['groq']['api_key'],
            model_name=self.config['groq']['model_name']
        )
        
        # Initialize sub-agents
        self.parser = TranscriptParser(self.llm)
        self.matcher = ScriptMatcher(self.config)
        self.evaluator = ComplianceEvaluator(self.config)
        
    def check_compliance(self, transcript_path: str) -> Dict:
        """
        Main method to check transcript compliance
        """
        try:
            # Read transcript
            with open(transcript_path, 'r') as f:
                transcript = f.read()
            
            # Parse transcript
            parsed_dialogue = self.parser.parse(transcript)
            
            # Match against script rules
            script_matches = self.matcher.match_dialogue(parsed_dialogue)
            
            # Evaluate compliance
            compliance_results = self.evaluator.evaluate(script_matches)
            
            # Generate final report
            return self._generate_report(compliance_results)
            
        except Exception as e:
            logging.error(f"Error in compliance checking: {str(e)}")
            raise
    
    def _generate_report(self, compliance_results: Dict) -> Dict:
        """Generate final compliance report"""
        return {
            'timestamp': datetime.now().isoformat(),
            'compliance_scores': compliance_results,
            'overall_score': self._calculate_overall_score(compliance_results),
            'issues': self._identify_issues(compliance_results)
        }
    
    def _calculate_overall_score(self, results: Dict) -> float:
        """Calculate weighted overall compliance score"""
        weights = {
            'greeting': 0.2,
            'verification': 0.3,
            'disclosure': 0.3,
            'resolution': 0.2
        }
        return sum(results[k] * weights[k] for k in weights)
    
    def _identify_issues(self, results: Dict) -> List[str]:
        """Identify compliance issues based on thresholds"""
        issues = []
        thresholds = self.config['compliance_thresholds']
        
        for section, score in results.items():
            if score < thresholds[section]:
                issues.append(f"Non-compliance in {section}: {score:.2f} < {thresholds[section]}")
        
        return issues 