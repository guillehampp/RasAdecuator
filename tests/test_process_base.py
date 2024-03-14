import os
import unittest

from process_base import ProcessBase


class TestProcessBase(unittest.TestCase):
    def setUp(self) -> None:
        self.process_base = ProcessBase("test", "test", "test")
        self.temp_dir = "tests/tmp"
        self.file_paths = [
            os.path.join(self.temp_dir, "test.xml"),
        ]
        for filepath in self.file_paths:
            with open(filepath, "w") as f:
                f.write("Contenido de prueba")

    def test_find_files(self):
        self.assertEqual(
            self.process_base.find_files(".xml", "tests/tmp/"), ["tests/tmp/test.xml"]
        )
