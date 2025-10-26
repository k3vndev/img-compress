
from imgc.args import Arg


class FilterFormats(Arg):
    def __init__(self, name: str, description: str, usage: str):
        super().__init__(name, description, usage)

    def execute(self, arg_value: str, main_config: dict):
        if not arg_value:
            raise Arg.Error(f'filter-formats needs a value to know what to filter.')

        formats = arg_value.split(',') if arg_value else []
        valid_formats = [ 'png', 'jpg', 'jpeg', 'webp' ]

        for raw_format in formats:
            # Return all comands
            if raw_format == '*':
                main_config['filter_formats'] = valid_formats
                return

            # Remove a possible leading dot
            if raw_format.startswith('.'):
                raw_format = raw_format[1:]

            if raw_format not in valid_formats:
                raise Arg.Error(f'Invalid format used in filter-formats. Recieved "{raw_format}"')

        main_config['filter_formats'] = set(formats)
