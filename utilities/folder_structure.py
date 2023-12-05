# %%
# Standard Library
import os


def print_folder_structure(
        start_path,
        ignored_folders=None,
        ignored_extensions=None,
        indent=0,
        output_path=None
    ):
    """
    Prints the folder structure starting from the given path.
    Ignored folders and file extensions can be specified.

    :param startpath: The starting path of the directory structure to print.
    :param ignored_folders: A list of folder names to ignore.
    :param ignored_extensions: A list of file extensions to ignore
        (e.g., ['.jpg', '.txt']).
    """
    if ignored_folders is None:
        ignored_folders = []
    if ignored_extensions is None:
        ignored_extensions = []

    output_lines = []

    for root, dirs, files in os.walk(start_path, topdown=True):
        dirs[:] = [
            d for d in dirs if d not in ignored_folders
        ]  # Modify dirs in place to ignore specified folders
        level = root.replace(start_path, "").count(os.sep)
        indent = " " * 4 * level
        output_lines.append(f"{indent}{os.path.basename(root)}/")

        subindent = " " * 4 * (level + 1)
        for f in files:
            if not any(f.endswith(ext) for ext in ignored_extensions):
                output_lines.append(f"{subindent}{f}")

    output_str = "\n".join(output_lines)

    if output_path is not None:
        with open(output_path, "w") as f:
            f.write(output_str)
    else:
        print(output_str)  # Print to console


if __name__=="__main__":
    ### Get args from command line
    # Standard Library
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_path", type=str, default=None)
    parser.add_argument("--ignored_folders", type=str, default=None)
    parser.add_argument("--ignored_extensions", type=str, default=None)
    parser.add_argument("--output_path", type=str, default="utilities/results/folder_structure.txt")
    parser.add_argument("--print_only", type=bool, default=False)
    args = parser.parse_args()

    if args.start_path is None:
        start_path = os.path.join(
        os.path.dirname(__file__), "..")
    else:
        start_path = args.start_path

    if args.ignored_folders is None:
        ignored_folders = [
            "__pycache__",
            ".git",
            ".pytest_cache",
            ".mypy_cache",
        ]
    else:
        ignored_folders = args.ignored_folders

    if args.ignored_extensions is None:
        ignored_extensions = [".pyc", ".log"]
    else:
        ignored_extensions = args.ignored_extensions

    output_path = args.output_path

    if args.print_only is None:
        print_only = False
    else:
        print_only = args.print_only

    if print_only:
        output_path = None

    print_folder_structure(
        start_path=start_path,
        ignored_folders=ignored_folders,
        ignored_extensions=ignored_extensions,
        output_path=output_path,
    )


# %%
