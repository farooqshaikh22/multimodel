from typing import List, Dict, Optional
from langchain.llms import BaseLLM
import re

class TranscriptParser:
    def __init__(self, llm: BaseLLM):
        self.llm = llm
    
    def parse(self, transcript: str) -> List[Dict]:
        """Parse transcript into structured dialogue turns"""
        dialogue_turns = []
        
        # Split transcript into turns
        lines = transcript.strip().split('\n')
        
        for line in lines:
            if line.strip():
                turn = self._parse_line(line)
                if turn:
                    dialogue_turns.append(turn)
        
        return dialogue_turns
    
    def _parse_line(self, line: str) -> Optional[Dict]:
        """Parse single line of dialogue"""
        # Match pattern: Speaker: Text
        match = re.match(r'^(Caller|Customer):\s*(.+)$', line)
        
        if match:
            return {
                'speaker': match.group(1),
                'text': match.group(2).strip(),
                'tokens': self._tokenize(match.group(2).strip())
            }
        return None
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization of text"""
        return text.lower().split() 