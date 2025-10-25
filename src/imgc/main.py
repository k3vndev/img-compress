import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from imgc.args import Arg, FilterFormats


def main():
    input_args = sys.argv[1:]

    main_config = {
        'filter_formats': ['*'], # Compress all formats by default
    }

    args_obj_list: list[Arg] = [
        FilterFormats(
            name='filter-formats',
            description='Command used to filter the formats of the images to be compressed',
            usage='filter-formats:format1,format2,format3 or filter-formats:*',
        ),
    ]

    for input_arg in input_args:
        splitted_arg = input_arg.split(':')

        if len(splitted_arg) != 2:
            raise ValueError(f"Invalid argument: {input_arg}")

        input_arg_name = splitted_arg[0]
        input_arg_value = splitted_arg[1]

        current_arg_obj: Arg = None

        
        for arg_obj in args_obj_list:
            if arg_obj.name == input_arg_name:
                current_arg_obj = arg_obj
                break

        if not current_arg_obj:
            print(f'Unknown argument name provided. Recieved {input_arg_name}')
            break
        
        print(f"Executing {current_arg_obj.name}...")

        try:
            current_arg_obj.execute(input_arg_value, main_config)
        except Exception as error:
            print(error)
            print(current_arg_obj.usage)

    print(main_config)




if __name__ == "__main__":
    main()