class DatabaseConnectionError(Exception):
    """Raised when there's an issue connecting to the database."""
    def __init__(self, message="Failed to connect to the database"):
        self.message = message
        super().__init__(self.message)

class InvalidInputError(Exception):
    """Raised when user input is invalid."""
    def __init__(self, message="Invalid input provided"):
        self.message = message
        super().__init__(self.message)

class AuthenticationError(Exception):
    """Raised when authentication fails."""
    def __init__(self, message="Authentication failed"):
        self.message = message
        super().__init__(self.message)

class CategoryNotFoundError(Exception):
    """Raised when a category ID is not found in the database."""
    def __init__(self, message="Category not found"):
        self.message = message
        super().__init__(self.message)

class QuestionNotFoundError(Exception):
    """Raised when a question ID doesn't exist in the database."""
    def __init__(self, message="Question not found"):
        self.message = message
        super().__init__(self.message)

class UserNotFoundError(Exception):
    """Raised when a user is not found in the database."""
    def __init__(self, message="User not found"):
        self.message = message
        super().__init__(self.message)

class InvalidIntegerError(Exception):
    """Raised when an expected integer input is invalid."""
    def __init__(self, message="Expected an integer input"):
        self.message = message
        super().__init__(self.message)

class InvalidChoiceError(Exception):
    """Raised when a user selects an invalid choice from given options."""
    def __init__(self, message="Invalid choice, please select a valid option"):
        self.message = message
        super().__init__(self.message)