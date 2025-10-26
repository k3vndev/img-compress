from .Arg import Arg
from imgc.lib import Consts

class FilterFormats(Arg):
    name = 'filter-formats'
    alias = 'ff'
    default_value = set(['*'])
    description = 'Argument used to filter the formats of the images to be compressed'
    usage = 'filter-formats:png,webp,jpeg or filter-formats:*'

    def __init__(self):
        super().__init__(self.name, self.alias, self.default_value, self.description, self.usage)

    def execute(self, arg_value: str, main_config: dict):
        if not arg_value:
            raise Arg.Error(f'{self.name} needs a value to know what to filter.')

        formats = arg_value.split(',') if arg_value else []
        valid_formats = Consts.allowed_formats

        for raw_format in formats:
            # Return all comands
            if raw_format == '*':
                main_config[self.name] = valid_formats
                return

            # Remove a possible leading dot
            if raw_format.startswith('.'):
                raw_format = raw_format[1:]

            if raw_format not in valid_formats:
                raise Arg.Error(f'Invalid format used in {self.name}. {self.dumpRecieved(raw_format)}')

        main_config[self.name] = set(formats)
