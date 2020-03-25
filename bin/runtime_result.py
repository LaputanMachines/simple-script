# coding=utf-8
"""Source for the RuntimeResult class for tracking runtime errors."""


class RuntimeResult:
    """Represents the results of runtime errors and streams."""

    def __init__(self):
        # Note: While the reset() function assigns
        #       all the values in this class,
        #       it is still necessary to include the
        #       initial definitions here so that Python
        #       is aware that the RuntimeResult class does
        #       indeed contain attributes.
        self.value = None
        self.error = None
        self.func_return_value = None
        self.loop_should_continue = None
        self.loop_should_break = None
        self.reset()  # Populate values

    def reset(self):
        """
        Resets all attributes of the RuntimeResult.
        Used for when functions are done being evaluated
        in the execution chain. We don't want to assign
        the 'value' attribute a FUNC, but rather its
        final returned value instead.
        """
        self.value = None
        self.error = None
        self.func_return_value = None
        self.loop_should_continue = False
        self.loop_should_break = False

    def register(self, result):
        """
        Registers a result into the RuntimeResult instance.
        :param result: The result of a runtime encounter.
        :return: The value of the result.
        """
        if isinstance(result, RuntimeResult):
            self.error = result.error
            self.func_return_value = result.func_return_value
            self.loop_should_continue = result.loop_should_continue
            self.loop_should_break = result.loop_should_break
            return result.value
        # Note: This hackish handling of the input types
        #       is bad-practice and should be properly
        #       resolved eventually. While this doesn't actually
        #       cause any issues, it introduces confusion and
        #       has the potential to break down the line. (#3)
        return result

    def success(self, value):
        """
        Process and wrap a successful runtime instance.
        :param value: Value of the runtime stream.
        :return: The RuntimeResult instance.
        """
        self.reset()
        self.value = value
        return self

    def failure(self, error):
        """
        Process and wrap an error instance.
        :param error: Error output from stream.
        :return: The RuntimeResult instance.
        """
        self.reset()
        self.error = error
        return self

    def success_return(self, value):
        """
        Processes a successful RETURN request.
        :param value: Value of the RETURN class.
        :return: The updated RuntimeResult instance.
        """
        self.reset()
        self.func_return_value = value
        return self

    def success_continue(self):
        """
        Processes a successful CONTINUE request.
        :return: The updated RuntimeResult class.
        """
        self.reset()
        self.loop_should_continue = True
        return self

    def success_break(self):
        """
        Processes a successful BREAK request.
        :return: The updated RuntimeResult class.
        """
        self.reset()
        self.loop_should_break = True
        return self

    def should_return(self):
        """
        Allows you to continue and break outside the current function.
        :return: Tuple with all RuntimeResult instance settings.
        """
        return (self.error or self.func_return_value or
                self.loop_should_continue or self.loop_should_break)
