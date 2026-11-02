# JPG Organizer

A small command-line tool written in Python that moves all `.jpg` / `.jpeg` images from a folder into a separate folder. It can run interactively or with command-line arguments, and includes a dry-run mode so you can preview changes before anything is moved.

## Features

- Finds `.jpg` and `.jpeg` files, ignoring letter case (`PHOTO.JPG` is matched too)
- Only looks at files directly inside the source folder (sub-folders are not searched)
- Creates the destination folder automatically if it does not exist
- Never overwrites files: name clashes are renamed (`photo.jpg` becomes `photo_1.jpg`, `photo_2.jpg`, ...)
- `--dry-run` mode to preview what would happen without moving anything
- Interactive prompts when no arguments are given
- Per-file status messages and a final summary
- Safe handling of errors and `Ctrl+C`
- No external dependencies (standard library only)

## Requirements

- **Python 3.9 or newer** (the code uses the `list[str]` type hint)

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/<your-username>/<your-repo>.git
   cd <your-repo>
   ```

2. Run the program:

   ```bash
   python ORGANIZER.py
   ```

   Use `python3` on some systems.

## Usage

```
python ORGANIZER.py [source] [destination] [--dry-run]
```

| Argument | Description |
|----------|-------------|
| `source` | Folder that contains the images (optional; you are prompted if omitted) |
| `destination` | Folder to move them into (optional; default is `SOURCE/jpg_images`) |
| `--dry-run` | Show what would be moved without moving anything |
| `-h`, `--help` | Show the help message |

### Examples

Interactive mode (the program asks for the folders):

```bash
python ORGANIZER.py
```

Move images using the default destination (`<source>/jpg_images`):

```bash
python ORGANIZER.py ~/Pictures
```

Choose your own destination:

```bash
python ORGANIZER.py ~/Downloads ~/Pictures/Photos
```

Preview first without changing anything:

```bash
python ORGANIZER.py ~/Downloads --dry-run
```

### Example Output

```
==================================================
                 JPG ORGANIZER
==================================================

Source:      /home/user/Downloads
Destination: /home/user/Downloads/jpg_images

  [moved]   beach.jpg
  [moved]   photo.jpg  (renamed to photo_1.jpg)
  [failed]  locked.JPG: [Errno 13] Permission denied

Done. 3 found, 2 moved, 1 failed.
```

## How It Works

| Function | Purpose |
|----------|---------|
| `find_jpg_files()` | Lists JPG files in the source folder (case-insensitive, sorted) |
| `get_unique_path()` | Finds a free filename so nothing is overwritten |
| `move_jpg_files()` | Moves the files (or simulates it in dry-run mode) and returns a summary |
| `parse_args()` | Reads command-line options |
| `ask_source_folder()` / `ask_destination_folder()` | Interactive prompts |
| `main()` | Program entry point, returns an exit code |

## Exit Codes

| Code | Meaning |
|-----:|---------|
| 0 | Success (including when no JPG files were found) |
| 1 | An error occurred, or at least one file failed to move |
| 130 | Cancelled by the user (`Ctrl+C`) |

## Notes

- The source and destination must be different folders.
- Files are **moved**, not copied. Use `--dry-run` first if you want to check the result.
- Only `.jpg` and `.jpeg` files are handled. To support other formats, edit `JPG_EXTENSIONS` at the top of the script.

## Ideas for Improvement

- Support more image types (PNG, GIF, WebP)
- Optional recursive search through sub-folders
- Copy mode instead of move
- Sort images into folders by date
- Unit tests for the file-finding and renaming logic

## Contributing

Suggestions and pull requests are welcome.

## License

Add a license of your choice (for example MIT).
