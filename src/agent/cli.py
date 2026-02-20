# ./src/agent/cli.py

from .agent import ToolAgent
from utils import ThinkingDots


class AgentCLI:
    """
    Simple command-line interface for interacting with ToolAgent.

    Responsibilities:
    - Read user input from stdin.
    - Delegate processing to ToolAgent.
    - Display responses.
    - Show a lightweight "thinking" indicator while processing.

    Non-responsibilities:
    - Business logic.
    - Tool execution.
    - LLM communication details.

    Example:
        >>> cli = AgentCLI()
        >>> isinstance(cli.agent, ToolAgent)
        True
    """

    def __init__(self) -> None:
        """
        Initialize CLI with agent and visual thinking indicator.

        Example:
            >>> cli = AgentCLI()
            >>> hasattr(cli, "dots")
            True
        """
        self.agent = ToolAgent()
        self.dots = ThinkingDots("Agent is thinking")

    def run(self) -> None:
        """
        Start interactive CLI loop.

        The loop:
        - Prompts user for input.
        - Exits on 'exit'.
        - Displays a thinking animation while agent processes input.
        - Prints structured agent response.

        Example (conceptual interaction):

            >>> # cli = AgentCLI()
            >>> # cli.run()
            >>> # You: Can I travel to Japan?
            >>> # Agent: {"result": {...}}
            >>> # ------------------------------------------------------------

        Note:
            This method blocks and runs until user types 'exit'.
        """
        print("Phi-3 simple chat. Type 'exit' to quit.\n")

        while True:
            user_input = input("\nYou: ").strip()

            if user_input.lower() == "exit":
                print("Bye!")
                break

            self.dots.start()

            try:
                reply = self.agent.run(user_input)
            finally:
                # Ensure animation always stops,
                # even if agent raises an exception
                self.dots.stop()

            print("Agent:", reply)
            print("_" * 60)
