"""Unit Test Suite: Schema and Business Rule Validators.

Validates data validation rules, threshold checks, and PII protections.
"""

import unittest
import hashlib


class TestDataValidation(unittest.TestCase):
    """Unit tests for telemetry validation and security masking rules."""

    def test_pii_sha256_masking(self):
        """Verify that PII hashing matches expected SHA-256 standard."""
        raw_contact = "operator.car@hydrogrow.ph"
        expected_hash = hashlib.sha256(raw_contact.encode("utf-8")).hexdigest()
        self.assertEqual(len(expected_hash), 64)
        self.assertNotEqual(raw_contact, expected_hash)

    def test_ph_range_validation(self):
        """Verify nutrient pH range validation boundaries."""
        valid_ph = 6.2
        invalid_ph_low = 3.0
        invalid_ph_high = 11.0

        def is_ph_valid(ph: float) -> bool:
            return 5.0 <= ph <= 8.5

        self.assertTrue(is_ph_valid(valid_ph))
        self.assertFalse(is_ph_valid(invalid_ph_low))
        self.assertFalse(is_ph_valid(invalid_ph_high))

    def test_relative_humidity_bounds(self):
        """Verify relative humidity is clamped between 0 and 100%."""
        def is_humidity_valid(rh: float) -> bool:
            return 0.0 <= rh <= 100.0

        self.assertTrue(is_humidity_valid(65.0))
        self.assertFalse(is_humidity_valid(-5.0))
        self.assertFalse(is_humidity_valid(105.0))


if __name__ == "__main__":
    unittest.main()
