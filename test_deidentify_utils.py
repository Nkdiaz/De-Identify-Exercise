import unittest
from deidentify_utils import calculate_age, zipcode_mask, zipcode_clean, extract_year, notes_cleanup

class CalculateAgeTest(unittest.TestCase):
    def test_calculate_ages_low(self): 
        self.assertEqual(calculate_age("2000-01-01"),"19") 
    def test_calculate_ages_high(self):
        self.assertEqual(calculate_age("1901-01-01"),"90+")

class ZipcodeMaskTest(unittest.TestCase):
    def test_zipcode_mask(self):
        self.assertEqual(zipcode_mask("10013"), "100")
    def test_zipcode_clean(self):
        self.assertEqual(zipcode_clean("100"), "10000")
    def test_zipcode_clean(self):
        self.assertEqual(zipcode_clean("10222"), "00000")

class ExtractYearTest(unittest.TestCase):
    def test_admin_date(self):
        self.assertEqual(extract_year("2019-03-12"), "2019")
    def test_disc_date(self):
        self.assertEqual(extract_year("2017-03-12"), "2017")

class NotesCleanTest(unittest.TestCase):
    def test_ssn_cleaned(self):
        self.assertEqual(notes_cleanup("123-45-6789"), "XXX-XX-XXXX")
    def test_email_cleaned(self):
        self.assertEqual(notes_cleanup("nkdiaz@gmail.com"), "@email")
    def test_phone_dash_cleaned(self):
        self.assertEqual(notes_cleanup("703-775-8765"), "(XXX)-XXX-XXXX")
    def test_phone_cleaned(self):
        self.assertEqual(notes_cleanup("7037758765"), "(XXX)-XXX-XXXX")
    def test_year_cleaned(self):
        self.assertEqual(notes_cleanup("2019-03-12"), "2019")

if __name__ == '__main__':
    unittest.main()
     

