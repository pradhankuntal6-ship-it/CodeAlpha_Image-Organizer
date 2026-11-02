import argparse
import os
import shutil
import sys

JPG_EXTENSIONS = (".jpg", ".jpeg")
DEFAULT_DESTINATION_NAME = "jpg_images"


# --------------------------------------------------------------------------- #
# Core logic
# --------------------------------------------------------------------------- #
def find_jpg_files(folder: str) -> list[str]:
    """Return the names of all JPG files directly inside `folder` (sorted).

    Sub-folders are not searched, and the match ignores letter case so
    'PHOTO.JPG' is found as well as 'photo.jpg'.
    """
    jpg_files = []
    with os.scandir(folder) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.lower().endswith(JPG_EXTENSIONS):
                jpg_files.append(entry.name)
    return sorted(jpg_files)


def get_unique_path(folder: str, filename: str) -> str:
    """Return a path in `folder` that does not exist yet.

    If 'photo.jpg' is taken, tries 'photo_1.jpg', 'photo_2.jpg', and so on.
    """
    name, extension = os.path.splitext(filename)
    path = os.path.join(folder, filename)

    counter = 1
    while os.path.exists(path):
        path = os.path.join(folder, f"{name}_{counter}{extension}")
        counter += 1
    return path


def move_jpg_files(source: str, destination: str, dry_run: bool = False) -> dict:
    """Move every JPG file from `source` to `destination`.

    Returns a summary: {"found": int, "moved": int, "failed": int}.
    """
    files = find_jpg_files(source)
    summary = {"found": len(files), "moved": 0, "failed": 0}

    if not files:
        return summary

    if not dry_run:
        os.makedirs(destination, exist_ok=True)

    for filename in files:
        source_path = os.path.join(source, filename)
        target_path = get_unique_path(destination, filename)
        target_name = os.path.basename(target_path)
        note = "" if target_name == filename else f"  (renamed to {target_name})"

        if dry_run:
            print(f"  [dry run] {filename}{note}")
            summary["moved"] += 1
            continue

        try:
            shutil.move(source_path, target_path)
        except (OSError, shutil.Error) as error:
            print(f"  [failed]  {filename}: {error}")
            summary["failed"] += 1
        else:
            print(f"  [moved]   {filename}{note}")
            summary["moved"] += 1

    return summary


# --------------------------------------------------------------------------- #
# Input handling
# --------------------------------------------------------------------------- #
def parse_args() -> argparse.Namespace:
    """Read command-line options."""
    parser = argparse.ArgumentParser(
        description="Move all .jpg files from a folder into a new folder."
    )
    parser.add_argument("source", nargs="?", help="folder that contains the images")
    parser.add_argument(
        "destination",
        nargs="?",
        help=f"folder to move them into (default: SOURCE/{DEFAULT_DESTINATION_NAME})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="show what would be moved without moving anything",
    )
    return parser.parse_args()


def ask_source_folder() -> str:
    """Prompt until the user enters an existing folder."""
    while True:
        answer = input("Folder with your images: ").strip().strip('"').strip("'")
        if os.path.isdir(answer):
            return os.path.abspath(answer)
        print("  That folder does not exist. Please try again.")


def ask_destination_folder(default: str) -> str:
    """Prompt for the destination folder; Enter accepts the default."""
    answer = input(f"Move images to [{default}]: ").strip().strip('"').strip("'")
    return os.path.abspath(answer) if answer else default


# --------------------------------------------------------------------------- #
# Program entry point
# --------------------------------------------------------------------------- #
def main() -> int:
    """Run the JPG organizer. Returns a process exit code."""
    args = parse_args()

    print("=" * 50)
    print("                 JPG ORGANIZER")
    print("=" * 50)

    try:
        # Source folder
        if args.source is None:
            source = ask_source_folder()
        elif os.path.isdir(args.source):
            source = os.path.abspath(args.source)
        else:
            print(f"Error: '{args.source}' is not a folder.")
            return 1

        # Destination folder
        default_destination = os.path.join(source, DEFAULT_DESTINATION_NAME)
        if args.destination is not None:
            destination = os.path.abspath(args.destination)
        elif args.source is None:
            destination = ask_destination_folder(default_destination)
        else:
            destination = default_destination

        if os.path.normcase(destination) == os.path.normcase(source):
            print("Error: the destination must be different from the source.")
            return 1

        mode = " (dry run, nothing will be changed)" if args.dry_run else ""
        print(f"\nSource:      {source}")
        print(f"Destination: {destination}{mode}\n")

        summary = move_jpg_files(source, destination, dry_run=args.dry_run)

    except (KeyboardInterrupt, EOFError):
        print("\nCancelled.")
        return 130
    except OSError as error:
        print(f"Error: {error}")
        return 1

    if summary["found"] == 0:
        print("No .jpg files were found. Nothing to do.")
    else:
        verb = "would be moved" if args.dry_run else "moved"
        print(f"\nDone. {summary['found']} found, "
              f"{summary['moved']} {verb}, {summary['failed']} failed.")

    return 0 if summary["failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())