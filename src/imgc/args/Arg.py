class Arg:
  """
    This class is used to create an argument.
    Arguments are custom settings added to the main command.
    It usually follows the format name:value
  """
  
  def __init__(self, name: str, alias: str, default_value: any, description: str, usage: str):
    self.name = name
    self.description = description
    self.usage = usage
    self.alias = alias
    self.default_value = default_value

  def execute(self):
    pass

  def dumpRecieved(self, value: str):
    return f'Recieved: "{value}".'

  class Error(Exception):
    """Raised when something goes wrong with and Arg."""
    pass