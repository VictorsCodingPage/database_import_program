from unittest.test.test_suite import *
import unittest
import imp
from psycopg2.extensions import *
import psycopg2
from database_create_statements import *
from database_sequence_creates import *


DTOs = imp.load_source('data_transfer_objects', './data_transfer_objects/data_transfer_objects.py')
data_sending = imp.load_source('data_sending_functions', './database_input_output/data_sending_functions/data_sending.py')

class Test_Data_Sending(unittest.TestCase):
    def setUp(self):
        self.dbconn = psycopg2.connect("host=localhost dbname=template1 user=postgres password=1234 port=5432")
        self.cursor = self.dbconn.cursor()
        self.dbconn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor.execute("CREATE DATABASE testing_grounds")
        self.dbconn.commit()
        self.dbconn.close()
        self.dbconn = psycopg2.connect("host=localhost dbname=testing_grounds user=postgres password=1234 port=5432")
        self.cursor = self.dbconn.cursor()
        self.cursor.execute(create_sequence("option_types") + create_sequence("option_value_variants") +
                            create_sequence("option_values") + create_sequence("product_categories") +
                            create_sequence("product_files") + create_sequence("product_option_types") +
                            create_sequence("products") + create_sequence("stores") +
                            create_sequence("variant_files") + create_sequence("variant_stores") +
                            create_sequence("variants"))
        self.cursor.execute(create_option_types + create_option_value_variants +
                            create_option_values + create_product_categories +
                            create_product_files + create_product_option_types +
                            create_products + create_stores + create_variant_files +
                            create_variant_stores + create_variants)
        self.dbconn.commit()

    def tearDown(self):
       self.dbconn.close()

    def test_store_insert(self):
        expected = "butterix"
        data_sending.insert_store(cursor, "butterix", ["bananabox", "lololGames", "TeeTees.com"], [True]*3)
        self.cursor.execute("select name from stores desc limit 1")
        actual_value = self.cursor.fetchone()[0]
        self.assertEqual(expected, actual_value)

    def test_product_insert(self):
        expected = None
        data_sending.export_data_to_database([DTOs.ProductDTO(DTOs.VariantDTO({"price":15.99, "updated_at":"2007-04-12"}), {"name":"Comica", "brand":"magazine",
                                                                          "updated_at":"2007-04-12"})], "91", cursor)
        self.cursor.execute("select * from products desc limit 1")
        actual_value = self.cursor.fetchone()[0]
        print actual_value
        self.assertEqual(expected, actual_value)








