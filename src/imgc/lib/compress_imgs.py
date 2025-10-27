from .Consts import Consts

from PIL import Image
from colorama import Fore
import os


folder = "./"

Name = None


def generate_name(config: dict, og_name: str, index: int, files_count: int):
    # Resolve Name import
    global Name
    if Name is None:
        from imgc.args import Name

    output_name = ""

    # Handle each value
    name_values = config[Name.name]
    for value in name_values:
        if isinstance(value, str):
            output_name += value
            continue
        elif isinstance(value, Name.Original):
            output_name += og_name
        elif isinstance(value, Name.Index):
            output_name += value.generate(index, files_count)

    return output_name


def compress_imgs(config: dict):
    from imgc.args import Quality, FilterFormats

    quality: int = config[Quality.name]
    filter_formats: set[str] = config[FilterFormats.name]
    target_format = "webp"

    # Add all formats if filter accepts all formats
    accepts_all_formats = list(filter_formats)[0] == "*"
    if accepts_all_formats:
        filter_formats = Consts.allowed_formats

    to_compress_imgs = []

    for filename in os.listdir(folder):
        # Extract the extension
        _, raw_ext = os.path.splitext(filename)
        ext = raw_ext[1:]

        if ext in filter_formats:
            to_compress_imgs.append(filename)

    if not len(to_compress_imgs):
        filters_msg = "that matched the filters " if not accepts_all_formats else ""
        print(f"No images {filters_msg}were found. Nothing was done :(")
        return

    print(
        f"{Fore.LIGHTMAGENTA_EX}{len(to_compress_imgs)} images were found! :){Fore.RESET}"
    )

    # Create output folder if it doesn't exist and clear it
    output_folder = Consts.output_folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    else:
        for f in os.listdir(output_folder):
            os.remove(os.path.join(output_folder, f))

    spinner = [".", "..", "...", "...."]
    l_just_val = 99

    # Compress each image
    for i, img_filename in enumerate(to_compress_imgs):
        # Print message and loading indicator
        loading_ind = spinner[i % len(spinner)]
        progress = f"{Fore.LIGHTGREEN_EX}({i + 1}/{len(to_compress_imgs)}){Fore.RESET}"

        msg = f"Compressing {img_filename} {progress} {loading_ind}"
        print(msg.ljust(l_just_val), end="\r", flush=True)

        original_img_path = os.path.join(folder, img_filename)
        img_obj = Image.open(original_img_path)

        # Get target name
        og_name, _ = os.path.splitext(img_filename)
        final_name = generate_name(
            config=config, index=i, og_name=og_name, files_count=len(to_compress_imgs)
        )

        target_img_path = os.path.join(output_folder, f"{final_name}.{target_format}")
        img_obj.save(target_img_path, target_format.upper(), quality=quality)

    print(
        f"Images compressed and saved to {Fore.GREEN}{output_folder}{Fore.RESET}!".ljust(
            l_just_val
        )
    )
