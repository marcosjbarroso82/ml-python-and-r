def make_multiple_inputs(inputs):
    """ 
    provides a function to call for every input requested. 
    Usage:
        inputs = make_multiple_inputs(["im-an-string", "1"])
        monkeypatch.setitem(__builtins__, 'input', inputs)
    """
    inputs = list(reversed(inputs))
    def next_input(_):
        """ provides the first item in the list. """
        return inputs.pop()
    return next_input