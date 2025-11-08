from .Consts import Consts

from PIL import Image
from colorama import Fore
import os


folder = "./"


def compress_imgs(config: dict):
    from imgc.args import Quality, FilterFormats, Format

    quality: int = config[Quality.name]
    filter_formats: set[str] = config[FilterFormats.name]
    target_format: str = config[Format.name]

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

        # Handle target format
        if target_format == "~":
            # Keep original format
            _, raw_ext = os.path.splitext(img_filename)
            target_format = raw_ext[1:]
        else:
            # Handle RGBA to RGB conversion for formats that do not support alpha channel
            no_alpha_formats = {"jpg", "jpeg", "bmp"}

            if img_obj.mode == "RGBA" and target_format in no_alpha_formats:
                img_obj = img_obj.convert("RGB")

        # Save compressed image
        save_format = target_format.upper()

        if save_format == "JPG":
            save_format = "JPEG"

        target_img_path = os.path.join(output_folder, f"{final_name}.{target_format}")
        img_obj.save(target_img_path, save_format, quality=quality)

    print(
        f"Images compressed and saved to {Fore.GREEN}{output_folder}{Fore.RESET}!".ljust(
            l_just_val
        )
    )


Name = None
existing_names: set[str] = set()


def generate_name(config: dict, og_name: str, index: int, files_count: int):
    global Name
    if Name is None:
        from imgc.args import Name

    name_values = config[Name.name]
    used_unique = False
    output_name = ""

    # Handle each value
    for value in name_values:
        if isinstance(value, str):
            output_name += value
        elif isinstance(value, Name.Original):
            output_name += og_name
            used_unique = True
        elif isinstance(value, Name.Index):
            output_name += value.generate(index, files_count)
            used_unique = True

    # Force index to avoid overwriting files
    if not used_unique:
        output_name += f"_{index + 1}"

    return output_name
