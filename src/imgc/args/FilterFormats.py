from .Arg import Arg
from imgc.lib import Consts
from typing import Set


class FilterFormats(Arg):
    name = "filter-formats"
    alias = "ff"
    default_value = set(["*"])
    description = "Argument used to filter the formats of the images to be compressed"
    usage = "filter-formats:png,webp,jpeg or filter-formats:*"

    def __init__(self):
        super().__init__(
            self.name, self.alias, self.default_value, self.description, self.usage
        )

    def execute(self, arg_value: str, main_config: dict):
        if not arg_value:
            raise Arg.Error(f"{self.name} needs a value to know what to filter.")

        formats = arg_value.split(",") if arg_value else []
        valid_formats = Consts.allowed_formats

        positive_filters: Set[str] = set()
        negative_filters: Set[str] = set()
        is_including_all = False

        for raw_format in formats:
            # Handle asterisk
            if raw_format == "*":
                is_including_all = True
                continue

            # Handle negative
            is_negative = False
            if raw_format.startswith("-"):
                is_negative = True
                raw_format = raw_format[1:]

            # Remove any leading dots
            if raw_format.startswith("."):
                raw_format = raw_format[1:]

            # Handle invalid formats
            if raw_format not in valid_formats:
                raise Arg.Error(
                    f"Invalid format used in {self.name}. {self.dumpRecieved(raw_format)}"
                )

            if is_negative:
                negative_filters.add(raw_format)
            else:
                positive_filters.add(raw_format)

        # Handle asterisk
        if is_including_all and not len(negative_filters):
            main_config[self.name] = set(valid_formats)
            return

        # Prevent the use of both positive and negative filters
        if len(positive_filters) and len(negative_filters):
            raise Arg.Error(
                f"Can't use both positive and negative filters in {self.name}. {self.dumpRecieved(formats)}"
            )

        # Handle positive filters
        if len(positive_filters):
            main_config[self.name] = positive_filters
            return

        try:
            # Handle negative filters
            all_filters = valid_formats
            for f in negative_filters:
                all_filters.remove(f)

            main_config[self.name] = all_filters

        except KeyError:
            raise Arg.Error(
                f"Sorry! An unexpected error happened while using negative filters in {self.name}. {self.dumpRecieved(formats)}"
            )
