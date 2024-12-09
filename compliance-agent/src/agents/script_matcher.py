from typing import Dict, List
import yaml
import re

class ScriptMatcher:
    def __init__(self, config: Dict):
        self.config = config
        # Load script rules
        with open('config/script_rules.yaml', 'r') as f:
            self.rules = yaml.safe_load(f)
    
    def match_dialogue(self, dialogue: List[Dict]) -> Dict:
        """Match dialogue against script rules"""
        matches = {
            'greeting': self._check_greeting(dialogue),
            'verification': self._check_verification(dialogue),
            'disclosure': self._check_disclosure(dialogue),
            'resolution': self._check_resolution(dialogue)
        }
        return matches
    
    def _check_greeting(self, dialogue: List[Dict]) -> float:
        """Check greeting compliance"""
        greeting_score = 0
        first_turns = dialogue[:2]  # Check first two turns for greeting elements
        
        for turn in first_turns:
            if turn['speaker'] == 'Caller':
                text = turn['text'].lower()
                # Check for greeting elements
                if re.search(r'good (morning|afternoon|evening)|hello', text):
                    greeting_score += 0.3
                if re.search(r'my name is .+? from', text):
                    greeting_score += 0.4
                if re.search(r'(mr|mrs|ms|miss)\. .+?', text):
                    greeting_score += 0.3
                
        return min(greeting_score, 1.0)
    
    def _check_verification(self, dialogue: List[Dict]) -> float:
        """Check verification compliance"""
        verification_score = 0
        for i, turn in enumerate(dialogue):
            if turn['speaker'] == 'Caller':
                text = turn['text'].lower()
                # Check for verification request
                if re.search(r'(confirm|verify).+(ic|identity|date of birth|dob)', text):
                    # Check if customer provided verification
                    if i + 1 < len(dialogue) and dialogue[i+1]['speaker'] == 'Customer':
                        customer_response = dialogue[i+1]['text'].lower()
                        if re.search(r'\d{4}|yes', customer_response):
                            verification_score = 1.0
                            break
        return verification_score
    
    def _check_disclosure(self, dialogue: List[Dict]) -> float:
        """Check disclosure compliance"""
        disclosure_score = 0
        for turn in dialogue:
            if turn['speaker'] == 'Caller':
                text = turn['text'].lower()
                if re.search(r'(call.+?recorded|recorded.+?call).+?(quality|compliance)', text):
                    disclosure_score = 1.0
                    break
        return disclosure_score
    
    def _check_resolution(self, dialogue: List[Dict]) -> float:
        """Check resolution compliance"""
        resolution_score = 0
        last_turns = dialogue[-4:]  # Check last four turns for better coverage
        
        # Check for proper closing elements
        has_confirmation = False
        has_thank_you = False
        has_goodbye = False
        has_final_check = False  # New element: checking if anything else needed
        
        for turn in last_turns:
            text = turn['text'].lower()
            # Check confirmation
            if any(word in text for word in ['confirm', 'note', 'payment', "i'll", 'will']):
                has_confirmation = True
            # Check thank you
            if 'thank' in text:
                has_thank_you = True
            # Check goodbye
            if any(word in text for word in ['goodbye', 'good day', 'bye']):
                has_goodbye = True
            # Check final service check
            if 'anything else' in text or 'help you with' in text:
                has_final_check = True
        
        # Calculate score with all elements
        elements = [has_confirmation, has_thank_you, has_goodbye, has_final_check]
        resolution_score = sum(elements) / len(elements)
        
        return resolution_score
    
    def _contains_element(self, text: str, element: str) -> bool:
        """Check if text contains required element"""
        element_patterns = {
            'introduction': r'(good|hello|hi)',
            'bank_name': r'from \w+ bank',
            'customer_name': r'(mr|mrs|ms|miss|mdm)\s+\w+'
        }
        return bool(re.search(element_patterns.get(element, ''), text, re.I)) 