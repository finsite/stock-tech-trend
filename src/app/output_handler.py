"""
Module to handle output of trend analysis to various targets.

This module provides a single function to send the processed analysis data
to an output destination. Currently, it prints the data and logs it. You can
extend it to send data to a database, a dashboard, or another queue.
"""

import json

from app.logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)


def send_to_output(data: dict[str, any]) -> None:
    """Outputs processed trend analysis to a chosen output target.

    Args:
    ----
        data (dict[str, any]): The processed trend analysis data as a dictionary.

    Returns:
    -------
        None
    """
    try:
        # Convert to JSON for output
        formatted_output: str = json.dumps(data, indent=4)

        # Log the output
        logger.info("Sending data to output: \n%s", formatted_output)

        # Placeholder: Replace with actual write to output target
        print(formatted_output)

    except Exception as e:
        # Log any errors
        logger.error("Failed to send output: %s", e)
