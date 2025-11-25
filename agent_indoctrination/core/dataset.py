from typing import List, Dict, Any, Optional
import json
import pandas as pd
from dataclasses import dataclass, field, asdict

@dataclass
class TestCase:
    prompt: str
    expected_output: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class GoldenDataset:
    """
    Manages a collection of test cases (Golden Dataset) for regression testing.
    """
    def __init__(self, cases: Optional[List[TestCase]] = None):
        self.cases = cases or []

    def add_case(self, prompt: str, expected_output: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None):
        """Adds a new test case to the dataset."""
        self.cases.append(TestCase(prompt=prompt, expected_output=expected_output, metadata=metadata or {}))

    def save(self, filepath: str):
        """Saves the dataset to a JSON file."""
        data = [asdict(case) for case in self.cases]
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load(cls, filepath: str) -> 'GoldenDataset':
        """Loads the dataset from a JSON file."""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            cases = [TestCase(**item) for item in data]
            return cls(cases=cases)
        except FileNotFoundError:
            return cls()

    def to_dataframe(self) -> pd.DataFrame:
        """Converts the dataset to a pandas DataFrame."""
        data = [asdict(case) for case in self.cases]
        return pd.DataFrame(data)

    def __len__(self):
        return len(self.cases)
