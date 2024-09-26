import csv
from pathlib import Path
from typing import List, Dict


class GroundTruthProvider:
    def __init__(self, ground_truth_file_path: Path):
        self._ground_truth_path = ground_truth_file_path
        self._question_answer_map = self._load_ground_truth_answers()

    def get_ground_truth_answer(self, question: str) -> List[str]:
        return self._question_answer_map[question]
    
    def get_all_questions(self) -> List[str]:
        return list(self._question_answer_map.keys())
    
    def _load_ground_truth_answers(self) -> Dict[str, List[str]]:
        mapping = {}
        with open(self._ground_truth_path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                mapping[row["question"]] = row["answer"]
        return mapping
