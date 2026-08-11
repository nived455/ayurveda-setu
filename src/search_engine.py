import json
import pandas as pd

class AyurvedaSearchEngine:
    def __init__(self, json_path: str = "data/ayurveda_data.json"):
        with open(json_path, "r", encoding="utf-8") as f:
            self.raw_data = json.load(f)
        self.df = pd.DataFrame(self.raw_data)

    def get_all_doshas(self):
        doshas = set()
        for dosha_list in self.df['dosha']:
            doshas.update(dosha_list)
        return sorted(list(doshas))

    def filter_data(self, query: str = "", selected_dosha: str = "All"):
        filtered = self.raw_data

        if selected_dosha != "All":
            filtered = [item for item in filtered if selected_dosha in item['dosha']]

        if query.strip():
            q = query.lower()
            filtered = [
                item for item in filtered
                if q in item['name'].lower()
                or q in item['sanskrit'].lower()
                or q in item['botanical'].lower()
                or any(q in u.lower() for u in item['uses'])
            ]

        return filtered