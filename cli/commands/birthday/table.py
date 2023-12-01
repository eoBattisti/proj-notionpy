from typing import List

from cli.base_table import BaseTable

class BirthdayTable(BaseTable):
    
    def __init__(self, fields: List[str] = ["Name", "Data"]) -> None:
        super().__init__(fields)
