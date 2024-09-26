from pathlib import Path
from typing import List


class MockRag:
    def __init__(self, local_file_path: Path):
        self._lines = self._load_lines(local_file_path)

    def get_answer(self, prompt: str):
        relevant_answers = sorted(self._lines, key=lambda x: self._get_similarity_score(prompt, x), reverse=True)

        return relevant_answers[0]

    def get_contexts(self, prompt: str) -> List[str]:
        relevant_answers = sorted(self._lines, key=lambda x: self._get_similarity_score(prompt, x), reverse=True)

        return relevant_answers[:2]
    
    @staticmethod
    def _load_lines(file_path: Path) -> List[str]:
        lines = []
        with open(file_path, "r") as f:
            for line in f.readlines():
                if len(line) > 0:
                    lines.append(line)
        return lines
    
    @staticmethod
    def _get_similarity_score(text_1: str, text_2: str) -> int:
        prompt_tokens = set(text_1.lower().split())
        line_tokens = set(text_2.lower().split())
        return len(prompt_tokens.intersection(line_tokens))
