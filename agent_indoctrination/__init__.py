"""
Agent Indoctrination Framework.
"""

from .core.agent import Agent, PythonAgent
from .core.config import Config
from .core.orchestrator import Orchestrator

class Indoctrinator:
    """
    Main entry point for the Agent Indoctrination framework.
    """
    
    def __init__(self, config_path: str = None):
        """
        Initialize the Indoctrinator.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = Config(config_path)
        self.orchestrator = Orchestrator(self.config)
        
    def run(self, agent):
        """
        Run the full indoctrination suite on an agent.
        
        Args:
            agent: The agent to test
            
        Returns:
            Test results
        """
        return self.orchestrator.run(agent)
        
    def generate_report(self, results, format="markdown", output_path=None):
        """
        Generate a report from results.
        
        Args:
            results: Test results
            format: Report format (markdown, json, pdf)
            output_path: Path to save report
            
        Returns:
            Path to generated report
        """
        from .reporting.generator import ReportGenerator
        generator = ReportGenerator(self.config)
        return generator.generate(results, format, output_path)
