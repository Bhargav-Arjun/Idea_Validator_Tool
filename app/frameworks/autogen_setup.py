# Agent setup and communication logic placeholder 
# app/frameworks/autogen_setup.py

from autogen import Agent, GroupChat, GroupChatManager
from app.agents import (
    idea_validator,
    market_research,
    relevance_filter,
    competitor_analysis,
    differentiator,
    decision
)
from app.utils.logger import logger

# Each agent gets initialized here with its internal logic
def setup_autogen_agents():
    logger.info("🔧 Setting up AutoGen Agents...")

    # 🧠 Agent 1: Idea Validator
    idea_validator_agent = Agent(
        name="IdeaValidatorAgent",
        description="Checks clarity, uniqueness, and feasibility of ideas",
        function=idea_validator.run
    )

    # 🌐 Agent 2: Market Research
    market_research_agent = Agent(
        name="MarketResearchAgent",
        description="Searches real-time sources or retrieves vector data",
        function=market_research.run
    )

    # 🧪 Agent 3: Relevance Filter
    relevance_filter_agent = Agent(
        name="RelevanceFilterAgent",
        description="Ranks and filters data using similarity",
        function=relevance_filter.run
    )

    # 🕵️ Agent 4: Competitor Analysis
    competitor_agent = Agent(
        name="CompetitorAnalysisAgent",
        description="Identifies similar ideas, products, or startups",
        function=competitor_analysis.run
    )

    # 🌟 Agent 5: Differentiator
    differentiator_agent = Agent(
        name="DifferentiatorAgent",
        description="Suggests improvements and positioning",
        function=differentiator.run
    )

    # 📊 Agent 6: Decision Maker
    decision_agent = Agent(
        name="DecisionAgent",
        description="Gives scorecard and final verdict",
        function=decision.run
    )

    # 👑 Group Manager (Orchestrator)
    orchestrator = GroupChatManager(
        name="IdeaOrchestratorAgent",
        description="Main controller agent to manage all agent flow",
        members=[
            idea_validator_agent,
            market_research_agent,
            relevance_filter_agent,
            competitor_agent,
            differentiator_agent,
            decision_agent
        ],
        system_message="Manage the pipeline from idea validation to scoring."
    )

    logger.info("✅ All agents wired with AutoGen.")

    return orchestrator
