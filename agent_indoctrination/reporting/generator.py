import json
import os

class ReportGenerator:
    def __init__(self, config):
        self.config = config
        
    def generate(self, results, format="markdown", output_path=None):
        if output_path is None:
            output_path = f"report.{format}"
            
        if format == "json":
            with open(output_path, "w") as f:
                json.dump(results, f, indent=2)
        elif format == "markdown":
            with open(output_path, "w") as f:
                f.write("# Agent Indoctrination Report\n\n")
                f.write(f"Status: {results.get('overall_status', 'unknown')}\n")
                f.write("## Results\n")
                f.write(json.dumps(results, indent=2))
        elif format == "pdf":
            # Stub for PDF generation
            with open(output_path, "w") as f:
                f.write("%PDF-1.4\n%Stub PDF content")
                
        return os.path.abspath(output_path)
