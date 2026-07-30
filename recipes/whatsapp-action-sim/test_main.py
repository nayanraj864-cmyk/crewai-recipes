"""Smoke test: main() runs without errors and build_crew signature is correct."""

import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

os.environ.setdefault("LLM_API_KEY", "nvapi-test")
sys.path.insert(0, str(Path(__file__).parent))

import main as recipe_main  # noqa: E402
from crew import build_crew  # noqa: E402


def test_crew_build() -> None:
    """Verify build_crew instantiates Crew with 3 agents and 3 tasks."""
    crew = build_crew(user_message="Hey! Where is my order?", sender_name="Test User")
    assert len(crew.agents) == 3
    assert len(crew.tasks) == 3


def test_main_runs() -> None:
    """Verify main.py runs smoothly with mocked LLM kickoff."""
    mock_output = MagicMock()
    mock_output.__str__ = lambda self: "📱 Mocked WhatsApp reply"
    with patch("crewai.Crew.kickoff", return_value=mock_output):
        recipe_main.main()


if __name__ == "__main__":
    test_crew_build()
    test_main_runs()
    print("✅ whatsapp-action-sim: test_main passed")
