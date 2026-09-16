"""
Unit Tests for CodeAlpha_File_Organizer_Automation
--------------------------------------------------
Uses Python's standard `unittest` and `tempfile` modules
to rigorously verify all core automation functions without
modifying user files.
"""

import os
import shutil
import tempfile
import unittest

from main import (
    clean_path,
    validate_source_directory,
    ensure_destination_directory,
    find_jpg_files,
    resolve_filename_conflict,
    move_jpg_files,
)


class TestFileOrganizer(unittest.TestCase):

    def setUp(self):
        """Create isolated temporary source and destination folders for testing."""
        self.test_root = tempfile.mkdtemp()
        self.source_dir = os.path.join(self.test_root, "source")
        self.dest_dir = os.path.join(self.test_root, "destination")
        os.makedirs(self.source_dir)
        os.makedirs(self.dest_dir)

    def tearDown(self):
        """Clean up temporary test directory tree."""
        shutil.rmtree(self.test_root, ignore_errors=True)

    def test_clean_path(self):
        """Verify removal of leading/trailing spaces and quotes."""
        self.assertEqual(clean_path('  "C:/test/path"  '), "C:/test/path")
        self.assertEqual(clean_path(" 'C:/another/path' "), "C:/another/path")
        self.assertEqual(clean_path(""), "")

    def test_validate_source_directory_valid(self):
        """Test valid directory returns True."""
        self.assertTrue(validate_source_directory(self.source_dir))

    def test_validate_source_directory_non_existent(self):
        """Test non-existent directory returns False."""
        fake_path = os.path.join(self.test_root, "does_not_exist")
        self.assertFalse(validate_source_directory(fake_path))

    def test_validate_source_directory_file_instead_of_dir(self):
        """Test file path returns False when expected to be a directory."""
        dummy_file = os.path.join(self.test_root, "file.txt")
        with open(dummy_file, "w") as f:
            f.write("sample")
        self.assertFalse(validate_source_directory(dummy_file))

    def test_ensure_destination_directory(self):
        """Test creating new destination directory automatically."""
        new_dest = os.path.join(self.test_root, "new_dest_folder")
        self.assertFalse(os.path.exists(new_dest))
        self.assertTrue(ensure_destination_directory(new_dest))
        self.assertTrue(os.path.exists(new_dest))
        self.assertTrue(os.path.isdir(new_dest))

    def test_find_jpg_files_filtering(self):
        """Verify only .jpg and .JPG files are found, ignoring unrelated extensions."""
        # Create JPG files
        for name in ["pic1.jpg", "pic2.jpg", "PICTURE.JPG"]:
            with open(os.path.join(self.source_dir, name), "w") as f:
                f.write("jpg data")

        # Create unrelated files
        for name in ["notes.txt", "vector.png", "doc.pdf", "presentation.docx"]:
            with open(os.path.join(self.source_dir, name), "w") as f:
                f.write("other data")

        # Create a subdirectory that has .jpg in name to verify folders are excluded
        os.makedirs(os.path.join(self.source_dir, "fake_folder.jpg"))

        found = find_jpg_files(self.source_dir)
        self.assertEqual(sorted(found), ["PICTURE.JPG", "pic1.jpg", "pic2.jpg"])
        self.assertNotIn("notes.txt", found)
        self.assertNotIn("vector.png", found)
        self.assertNotIn("doc.pdf", found)
        self.assertNotIn("presentation.docx", found)
        self.assertNotIn("fake_folder.jpg", found)

    def test_resolve_filename_conflict(self):
        """Verify collision avoidance renames files with numeric suffix."""
        # Create existing file in destination
        with open(os.path.join(self.dest_dir, "photo.jpg"), "w") as f:
            f.write("original photo")

        resolved_path, was_renamed = resolve_filename_conflict(self.dest_dir, "photo.jpg")
        self.assertTrue(was_renamed)
        self.assertTrue(resolved_path.endswith("photo_1.jpg"))

        # Create photo_1.jpg in destination to test second collision
        with open(resolved_path, "w") as f:
            f.write("second photo")

        resolved_path_2, was_renamed_2 = resolve_filename_conflict(self.dest_dir, "photo.jpg")
        self.assertTrue(was_renamed_2)
        self.assertTrue(resolved_path_2.endswith("photo_2.jpg"))

    def test_move_jpg_files(self):
        """Verify moving files from source to destination."""
        # Create files in source
        with open(os.path.join(self.source_dir, "img1.jpg"), "w") as f:
            f.write("image 1")
        with open(os.path.join(self.source_dir, "keep.txt"), "w") as f:
            f.write("stay here")

        results = move_jpg_files(self.source_dir, self.dest_dir, ["img1.jpg"])

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["status"], "success")
        self.assertFalse(os.path.exists(os.path.join(self.source_dir, "img1.jpg")))
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, "img1.jpg")))
        # Ensure unrelated file was untouched
        self.assertTrue(os.path.exists(os.path.join(self.source_dir, "keep.txt")))


if __name__ == "__main__":
    unittest.main()
