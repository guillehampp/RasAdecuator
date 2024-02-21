from main import load_config
import os
import unittest

class TestMain(unittest.TestCase):
    def setUp(self) -> None:
        self.config = load_config()
    def test_load_config(self):
        self.assertEqual(self.config.get('workspace_l0f_input'), "workspaceL0F/inputDir")