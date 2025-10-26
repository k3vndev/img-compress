import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from imgc.args import Arg, FilterFormats

import colorama
from colorama import Fore, Style

colorama.init()
colorama.just_fix_windows_console()


def handle_args(main_config, input_args, args_obj_list):
    for input_arg in input_args:
        # Split arg name and value
        splitted_arg = input_arg.split(':')

        if len(splitted_arg) > 2:
            raise ValueError(f"An argument cant have multiple values. Recieved {input_arg}")

        input_arg_name  = splitted_arg[0]
        input_arg_value = None

        if len(splitted_arg) == 2:
            input_arg_value = splitted_arg[1]

        current_arg_obj: Arg = None

        # Find the arg that's being used
        for arg_obj in args_obj_list:
            if arg_obj.name == input_arg_name:
                current_arg_obj = arg_obj
                break

        if not current_arg_obj:
            print(f'Unknown argument name provided. Recieved {input_arg_name}')
            break
        

        try:
            current_arg_obj.execute(input_arg_value, main_config)
            
        except Arg.Error as error:
            # Handle errors
            print(Fore.RED)
            print(f"Error: {error}")
            print(f"{Fore.MAGENTA}Example usage: {current_arg_obj.usage}")
            print(Fore.RESET)

def main():
    input_args = sys.argv[1:]

    main_config = {
        'filter_formats': ['*'], # Compress all formats by default
    }

    args_obj_list: list[Arg] = [
        FilterFormats(
            name='filter-formats',
            description='Command used to filter the formats of the images to be compressed',
            usage='filter-formats:png,webp,jpeg or filter-formats:*',
        ),
    ]

    handle_args(main_config, input_args, args_obj_list)

    

    print(main_config)




if __name__ == "__main__":
    main()