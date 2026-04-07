#!/usr/bin/env python3
"""Report Generator Module"""
import json
import os
from datetime import datetime

class ReportGenerator:
    def __init__(self, results, output_path):
        self.results = results
        self.output_path = output_path

    def generate(self):
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        report = {
            "timestamp": datetime.now().isoformat(),
            "toolkit": "JEFE Cybersecurity Toolkit v1.0",
            "modules": self.results,
            "summary": self.summarize()
        }
        with open(self.output_path, "w") as f:
            json.dump(report, f, indent=2)
        return report

    def summarize(self):
        total = 0
        critical = 0
        high = 0
        medium = 0
        for module, data in self.results.items():
            if isinstance(data, dict) and "findings" in data:
                for f in data["findings"]:
                    total += 1
                    sev = f.get("severity","")
                    if sev == "critical": critical += 1
                    elif sev == "high": high += 1
                    elif sev == "medium": medium += 1
        return {"total_findings": total, "critical": critical, "high": high, "medium": medium}

