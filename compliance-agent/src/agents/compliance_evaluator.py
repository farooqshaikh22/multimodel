from typing import Dict, List

class ComplianceEvaluator:
    def __init__(self, config: Dict):
        self.config = config
        self.thresholds = config['compliance_thresholds']
    
    def evaluate(self, matches: Dict) -> Dict:
        """Evaluate compliance based on script matches"""
        scores = {}
        
        for section, score in matches.items():
            threshold = self.thresholds[section]
            scores[section] = self._calculate_section_score(score, threshold)
        
        return scores
    
    def _calculate_section_score(self, raw_score: float, threshold: float) -> float:
        """Calculate normalized section score"""
        if raw_score >= threshold:
            return 1.0
        return raw_score / threshold 