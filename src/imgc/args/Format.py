from .Arg import Arg
from imgc.lib import Consts


class Format(Arg):
    name = "format"
    alias = "f"
    default_value = "webp"
    description = "Argument used to set the output images format"
    usage = "format:png or format:~"

    def __init__(self):
        super().__init__(
            self.name, self.alias, self.default_value, self.description, self.usage
        )

    def execute(self, arg_value: str, main_config: dict):
        if not self.validateArgValue(arg_value):
            raise Arg.Error(
                f"{self.name} needs a value to know which format to convert to. "
                "Do not call if you wish to keep the original format."
            )

        # Handle keeping original format
        if arg_value == "~":
            main_config[self.name] = arg_value
            return

        # Remove leading dot if present
        if arg_value.startswith("."):
            arg_value = arg_value[1:]

        # Validate format
        if arg_value not in Consts.allowed_formats:
            raise Arg.Error(
                f"Invalid format '{arg_value}' in {self.name}. "
                f'Allowed formats are: "{'", "'.join(Consts.allowed_formats)}" or "~". {self.dumpRecieved(arg_value)}'
            )

        # Set the value
        main_config[self.name] = arg_value
