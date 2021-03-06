#!/bin/env python3

import unittest
from datetime import datetime

from src.database.data_structure import DataStructure


class Test(unittest.TestCase):

    def test_data_structure(self):
        well = DataStructure()
        well.ID = 123
        well.Name = 'WellName'
        
        # This returns a dictionary object for the attributes in an object
        dd = vars(well)
        self.assertEqual(len(dd), 4)
        self.assertIn('_format', dd)  # The format attribute is used for formatting.
        self.assertIn('_original', dd)  # Used for comparing differences.
        self.assertEqual(dd['ID'], 123)
        self.assertEqual(dd['Name'], 'WellName')
        
    def test_format_lease(self):
        """ This is the old way of formatting attributes and will be deprecated shortly: test_formatter_lease
        for the new way """
        well = DataStructure()
        well.ID = 123
        well.LeaseType = 'OL'
        
        # If there is no attribute in the object called 'LeaseID' use the ID attribute to format the lease string
        self.assertEqual(well.Lease, 'OL-0123')

        well.LeaseID = 1
        # If there is an attribute in the object called 'LeaseID' use it to format the lease string
        self.assertEqual(well.Lease, 'OL-0001')

    def test_formatter_date(self):
        monthly = DataStructure()
        monthly.ID = 123
        monthly.ExtractMonth = datetime(2016, 2, 22)
        self.assertEqual(monthly._format.yyyy_mm_dd(monthly.ExtractMonth), '2016-02-22')
        self.assertEqual(monthly._format.yyyy_mm_dd(None), '')

    def test_formatter_lease(self):
        well = DataStructure()
        well.ID = 123
        well.LeaseType = 'OL'
        
        # If there is no attribute in the object called 'LeaseID' use the ID attribute to format the lease string
        self.assertEqual(well._format.Lease, 'OL-0123')

        well.LeaseID = 1
        # If there is an attribute in the object called 'LeaseID' use it to format the lease string
        self.assertEqual(well._format.Lease, 'OL-0001')
        
    def test_formatter_prod_month(self):        
        well = DataStructure()
        well.ProdMonth = 201602
        
        self.assertEqual(well._format.ProdMonth, '2016-02')

    def test_formatter_extract_date(self):
        monthly = DataStructure()
        monthly.ExtractDate = 20170507

        self.assertEqual(monthly._format.ExtractDate, '2017-05-07')

    def test_html_lf(self):
        well = DataStructure()
        well.Msg = 'abc;def;geh;'
        self.assertEqual('abc<br>def<br>geh<br>', well._format.html_lf(well.Msg))

        well.Msg = '$abc;$def;$geh;'
        self.assertEqual('\$abc<br>\$def<br>\$geh<br>', well._format.html_lf(well.Msg))

    def test_json(self):
        well = DataStructure(json_string='{"ID": 123, "LeaseType": "OL"}')
        self.assertEqual(123,well.ID)
        self.assertEqual('OL',well.LeaseType)
        self.assertEqual('{"ID": 123, "LeaseType": "OL"}', well.json_dumps())

    def test_list_str(self):
        # this silly method is just to get 100% coverage. Don't test this because the order sometimes changes.
        well = DataStructure(json_string='{"ID": 123, "LeaseType": "OL"}')
        s = str(well)
        s = well.headers()
        s = well.data()

    def test_diff(self):
        calc1 = DataStructure()
        self.assertEqual('', calc1.diff('SomeValue'))

        calc2 = DataStructure()
        calc2.original(calc1)
        self.assertRaises(AttributeError, calc2.diff, 'SomeValue')

        calc1.SomeValue = 123
        calc2.SomeValue = 123
        self.assertEqual('', calc1.diff('SomeValue'))

        calc2.SomeValue = 1234
        self.assertEqual('class="diff"', calc2.diff('SomeValue'))