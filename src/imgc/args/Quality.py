from imgc.args import Arg

class Quality(Arg):
    name = 'quality'
    alias = 'q'
    default_value = 70
    description = 'Argument used to set the output images quality'
    usage = 'quality:40'

    def __init__(self):
        super().__init__(self.name, self.alias, self.default_value, self.description, self.usage)

    def execute(self, arg_value: str, main_config: dict):
        if not arg_value:
            raise Arg.Error(f'{self.name} needs a value to know how much compression to apply.')

        try:
            parsed_value = round(int(arg_value))

            if (parsed_value < 0 or parsed_value > 100):
                raise ValueError
            
            main_config['quality'] = parsed_value

        except ValueError:
            raise Arg.Error(
                f'Expected a valid number in {self.name}. Expected an integer between 0 and 100. {self.dumpRecieved(arg_value)}')