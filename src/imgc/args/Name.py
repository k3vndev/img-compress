from .Arg import Arg


class Name(Arg):
    class Original:
        vars = ["n", "name"]
        pass

    class Index:
        vars = ["i", "index"]

        def __init__(self, pad=False, start=1, step=1):
            self.pad = pad
            self.start = start
            self.step = step

        def generate(self, i: int, files_count: int):
            i_val = i if self.step > 0 else files_count - 1 - i
            i_str = abs(self.start + i_val * self.step)
            max_i_len = len(str(abs(self.start + (files_count - 1) * self.step)))
            txt = f"{i_str:0{max_i_len}d}" if self.pad else i_str

            return str(txt)

    name = "name"
    alias = "n"
    default_value = [Original()]
    description = "Argument used to set the output images name"
    usage = "name:image-[i] or name:image-[.i0*5]"

    open_tag, close_tag = ["[", "]"]

    def __init__(self):
        super().__init__(
            self.name, self.alias, self.default_value, self.description, self.usage
        )

    def search_variables(self, txt: str, variables: list[str]):
        already_found = False
        original_txt = txt

        start = None
        end = None
        var_used = None

        for _ in range(2):
            for var in variables:
                index = txt.find(var)
                if index == -1:
                    continue

                if already_found:
                    raise Arg.Error(
                        f'Duplicated variable in brackets: "{original_txt}" has the key "{var}" two times or more. '
                        "Only one variable is needed per bracket chunk."
                    )

                start, end = [index, index + len(var)]
                var_used = var
                already_found = True
                txt = txt[0:start] + txt[end:]

        return start, end, var_used

    # Validate name
    def execute(self, arg_value: str, main_config: dict):
        if not self.validateArgValue(arg_value):
            raise Arg.Error(
                f"{self.name} needs a value to know how to name the output. Do not call if you wish to leave the names as they are."
            )

        forbidden_chars = set([":", '"', "/", "\\", "|", "?", "*"])
        arg_value = arg_value.strip()

        current_chunk = ""
        chunks: list[str] = []

        opened_a_tag = False

        # Parse content into chunks and make basic validations
        for i, char in enumerate(arg_value):
            # Handle open tags
            if char == self.open_tag:
                if not opened_a_tag:
                    opened_a_tag = True

                    # Start current chunk
                    if current_chunk:
                        chunks.append(current_chunk)
                        current_chunk = ""
                else:
                    raise Arg.Error(
                        f"You must close the previous bracket before opening a new one. {self.dumpRecieved(arg_value)}"
                    )

            # Write to current chunk
            current_chunk += char

            # Handle close tags
            if char == self.close_tag:
                if opened_a_tag:
                    opened_a_tag = False

                    # Close current chunk
                    chunks.append(current_chunk)
                    current_chunk = ""
                else:
                    raise Arg.Error(
                        f"You can't close a bracket if you haven't opened yet. {self.dumpRecieved(arg_value)}"
                    )

            # Handle last char
            if i == len(arg_value) - 1:
                if opened_a_tag and char != self.close_tag:
                    raise Arg.Error(
                        f"You never closed the last bracket. {self.dumpRecieved(arg_value)}"
                    )
                chunks.append(current_chunk)
                current_chunk = ""

        # Convert chunks into utility objects
        name_vals = []

        for chunk in chunks:
            # Skip chunk if it's empty
            if not chunk:
                continue

            is_tag = chunk[0] == self.open_tag

            # Handle normal text
            if not is_tag:

                # Validate characters
                for char in chunk:
                    if char in forbidden_chars:
                        raise Arg.Error(
                            f"Invalid character used in {self.name}. Used: {char}"
                        )

                # Add normal text
                name_vals.append(chunk)
                continue

            # Strip inner content from chunk
            inner = chunk[1:-1]

            # Handle Original
            _, _, n_var_used = self.search_variables(inner, self.Original.vars)
            if n_var_used:
                name_vals.append(self.Original())
                continue

            # Handle index
            i_start, i_end, i_var_used = self.search_variables(inner, self.Index.vars)

            if not i_var_used:
                listed_vars = '", "'.join(self.Index.vars + self.Original.vars)

                raise Arg.Error(
                    f'No valid variable found in brackets: "{chunk}". Expected one of the following variables:" {listed_vars}"'
                )

            pad_substr = inner[0:i_start]
            pad = pad_substr == "."

            if pad_substr and not pad:
                msg_start = (
                    "Multiple tokens" if len(pad_substr) > 1 else "Unexpected token"
                )

                raise Arg.Error(
                    f'{msg_start} found before "{i_var_used}" in "{chunk}". Expected an auto-padding indicator (using a single ".") or nothing.'
                )

            separator = "*"
            params_substr = inner[i_end:]

            separator_already_found = False
            start = ""
            step = ""

            # Safely extract params:
            for char in params_substr:

                # Handle separator
                if char == separator:
                    if not separator_already_found:
                        separator_already_found = True
                        continue

                    raise Arg.Error(
                        f'Duplicated separator in variable params: "{params_substr}" use the "{separator}" two times or more. '
                        "Only one separator is needed per bracket chunk."
                    )

                # Write to start or step
                if not separator_already_found:
                    start += char
                else:
                    step += char

            if separator_already_found and not step:
                raise Arg.Error(
                    f'Missing step value after separator in variable params: "{params_substr}" in "{chunk}".'
                )

            # Parse start and step
            def parse_param(val: str, name: str):
                try:
                    if not val:
                        return None

                    return int(val)
                except ValueError:
                    raise Arg.Error(
                        f'Expected a valid integer number for {name} param at "{i_var_used}" variable. {self.dumpRecieved(val)}'
                    )

            start = parse_param(start, "start")
            step = parse_param(step, "step")

            if start and start < 0:
                raise Arg.Error(
                    f'Start value cannot be negative at "{i_var_used}" variable.'
                )

            if step == 0:
                raise Arg.Error(
                    f'Step value cannot be zero at "{i_var_used}" variable. That would make all indexes the same!'
                )

            # Set variables
            index_obj = self.Index()

            if step != None:
                index_obj.step = step
            if start != None:
                index_obj.start = start

            index_obj.pad = pad
            name_vals.append(index_obj)

        # Set main config
        main_config[self.name] = name_vals
