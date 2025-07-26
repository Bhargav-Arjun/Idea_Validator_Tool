# app/agents/orchestrator.py

"""
This file is now a thin wrapper around the GroupChatManager
returned by app.frameworks.autogen_setup.setup_autogen_agents().
"""

from autogen import ConversableAgent, Agent
from typing import Dict
from app.frameworks.autogen_setup import setup_autogen_agents


class IdeaOrchestratorAgent(ConversableAgent):
    """
    A light wrapper that delegates all work to the AutoGen GroupChatManager.
    """

    def __init__(self, name: str = "IdeaOrchestratorAgent") -> None:
        # Initialise the parent ConversableAgent (mostly for interface parity)
        super().__init__(name=name)
        # Build the AutoGen agent network
        self.manager: Agent = setup_autogen_agents()

    # Entry‑point used by FastAPI
    def run(self, user_idea: str) -> Dict:
        """
        Passes the user idea into the AutoGen group chat and returns the
        final scorecard + trace produced by the DecisionAgent.
        """
        return self.manager.run(input=user_idea)
