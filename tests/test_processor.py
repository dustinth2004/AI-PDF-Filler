import sys
import os
import unittest
from unittest.mock import MagicMock, patch
import numpy as np

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestPDFProcessor(unittest.TestCase):
    @patch('pdf_processor.fitz')
    @patch('pdf_processor.cv2')
    @patch('pdf_processor.pytesseract')
    @patch('pdf_processor.requests')
    @patch('pdf_processor.os')
    @patch('pdf_processor.Image')
    @patch('pdf_processor.ImageDraw')
    @patch('pdf_processor.ImageFont')
    def test_process_pdf_flow(self, mock_image_font, mock_image_draw, mock_image, mock_os, mock_requests, mock_pytesseract, mock_cv2, mock_fitz):

        # Setup Mocks

        # Mock ImageDraw
        mock_draw_instance = MagicMock()
        mock_image_draw.Draw.return_value = mock_draw_instance
        # textbbox returns (left, top, right, bottom)
        mock_draw_instance.textbbox.return_value = (0, 0, 10, 10)

        # Mock ImageFont
        mock_image_font.truetype.return_value = MagicMock()
        mock_image_font.load_default.return_value = MagicMock()

        # Mock OS path operations to work as expected
        mock_os.path.join.side_effect = os.path.join
        mock_os.path.dirname.side_effect = os.path.dirname
        mock_os.path.abspath.side_effect = os.path.abspath
        mock_os.makedirs.return_value = True
        mock_os.remove.return_value = True

        # Mock Fitz (PDF)
        mock_doc = MagicMock()
        mock_doc.__len__.return_value = 1
        mock_page = MagicMock()
        mock_doc.__getitem__.return_value = mock_page
        mock_fitz.open.return_value = mock_doc

        # Mock requests (Ollama)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '{"response": "Mocked Answer"}'
        mock_requests.post.return_value = mock_response

        # Mock cv2
        mock_img_array = np.zeros((1000, 1000, 3), dtype=np.uint8)
        mock_cv2.imread.return_value = mock_img_array
        # Mock other cv2 functions to return valid types
        mock_cv2.cvtColor.return_value = np.zeros((1000, 1000), dtype=np.uint8)

        # Mock pytesseract
        mock_pytesseract.image_to_string.return_value = "Test Field Name"
        # Mock image_to_data to return no Q/A sections to avoid complex logic there
        mock_pytesseract.image_to_data.return_value = {'text': [], 'left': [], 'top': [], 'width': [], 'height': []}
        mock_pytesseract.Output.DICT = 'dict'

        # Import the module under test
        from pdf_processor import process_pdf

        # Mock internal functions to simplify testing logic
        # We mock detect_cells to return one cell
        # We mock is_cell_empty to return True
        # We mock read_context_file to return dummy context

        with patch('pdf_processor.detect_cells') as mock_detect_cells, \
             patch('pdf_processor.is_cell_empty') as mock_is_empty, \
             patch('pdf_processor.read_context_file') as mock_read_context:

            mock_detect_cells.return_value = [(100, 100, 200, 50)] # x, y, w, h
            mock_is_empty.return_value = True
            mock_read_context.return_value = "Dummy Context Data"

            # Execute
            process_pdf("dummy_input.pdf", "output_dir", "dummy_context.txt")

            # Verifications

            # 1. Verify PDF was opened
            mock_fitz.open.assert_called_with("dummy_input.pdf")

            # 2. Verify Image Processing was called
            mock_cv2.imread.assert_called()

            # 3. Verify Ollama was called (because we found a cell and it was empty)
            mock_requests.post.assert_called()
            call_args = mock_requests.post.call_args
            self.assertIn("Test Field Name", call_args[1]['json']['prompt'])
            self.assertIn("Dummy Context Data", call_args[1]['json']['prompt'])

            print("\nTest passed: PDF Processing flow verified with mocks.")

if __name__ == '__main__':
    unittest.main()
