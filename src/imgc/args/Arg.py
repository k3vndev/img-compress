class Arg:
  """
    This class is used to create an argument.
    Argument is a value that is passed to the command.
    It follows the format name:value
  """
  
  def __init__(self, name: str, description: str, usage: str):
    self.name = name
    self.description = description
    self.usage = usage

  def execute(self):
    pass