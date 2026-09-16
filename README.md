# 📁 CodeAlpha File Organizer Automation ⚡

<div align="center">

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=for-the-badge)](https://www.python.org/)
[![CodeAlpha Task](https://img.shields.io/badge/CodeAlpha-Task%203-orange.svg?style=for-the-badge)](https://www.codealpha.tech/)
[![Code Style: PEP 8](https://img.shields.io/badge/Code%20Style-PEP%208-brightgreen.svg?style=for-the-badge)](https://pep8.org/)

**A clean, robust, and safe Python automation tool that scans directories, detects `.jpg` image files, and safely organizes them into a target destination folder without data loss.**

[Key Features](#-key-features) •
[Quick Start](#-quick-start--installation) •
[How It Works](#-how-the-automation-works) •
[Function Guide](#-function-documentation) •
[Testing](#-testing--verification)

</div>

---

## 📌 Table of Contents

- [📖 Project Overview](#-project-overview)
- [🎯 Problem Statement](#-problem-statement)
- [🏆 Objectives](#-objectives)
- [✨ Key Features](#-key-features)
- [⚙️ How the Automation Works](#-how-the-automation-works)
- [🛠️ Technologies & Modules Used](#-technologies--modules-used)
- [📂 Project Directory Structure](#-project-directory-structure)
- [🚀 Quick Start & Installation](#-quick-start--installation)
- [💻 How to Run](#-how-to-run)
- [📋 Example Input & Output](#-example-input--output)
- [🧩 Function Documentation](#-function-documentation)
- [🧪 Testing & Verification](#-testing--verification)
- [🛡️ Safety Considerations & Conflict Resolution](#-safety-considerations--conflict-resolution)
- [🔮 Future Roadmap](#-future-roadmap)
- [📤 GitHub Upload & Repository Commands](#-github-upload--repository-commands)
- [👤 Author & Acknowledgments](#-author--acknowledgments)

---

## 📖 Project Overview

In day-to-day computer usage, directories such as `Downloads`, `Desktop`, or temporary staging folders rapidly accumulate hundreds of unorganized files: documents, spreadsheets, PDFs, screenshots, and photos. Sorting photos manually is tedious, repetitive, and error-prone.

This project, **CodeAlpha File Organizer Automation (Task 3)**, demonstrates how Python can automate real-world file management. It identifies all `.jpg` / `.JPG` images from a designated source folder, verifies directory integrity, safely creates the target folder if missing, and moves files into place while guarding against accidental overwrites.

> [!NOTE]
> This project is designed strictly using **Python's Standard Library** (`os`, `shutil`, `sys`, `unittest`), requiring **zero external `pip` dependencies**.

---

## 🎯 Problem Statement

Users often have folders cluttered with mixed extensions:
- 📄 Documents: `.pdf`, `.docx`, `.txt`, `.xlsx`
- 🖼️ Other image formats: `.png`, `.gif`, `.svg`, `.webp`
- 🎵 Media & Archives: `.mp3`, `.mp4`, `.zip`
- 📸 Target photos: `.jpg`, `.JPG`

Manually sorting these introduces friction:
1. Identifying target `.jpg` images from a crowded folder takes time.
2. Inadvertent selection risks moving or deleting critical non-image files.
3. Target directories might not exist yet, causing typical scripts to crash.
4. If a destination file already shares the same name, standard copy/move scripts overwrite and permanently destroy existing files.

---

## 🏆 Objectives

- 🚀 **Automate Repetitive Work:** Move all `.jpg` images with a single command.
- 🎯 **Selective Filtering:** Strictly move `.jpg` files while leaving unrelated files completely untouched.
- 🛡️ **Non-Destructive Safety:** Ensure existing files in the destination folder are never overwritten without warning.
- 📂 **Dynamic Provisioning:** Automatically create the destination directory if it does not already exist.
- 🧼 **Clean Code Architecture:** Structured with modular, testable functions following PEP 8 conventions.

---

## ✨ Key Features

- 🔍 **Extension Filtering:** Automatically discovers `.jpg` and `.JPG` files.
- 🚫 **Unrelated File Protection:** Explicitly ignores `.png`, `.pdf`, `.txt`, `.docx`, and other file formats.
- 📁 **Subdirectory Isolation:** Ignores subfolders even if their names contain `.jpg` (e.g. `backup_jpg/`).
- 🛠️ **Automatic Directory Creation:** Automatically creates destination folder (`os.makedirs`) if missing.
- 🛡️ **Collision Avoidance:** If a file with the same name already exists in the destination, appends a numbered counter (`photo_1.jpg`, `photo_2.jpg`) to prevent data loss.
- 🧹 **Path Sanitization:** Trims quotes and extra spaces—supports dragging and dropping folders into the terminal prompt.
- 📊 **Detailed Execution Summary:** Displays the list of moved files, any renamed files, and total counts.
- 💡 **Graceful Error Handling:** Handles missing folders, permission issues, and 0-file scenarios cleanly without crashing.

---

## ⚙️ How the Automation Works

```
                     ┌────────────────────────────────┐
                     │         User Launches          │
                     │         python main.py         │
                     └───────────────┬────────────────┘
                                     │
                                     ▼
                     ┌────────────────────────────────┐
                     │      1. Path Sanitization      │
                     │  (Removes quotes & whitespace) │
                     └───────────────┬────────────────┘
                                     │
                                     ▼
                     ┌────────────────────────────────┐
                     │    2. Source Path Check        │
                     │  Exists? Is it a directory?    │
                     └───────┬────────────────┬───────┘
                        No   │                │ Yes
           ┌─────────────────┘                ▼
           ▼                         ┌────────────────────────────────┐
 ❌ Print error message              │ 3. Destination Path Check      │
    and safely stop                  │ Exists? If not: os.makedirs()  │
                                     └────────┬───────────────────────┘
                                              │
                                              ▼
                                     ┌────────────────────────────────┐
                                     │ 4. Scan & Extension Filter     │
                                     │ Check: os.path.isfile()        │
                                     │ Match: .jpg / .JPG             │
                                     │ Ignore: .png, .pdf, .txt, etc. │
                                     └────────┬───────────────────────┘
                                              │
                                              ▼
                                     ┌────────────────────────────────┐
                                     │ 5. Collision Check & Move      │
                                     │ Duplicate? -> rename to _1.jpg │
                                     │ Transfer via shutil.move()     │
                                     └────────┬───────────────────────┘
                                              │
                                              ▼
                                     ┌────────────────────────────────┐
                                     │ 6. Output Execution Summary    │
                                     │ Lists files moved & count      │
                                     └────────────────────────────────┘
```

---

## 🛠️ Technologies & Modules Used

| Icon | Module | Type | Role in Project |
| :---: | :--- | :---: | :--- |
| 🐍 | **Python 3.8+** | Core Language | Runtime execution environment |
| 🗂️ | **`os`** | Standard Library | Directory scanning (`listdir`), path joining (`path.join`), existence checks (`path.exists`), and folder creation (`makedirs`) |
| 📦 | **`shutil`** | Standard Library | High-level filesystem manipulation; safely moves files using `shutil.move` |
| 💻 | **`sys`** | Standard Library | Handles system exits and command-line parameters |
| 🧪 | **`unittest`** | Standard Library | Automated unit tests covering all functions and edge cases |

> [!TIP]
> No `pip install` required! Everything runs right out of the box with any standard Python installation.

---

## 📂 Project Directory Structure

```text
Task-automation-/
│
├── main.py                  # 🚀 Main automation script with modular functions
├── setup_test_files.py      # 🧪 Utility script to generate sample test files
├── test_main.py             # 🔍 Automated unit test suite (unittest)
├── requirements.txt         # 📋 Zero-dependency specification file
├── .gitignore               # 🙈 Git ignore rules for Python bytecode & OS files
├── README.md                # 📖 Comprehensive project documentation
└── test_files/              # 📁 Test environment sandbox
    ├── source/              # 📥 Source folder containing sample test files
    └── destination/         # 📤 Target destination folder (with .gitkeep)
```

---

## 🚀 Quick Start & Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/pranithakoyyalamudi-blip/Task-automation-.git
cd Task-automation-
```

### 2️⃣ Check Python Installation
```bash
python --version
```
*(Ensure Python 3.8 or higher is installed)*

### 3️⃣ (Optional) Generate Sample Demo Files
Before running on personal files, you can seed dummy test files:
```bash
python setup_test_files.py
```

---

## 💻 How to Run

Run the main script:
```bash
python main.py
```

You will be prompted to enter the source and destination paths:
```text
Enter Source Folder Path: test_files/source
Enter Destination Folder Path: test_files/destination
```

You can enter relative paths, absolute paths, or drag and drop folders directly from File Explorer.

---

## 📋 Example Input & Output

### 🖥️ Terminal Execution:

```text
=======================================================
      CodeAlpha File Organizer Automation (Task 3)    
=======================================================
This script moves all .jpg images from a source folder
to a destination folder while safely ignoring other files.

Enter Source Folder Path: test_files/source
Enter Destination Folder Path: test_files/destination

=======================================================
CODEALPHA FILE ORGANIZER: SCAN & MOVE PROCESS
=======================================================
Source Folder     : C:\Users\User\...\test_files\source
Destination Folder: C:\Users\User\...\test_files\destination
-------------------------------------------------------

Found 5 JPG files.

Moving files...

Moved:
  - image.jpg
  - photo1.jpg -> photo1_1.jpg (Renamed to prevent overwrite)
  - photo2.jpg
  - profile.jpg
  - vacation.JPG
-------------------------------------------------------
Successfully moved 5 files.
=======================================================
```

### 📂 Directory Status After Execution:

| Directory | Contents After Run | Note |
| :--- | :--- | :--- |
| **`test_files/destination/`** | `photo1.jpg`, `photo1_1.jpg`, `image.jpg`, `photo2.jpg`, `profile.jpg`, `vacation.JPG` | ✅ All JPG images moved safely |
| **`test_files/source/`** | `notes.txt`, `project.docx`, `report.pdf`, `screenshot.png` | 🛡️ Non-JPG files strictly preserved |

---

## 🧩 Function Documentation

Every function in [`main.py`](main.py) follows single-responsibility design:

### 1. `clean_path(raw_path: str) -> str`
- **What it does:** Strips surrounding whitespace and single/double quotation marks.
- **Why it matters:** On Windows, dragging a directory into the command prompt wraps the path in quotes (e.g. `"C:\Users\Desktop"`). Sanitizing prevents `FileNotFoundError`.

### 2. `validate_source_directory(source_path: str) -> bool`
- **What it does:** Uses `os.path.exists()` and `os.path.isdir()` to verify that the source path is valid and is a directory.
- **Why it matters:** Prevents script crashes if the user mistypes the folder path.

### 3. `ensure_destination_directory(destination_path: str) -> bool`
- **What it does:** Checks if destination folder exists. If not, invokes `os.makedirs(destination_path, exist_ok=True)`.
- **Why it matters:** Relieves the user from manually creating target folders beforehand.

### 4. `find_jpg_files(source_path: str) -> list[str]`
- **What it does:** Reads folder entries using `os.listdir()`, verifies each is a file with `os.path.isfile()`, and filters by `.lower().endswith(".jpg")`.
- **Why it matters:** Strictly isolates `.jpg` and `.JPG` files and ignores subdirectories and other formats (`.png`, `.pdf`, `.txt`, `.docx`).

### 5. `resolve_filename_conflict(destination_path: str, filename: str) -> tuple[str, bool]`
- **What it does:** Checks `os.path.exists()` for destination filenames. If a match exists, generates a safe numbered filename (e.g. `image_1.jpg`, `image_2.jpg`).
- **Why it matters:** Guarantees zero data loss—existing destination files are never destroyed.

### 6. `move_jpg_files(source_path: str, destination_path: str, files: list[str]) -> list[dict]`
- **What it does:** Moves each file using `shutil.move()` and catches individual I/O or permission errors.
- **Why it matters:** Prevents a single locked file from halting the entire batch transfer.

### 7. `organize_jpg_files(source_path: str, destination_path: str) -> None`
- **What it does:** Coordinates validation, file discovery, movement, and formatted console summaries.

### 8. `main() -> None`
- **What it does:** CLI entry point prompting user for inputs.

---

## 🧪 Testing & Verification

A dedicated automated test suite is provided in [`test_main.py`](test_main.py) using Python's built-in `unittest` module.

### Run Automated Tests:
```bash
python test_main.py
```

### Test Coverage Summary:
- ✅ **`test_clean_path`**: Verifies quotation and whitespace stripping.
- ✅ **`test_validate_source_directory_valid`**: Verifies valid directory detection.
- ✅ **`test_validate_source_directory_non_existent`**: Catches invalid directories gracefully.
- ✅ **`test_validate_source_directory_file_instead_of_dir`**: Detects if a file was provided instead of a folder.
- ✅ **`test_ensure_destination_directory`**: Verifies automatic folder creation.
- ✅ **`test_find_jpg_files_filtering`**: Validates `.jpg` and `.JPG` matching, excluding `.png`, `.pdf`, `.txt`, and folders.
- ✅ **`test_resolve_filename_conflict`**: Verifies collision avoidance counter increments.
- ✅ **`test_move_jpg_files`**: Verifies physical file relocation without corrupting source non-JPG files.

---

## 🛡️ Safety Considerations & Conflict Resolution

1. **Non-Destructive Movement:** Standard file operations often overwrite existing files silently. This script checks destination paths first and renames duplicates safely:
   $$\text{photo.jpg} \longrightarrow \text{photo\_1.jpg} \longrightarrow \text{photo\_2.jpg}$$
2. **Identical Directory Guard:** If the user specifies the same path for both source and destination, execution is halted immediately.
3. **Graceful Exception Handling:** Individual file moves are wrapped in `try-except` blocks to handle file locks or read-only attributes without crashing.

---

## 🔮 Future Roadmap

- [ ] 🎛️ **Multi-Extension Support:** Add options to categorize files by type (`.png`, `.pdf`, `.docx`, `.mp4`).
- [ ] 📅 **Date-Based Organization:** Organize photos into subfolders by year and month from EXIF metadata.
- [ ] 🖥️ **Desktop GUI:** Add a Tkinter or PyQt graphical user interface with folder pickers.
- [ ] 📋 **Copy vs. Move Mode:** Allow toggling between moving (deleting from source) and copying.

---

## 📤 GitHub Upload & Repository Commands

To push this repository to GitHub:

```bash
# 1. Check current status
git status

# 2. Stage all files
git add .

# 3. Commit changes
git commit -m "docs: enhance README with icons, badges, and detailed architecture"

# 4. Set remote origin
git remote set-url origin https://github.com/pranithakoyyalamudi-blip/Task-automation-.git

# 5. Push to GitHub main branch
git push -u origin main
```

---

## 👤 Author & Acknowledgments

- **Intern:** Harsh
- **Program:** CodeAlpha Python Programming Internship
- **Task:** Task 3 — File Organizer Automation
- **Organization:** [CodeAlpha](https://www.codealpha.tech/)