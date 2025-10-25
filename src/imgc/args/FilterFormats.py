
from imgc.args import Arg


class FilterFormats(Arg):
    def __init__(self, name: str, description: str, usage: str):
        super().__init__(name, description, usage)

    def execute(self, arg_value: str, main_config: dict):
        formats = arg_value.split(',') if arg_value else []
        valid_formats = [ 'png', 'jpg', 'jpeg', 'webp' ]

        if '*' in formats:
            main_config['filter_formats'] = valid_formats
            return

        for raw_format in formats:
            if raw_format.startswith('.'):
                raw_format = raw_format[1:]

            if raw_format not in valid_formats:
                raise ValueError(f'Invalid format used in filter-formats. Recieved "{raw_format}"')

        main_config['filter_formats'] = formats
