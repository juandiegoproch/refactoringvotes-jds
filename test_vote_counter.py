import unittest
from unittest.mock import patch, mock_open
from io import StringIO
from vote_counter import count_votes  # Assuming your code is in 'your_module.py'

class TestVoteCounter(unittest.TestCase):

    @patch("builtins.print")
    def test_count_votes_valid_file(self, mock_print):
        mock_csv = """city,candidate,votes
        Springfield,Alice,1200
        Springfield,Bob,750
        Shelbyville,Alice,2000
        Shelbyville,Bob,2500"""
        
        # Mock file opening and reading
        with patch("builtins.open", mock_open(read_data=mock_csv)):
            count_votes("votes.csv")
        
        # Expected output after tallying votes
        mock_print.assert_any_call("Alice: 3200 votes")
        mock_print.assert_any_call("Bob: 3250 votes")
        mock_print.assert_any_call("winner is Bob")
        self.assertEqual(mock_print.call_count, 3)

    @patch("builtins.print")
    def test_count_votes_invalid_votes(self, mock_print):
        # Simulate a CSV file with invalid votes data
        mock_csv = """city,candidate,votes
        Springfield,Bob,750
        Shelbyville,Alice,2000
        Springfield,Alice,invalid
        Shelbyville,Bob,2500"""
        
        # Mock file opening and reading
        with patch("builtins.open", mock_open(read_data=mock_csv)):
            count_votes("votes.csv")
        
        # Expect Alice to be skipped due to invalid data, only Bob's votes should print correctly
        mock_print.assert_any_call("Bob: 3250 votes")
        mock_print.assert_any_call("Alice: 2000 votes")
        mock_print.assert_any_call("winner is Bob")
        self.assertEqual(mock_print.call_count, 3)

    @patch("builtins.print")
    def test_count_votes_tie(self, mock_print):
        # Simulate a CSV file where there is a tie in votes
        mock_csv = """city,candidate,votes
        Springfield,Alice,1000
        Springfield,Bob,1000
        Shelbyville,Alice,1000
        Shelbyville,Bob,1000"""
        
        with patch("builtins.open", mock_open(read_data=mock_csv)):
            count_votes("votes.csv")
        
        # Check that both candidates are printed
        mock_print.assert_any_call("Alice: 2000 votes")
        mock_print.assert_any_call("Bob: 2000 votes")
        
        # Check if the winner is correctly printed (could be either Alice or Bob, depending on how you sort)
        mock_print.assert_any_call("There was a tie")  # or "winner is Bob", depending on sorting order
        self.assertEqual(mock_print.call_count, 3)

    @patch("builtins.print")
    def test_count_votes_single_candidate(self, mock_print):
        mock_csv = """city,candidate,votes
        Springfield,Alice,1000"""
        
        with patch("builtins.open", mock_open(read_data=mock_csv)):
            count_votes("votes.csv")
        
        mock_print.assert_any_call("Alice: 1000 votes")
        mock_print.assert_any_call("winner is Alice")
        self.assertEqual(mock_print.call_count, 2)

    @patch("builtins.print")
    def test_count_votes_negative_votes(self, mock_print):
        mock_csv = """city,candidate,votes
        Springfield,Alice,-500
        Shelbyville,Bob,-300"""
        
        with patch("builtins.open", mock_open(read_data=mock_csv)):
            count_votes("votes.csv")
        
        mock_print.assert_any_call("Alice: -500 votes")
        mock_print.assert_any_call("Bob: -300 votes")
        mock_print.assert_any_call("winner is Bob")
        self.assertEqual(mock_print.call_count, 3)
if __name__ == "__main__":
    unittest.main()
