from unittest.mock import Mock, patch

import httpx
import pytest

from bnc.utils import (
    calculate_bulls_and_cows,
    check_color,
    generate_guess,
    get_random_number,
    validate_code_input,
)


class TestCheckColor:
    def test_valid_colors(self):
        assert check_color(1, 6) is True
        assert check_color(6, 6) is True
        assert check_color(3, 8) is True

    def test_invalid_colors(self):
        assert check_color(0, 6) is False
        assert check_color(7, 6) is False
        assert check_color(-1, 6) is False
        assert check_color(10, 6) is False


class TestValidateCodeInput:
    def test_valid_code(self):
        result = validate_code_input("1234", 4, 6)
        assert result == [1, 2, 3, 4]

    def test_valid_code_max_colors(self):
        result = validate_code_input("6666", 4, 6)
        assert result == [6, 6, 6, 6]

    def test_wrong_length(self):
        with pytest.raises(ValueError, match="Code must be exactly 4 digits long"):
            validate_code_input("123", 4, 6)

        with pytest.raises(ValueError, match="Code must be exactly 4 digits long"):
            validate_code_input("12345", 4, 6)

    def test_non_digits(self):
        with pytest.raises(ValueError, match="Code must contain only digits"):
            validate_code_input("12ab", 4, 6)

        with pytest.raises(ValueError, match="Code must contain only digits"):
            validate_code_input("a234", 4, 6)

    def test_out_of_range_colors(self):
        with pytest.raises(ValueError, match="Digit 7 is out of range"):
            validate_code_input("1237", 4, 6)

        with pytest.raises(ValueError, match="Digit 0 is out of range"):
            validate_code_input("1230", 4, 6)

    def test_empty_string(self):
        with pytest.raises(ValueError, match="Code must be exactly 4 digits long"):
            validate_code_input("", 4, 6)


class TestCalculateBullsAndCows:
    def test_all_bulls(self):
        bulls, cows = calculate_bulls_and_cows([1, 2, 3, 4], [1, 2, 3, 4])
        assert bulls == 4
        assert cows == 0

    def test_all_cows(self):
        bulls, cows = calculate_bulls_and_cows([1, 2, 3, 4], [4, 3, 2, 1])
        assert bulls == 0
        assert cows == 4

    def test_no_matches(self):
        bulls, cows = calculate_bulls_and_cows([1, 2, 3, 4], [5, 5, 6, 6])
        assert bulls == 0
        assert cows == 0

    def test_mixed_bulls_cows(self):
        bulls, cows = calculate_bulls_and_cows([1, 2, 3, 4], [1, 3, 2, 5])
        assert bulls == 1
        assert cows == 2

    def test_duplicate_in_secret(self):
        bulls, cows = calculate_bulls_and_cows([1, 1, 2, 3], [1, 2, 1, 1])
        assert bulls == 1
        assert cows == 2

    def test_duplicate_in_guess(self):
        bulls, cows = calculate_bulls_and_cows([1, 2, 3, 4], [1, 1, 1, 1])
        assert bulls == 1
        assert cows == 0

    def test_multiple_duplicates(self):
        bulls, cows = calculate_bulls_and_cows([1, 1, 2, 2], [2, 2, 1, 1])
        assert bulls == 0
        assert cows == 4

    def test_empty_secret(self):
        with pytest.raises(ValueError, match="Secret code must be set"):
            calculate_bulls_and_cows([], [1, 2, 3, 4])


class TestGenerateGuess:
    def test_correct_length(self):
        guess = generate_guess(4, 6)
        assert len(guess) == 4

    def test_all_digits(self):
        guess = generate_guess(5, 8)
        assert guess.isdigit()

    def test_valid_range(self):
        for _ in range(100):
            guess = generate_guess(4, 6)
            for digit in guess:
                assert 1 <= int(digit) <= 6

    def test_different_lengths(self):
        assert len(generate_guess(3, 6)) == 3
        assert len(generate_guess(6, 6)) == 6
        assert len(generate_guess(10, 6)) == 10

    @patch("bnc.utils.random.randint")
    def test_randomness(self, mock_randint):
        mock_randint.side_effect = [1, 2, 3, 4]
        guess = generate_guess(4, 6)
        assert guess == "1234"
        assert mock_randint.call_count == 4


class TestGetRandomNumber:
    def test_custom_length(self):
        with patch("bnc.utils.random.randint", side_effect=[1, 2, 3, 4, 5]):
            result = get_random_number(length=5)
            assert len(result) == 5

    def test_invalid_length(self):
        with pytest.raises(ValueError, match="Length must be a positive integer"):
            get_random_number(length=0)

        with pytest.raises(ValueError, match="Length must be a positive integer"):
            get_random_number(length=-1)

    def test_invalid_range(self):
        with pytest.raises(
            ValueError, match="min_value .* must be less than max_value"
        ):
            get_random_number(min_value=5, max_value=5)

        with pytest.raises(
            ValueError, match="min_value .* must be less than max_value"
        ):
            get_random_number(min_value=10, max_value=5)

    def test_invalid_base(self):
        with pytest.raises(ValueError, match="Base value must be 2, 8, 10, or 16"):
            get_random_number(base=3)

    def test_negative_min_value(self):
        with pytest.raises(ValueError, match="min_value cannot be negative"):
            get_random_number(min_value=-1)

    @patch("bnc.utils.httpx.get")
    def test_api_success(self, mock_get):
        mock_response = Mock()
        mock_response.text = "1 2 3 4"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = get_random_number(length=4, min_value=1, max_value=6)
        assert result == "1234"

        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert args[0] == "https://www.random.org/integers/"
        assert kwargs["params"]["num"] == 4
        assert kwargs["params"]["min"] == 1
        assert kwargs["params"]["max"] == 6

    @patch("bnc.utils.httpx.get")
    def test_api_failure_fallback(self, mock_get):
        mock_get.side_effect = httpx.RequestError("Connection failed")

        with patch("bnc.utils.random.randint", side_effect=[1, 2, 3, 4]):
            result = get_random_number(length=4)
            assert result == "1234"

    @patch("bnc.utils.httpx.get")
    def test_api_http_error_fallback(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Server error", request=Mock(), response=Mock()
        )
        mock_get.return_value = mock_response

        with patch("bnc.utils.random.randint", side_effect=[5, 6, 5, 6]):
            result = get_random_number(length=4)
            assert result == "5656"

    @patch("bnc.utils.httpx.get")
    def test_api_wrong_response_length(self, mock_get):
        mock_response = Mock()
        mock_response.text = "1 2 3"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        with patch("bnc.utils.random.randint", side_effect=[4, 3, 2, 1]):
            result = get_random_number(length=4)
            assert result == "4321"

    @patch("bnc.utils.httpx.get")
    @patch("bnc.utils.logger")
    def test_logging_on_api_failure(self, mock_logger, mock_get):
        mock_get.side_effect = httpx.RequestError("Network error")

        with patch("bnc.utils.random.randint", side_effect=[1, 2, 3, 4]):
            get_random_number(length=4)

        mock_logger.warning.assert_called_once()
        warning_msg = mock_logger.warning.call_args[0][0]
        assert "Failed to get random number from API" in warning_msg
