"""
Test Environment Setup Script
-----------------------------
Prepares sample test directories and files for CodeAlpha_File_Organizer_Automation.

Creates:
- test_files/source/
    ├── photo1.jpg
    ├── photo2.jpg
    ├── image.jpg
    ├── profile.jpg
    ├── vacation.JPG         (Tests case-insensitive matching)
    ├── screenshot.png       (Unrelated file - should NOT be moved)
    ├── report.pdf           (Unrelated file - should NOT be moved)
    ├── notes.txt            (Unrelated file - should NOT be moved)
    └── project.docx         (Unrelated file - should NOT be moved)

- test_files/destination/
    (Empty or pre-seeded to demonstrate collision resolution)
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = os.path.join(BASE_DIR, "test_files", "source")
DEST_DIR = os.path.join(BASE_DIR, "test_files", "destination")


def create_sample_files(seed_conflict: bool = False):
    """
    Creates sample dummy files in test_files/source and test_files/destination.
    """
    print(f"Setting up test environment in: {os.path.join(BASE_DIR, 'test_files')}")

    # Ensure clean directories
    os.makedirs(SOURCE_DIR, exist_ok=True)
    os.makedirs(DEST_DIR, exist_ok=True)

    # List of JPG files to generate
    jpg_samples = [
        ("photo1.jpg", "Sample binary/text content representing photo1.jpg"),
        ("photo2.jpg", "Sample binary/text content representing photo2.jpg"),
        ("image.jpg", "Sample binary/text content representing image.jpg"),
        ("profile.jpg", "Sample binary/text content representing profile.jpg"),
        ("vacation.JPG", "Sample binary/text content representing vacation.JPG (uppercase extension)"),
    ]

    # List of Non-JPG files that MUST NOT be moved
    unrelated_samples = [
        ("screenshot.png", "PNG image file data - must remain in source"),
        ("report.pdf", "%PDF-1.4 dummy pdf document - must remain in source"),
        ("notes.txt", "Plain text meeting notes - must remain in source"),
        ("project.docx", "Word document dummy - must remain in source"),
    ]

    print("\nCreating sample files in source folder...")
    for filename, content in jpg_samples + unrelated_samples:
        file_path = os.path.join(SOURCE_DIR, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  [+] Created {filename}")

    if seed_conflict:
        # Pre-seed a photo1.jpg in destination to demonstrate conflict handling
        conflict_file = os.path.join(DEST_DIR, "photo1.jpg")
        with open(conflict_file, "w", encoding="utf-8") as f:
            f.write("Pre-existing photo1 in destination")
        print(f"\n  [*] Pre-seeded conflict file in destination: {conflict_file}")

    print("\nTest environment setup complete!")
    print(f"Source Folder     : {SOURCE_DIR}")
    print(f"Destination Folder: {DEST_DIR}")


if __name__ == "__main__":
    seed_conflict_flag = "--conflict" in sys.argv
    create_sample_files(seed_conflict=seed_conflict_flag)
