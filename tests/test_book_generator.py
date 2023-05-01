import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
from dataclasses import dataclass
from backend.tools import BookGenerator, BookParams

class TestBookGenerator(unittest.TestCase):
    def setUp(self):
        self.test_params = BookParams(
            title="Test Title",
            author="Test Author",
            synopsis="Test Synopsis",
            page_width=5,
            page_height=8,
            margin=1,
        )

    def test_generate(self):
        with patch("backend.models.OpenAIModel") as mock_model:
            mock_model_instance = MagicMock()
            mock_model.return_value = mock_model_instance

            BookGenerator.generate(self.test_params)

            mock_model.assert_called_once_with("gpt-3.5-turbo")
            mock_model_instance.generate.assert_called_once()

    def test_build(self):
        BookGenerator.build(self.test_params)

        tex_file = Path(f"output/{self.test_params.title}.tex")
        self.assertTrue(tex_file.is_file())

        # Clean up the generated test file
        tex_file.unlink()

if __name__ == '__main__':
    unittest.main()
