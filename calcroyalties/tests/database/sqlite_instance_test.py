#!/bin/env python3
"""
This tests all the primary features in the sqlite_insance. It is written as one
big method which is generally not a good idea but in this case it seemed like
the best way to test it.
"""
import unittest

import config
from tests.database.sqlite_utilities_test import DatabaseUtilities

class TestSqliteInstance(unittest.TestCase):


    TEST_TABLE_NAME = 'mytable'
    
    def setUp(self):
        self.assertEqual(config.get_environment(),'unittest') # Distructive Tests must run in unittest enviornment
        db_utils = DatabaseUtilities()
        db_utils.delete_all_tables()

        instance = config.get_database_instance()
        instance.execute('create table ' + self.TEST_TABLE_NAME  + ' (myKey int, myText text, myDate date)')
        instance.commit()
        
        instance.execute('insert into ' + self.TEST_TABLE_NAME + " values (1, 'Test Item One', '2016-02-14')")
        instance.execute('insert into ' + self.TEST_TABLE_NAME + " values (2, 'Test Item Two', '2016-02-14')")
        instance.commit()

    def test_all_features(self):
        instance = config.get_database_instance()

        self.assertIn(self.TEST_TABLE_NAME, instance.get_table_names(), 'Should have created table: ' + self.TEST_TABLE_NAME)

        selectStmt = 'select * from ' + self.TEST_TABLE_NAME + ' order by myKey'
        values = instance.execute(selectStmt)

        rows = []
        for row in values:
            rows.append(row)

        self.assertEqual(2,len(rows), 'Should be two rows in the table')
        self.assertEqual(1,rows[0][0], 'First key should be 1')
        self.assertEqual(2,rows[1][0], 'First key should be 1')
        
    def test_get_column_name(self):
        instance = config.get_database_instance()
        db_utils = DatabaseUtilities()
        db_utils.delete_all_tables()

        instance.execute('create table ' + self.TEST_TABLE_NAME  + ' (myKey int, myText text, myDate date)')
        instance.execute('insert into ' + self.TEST_TABLE_NAME + " values (1, 'Test Item One', '2016-02-14')")
        
        instance.execute('select * from ' + self.TEST_TABLE_NAME)
        
        columns = instance.get_column_names()
        self.assertEqual(columns[0],'myKey')
        self.assertEqual(columns[1],'myText')
        self.assertEqual(columns[2],'myDate')
        
