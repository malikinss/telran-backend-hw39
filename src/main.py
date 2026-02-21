# ./src/main.py

"""
Application entry point.

This module initializes environment configuration and launches
the interactive CLI agent.

Responsibilities:
    - Load environment variables from a .env file.
    - Initialize the CLI interface.
    - Start the main interaction loop.

Example:
    Run from command line:

        >>> python -m src.main

    Or directly:

        >>> python src/main.py
"""

from dotenv import load_dotenv

# Load environment variables from a .env file into process environment.
# This allows configuration such as API keys to be defined externally.
load_dotenv()


def main() -> None:
    """
    Start the CLI agent application.

    Performs a lazy import of `AgentCLI` to:
        - Avoid circular import issues.
        - Reduce startup overhead if the module is imported but not executed.
        - Ensure environment variables are loaded before agent initialization.

    Returns:
        None

    Example:
        >>> main()
    """
    from agent import AgentCLI

    cli = AgentCLI()
    cli.run()


if __name__ == "__main__":
    """
    Execute the application when run as a script.

    This guard ensures that `main()` is only executed when the module
    is run directly, and not when it is imported as a dependency.
    """
    main()
