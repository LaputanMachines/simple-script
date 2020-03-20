# coding=utf-8
"""Source for the RuntimeResult class for tracking runtime errors."""


class RuntimeResult:
    """Represents the results of runtime errors and streams."""

    def __init__(self):
        """
        Initializes the blank RuntimeResult instance.
        """
        self.value = None
        self.error = None

    def register(self, result):
        """
        Registers a result into the RuntimeResult instance.
        :param result: The result of a runtime encounter.
        :return: The value of the result.
        """
        if result.error:
            self.error = result.error
        return result.value

    def success(self, value):
        """
        Process and wrap a successful runtime instance.
        :param value: Value of the runtime stream.
        :return: The RuntimeResult instance.
        """
        self.value = value
        return self

    def failure(self, error):
        """
        Process and wrap an error instance.
        :param error: Error output from stream.
        :return: The RuntimeResult instance.
        """
        self.error = error
        return self
