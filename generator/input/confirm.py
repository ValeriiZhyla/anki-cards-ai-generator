def confirm_action(prompt) -> bool:
    """Ask user to enter 'yes' or 'no' (or any affirmative) to confirm an action.

    Args:
        prompt (str): The prompt message to display to the user.

    Returns:
        bool: True if user enters a positive confirmation, False otherwise.
    """
    # Define a set of affirmative responses
    positive_responses = {"yes", "y", "ye", "ok", "true", "1"}

    # Display the prompt with a default indication
    response = input(f"{prompt} [y/N]: ").strip().lower()

    # Return True if response is in affirmative, False otherwise
    return response in positive_responses
