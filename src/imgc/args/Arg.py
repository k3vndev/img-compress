class Arg:
  """
    This class is used to create an argument.
    Arguments are custom settings added to the main command.
    It usually follows the format name:value
  """
  
  def __init__(self, name: str, description: str, usage: str):
    self.name = name
    self.description = description
    self.usage = usage

  def execute(self):
    pass

  class Error(Exception):
    """Raised when something goes wrong with and Arg."""
    pass