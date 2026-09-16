"""
CodeAlpha File Organizer Automation
-----------------------------------
Task 3: Automated File Management Script
Objective: Automatically find all .jpg image files in a source folder
           and move them safely into a destination folder.

Key Modules Used:
- os: Used for interacting with the operating system, inspecting files,
      checking paths, and creating directories.
- shutil: Used for high-level file operations, specifically moving files.
"""

import os
import shutil
import sys


def clean_path(raw_path: str) -> str:
    """
    Cleans quotation marks and leading/trailing whitespace from user input.
    Commonly needed when users drag-and-drop folders into terminal prompts.
    """
    if not raw_path:
        return ""
    # Strip whitespace and surrounding single or double quotes
    return raw_path.strip().strip('"').strip("'").strip()


def validate_source_directory(source_path: str) -> bool:
    """
    Checks whether the source directory exists and is indeed a directory.

    Parameters:
        source_path (str): The folder path provided by the user.

    Returns:
        bool: True if path exists and is a valid directory, False otherwise.
    """
    if not source_path:
        print("[!] Error: Source path cannot be empty.")
        return False

    if not os.path.exists(source_path):
        print(f"[!] Error: Source folder does not exist: '{source_path}'")
        return False

    if not os.path.isdir(source_path):
        print(f"[!] Error: The path provided is a file, not a directory: '{source_path}'")
        return False

    return True


def ensure_destination_directory(destination_path: str) -> bool:
    """
    Verifies if the destination folder exists. If not, automatically creates it.

    Parameters:
        destination_path (str): The target directory path.

    Returns:
        bool: True if destination exists or was created successfully, False on error.
    """
    if not destination_path:
        print("[!] Error: Destination path cannot be empty.")
        return False

    try:
        if not os.path.exists(destination_path):
            os.makedirs(destination_path, exist_ok=True)
            print(f"[+] Destination folder did not exist. Created: '{destination_path}'")
        elif not os.path.isdir(destination_path):
            print(f"[!] Error: Destination path exists but is not a directory: '{destination_path}'")
            return False
        return True
    except OSError as error:
        print(f"[!] Failed to create destination directory: {error}")
        return False


def find_jpg_files(source_path: str) -> list[str]:
    """
    Scans the source directory and identifies all files ending with '.jpg'.
    Safely ignores subdirectories and unrelated file formats (e.g. .png, .pdf, .txt, .docx).

    Parameters:
        source_path (str): Directory to scan.

    Returns:
        list[str]: A list of filenames ending with .jpg (case-insensitive).
    """
    jpg_files = []
    try:
        entries = os.listdir(source_path)
    except PermissionError:
        print(f"[!] Permission denied: Cannot read folder '{source_path}'")
        return []
    except OSError as error:
        print(f"[!] Operating system error while reading folder: {error}")
        return []

    for entry in entries:
        full_entry_path = os.path.join(source_path, entry)
        # Check if entry is a file (exclude subdirectories)
        if os.path.isfile(full_entry_path):
            # Check for .jpg extension (case-insensitive: .jpg, .JPG, .Jpg)
            if entry.lower().endswith(".jpg"):
                jpg_files.append(entry)

    return sorted(jpg_files)


def resolve_filename_conflict(destination_path: str, filename: str) -> tuple[str, bool]:
    """
    Checks whether a file already exists in the destination folder.
    If a conflict is detected, generates a safe unique filename (e.g. photo_1.jpg)
    to prevent accidental overwrites.

    Parameters:
        destination_path (str): The target directory path.
        filename (str): The original filename.

    Returns:
        tuple[str, bool]: (resolved_destination_filepath, was_renamed)
    """
    target_path = os.path.join(destination_path, filename)

    if not os.path.exists(target_path):
        return target_path, False

    # Conflict detected: split filename and extension to insert unique counter
    base_name, extension = os.path.splitext(filename)
    counter = 1

    while True:
        new_filename = f"{base_name}_{counter}{extension}"
        new_target_path = os.path.join(destination_path, new_filename)
        if not os.path.exists(new_target_path):
            return new_target_path, True
        counter += 1


def move_jpg_files(source_path: str, destination_path: str, files: list[str]) -> list[dict]:
    """
    Moves specified JPG files from the source folder to the destination folder.
    Applies collision detection to avoid overwriting files.

    Parameters:
        source_path (str): Origin folder.
        destination_path (str): Destination folder.
        files (list[str]): List of JPG filenames to move.

    Returns:
        list[dict]: List of operation records with status, original name, and final path.
    """
    results = []

    for filename in files:
        src_file = os.path.join(source_path, filename)
        dest_file, was_renamed = resolve_filename_conflict(destination_path, filename)
        final_filename = os.path.basename(dest_file)

        try:
            shutil.move(src_file, dest_file)
            results.append({
                "original_name": filename,
                "final_name": final_filename,
                "was_renamed": was_renamed,
                "status": "success",
                "destination_path": dest_file,
            })
        except (shutil.Error, OSError, PermissionError) as err:
            results.append({
                "original_name": filename,
                "final_name": final_filename,
                "was_renamed": was_renamed,
                "status": "failed",
                "error": str(err),
            })

    return results


def organize_jpg_files(source_path: str, destination_path: str) -> None:
    """
    High-level orchestrator that coordinates validation, discovery, and file transfer.
    """
    # 1. Clean and normalize paths
    clean_src = os.path.abspath(clean_path(source_path))
    clean_dst = os.path.abspath(clean_path(destination_path))

    # Guard: prevent source and destination from being identical
    if os.path.normpath(clean_src) == os.path.normpath(clean_dst):
        print("\n[!] Error: Source and Destination folders cannot be the same path.")
        return

    print("\n" + "=" * 55)
    print("CODEALPHA FILE ORGANIZER: SCAN & MOVE PROCESS")
    print("=" * 55)
    print(f"Source Folder     : {clean_src}")
    print(f"Destination Folder: {clean_dst}")
    print("-" * 55)

    # 2. Validate Source Folder
    if not validate_source_directory(clean_src):
        return

    # 3. Ensure Destination Folder Exists
    if not ensure_destination_directory(clean_dst):
        return

    # 4. Search for .jpg files
    jpg_files = find_jpg_files(clean_src)
    total_found = len(jpg_files)

    print(f"\nFound {total_found} JPG file{'s' if total_found != 1 else ''}.")

    # 5. Handle case where no JPG files exist
    if total_found == 0:
        print("[i] No JPG files were found in the source directory.")
        print("[i] Non-JPG files (e.g. .png, .pdf, .txt, .docx) were left untouched.")
        print("-" * 55)
        print("Total files moved: 0")
        return

    # 6. Execute File Move
    print("\nMoving files...")
    move_results = move_jpg_files(clean_src, clean_dst, jpg_files)

    successful_moves = [r for r in move_results if r["status"] == "success"]
    failed_moves = [r for r in move_results if r["status"] == "failed"]

    # 7. Display Results
    if successful_moves:
        print("\nMoved:")
        for item in successful_moves:
            if item["was_renamed"]:
                print(f"  - {item['original_name']} -> {item['final_name']} (Renamed to prevent overwrite)")
            else:
                print(f"  - {item['final_name']}")

    if failed_moves:
        print("\n[!] Warnings / Failed Moves:")
        for item in failed_moves:
            print(f"  - {item['original_name']}: {item.get('error', 'Unknown error')}")

    print("-" * 55)
    print(f"Successfully moved {len(successful_moves)} file{'s' if len(successful_moves) != 1 else ''}.")
    if failed_moves:
        print(f"Failed to move {len(failed_moves)} file(s).")
    print("=" * 55)


def main():
    """
    Command-line interface entry point.
    Interactively requests source and destination paths from the user.
    """
    print("\n=======================================================")
    print("      CodeAlpha File Organizer Automation (Task 3)    ")
    print("=======================================================")
    print("This script moves all .jpg images from a source folder")
    print("to a destination folder while safely ignoring other files.\n")

    # Prompt user for source path
    user_source = input("Enter Source Folder Path: ").strip()
    if not user_source:
        print("[!] Exiting: Source path is required.")
        sys.exit(1)

    # Prompt user for destination path
    user_destination = input("Enter Destination Folder Path: ").strip()
    if not user_destination:
        print("[!] Exiting: Destination path is required.")
        sys.exit(1)

    organize_jpg_files(user_source, user_destination)


if __name__ == "__main__":
    main()
