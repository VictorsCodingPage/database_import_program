import psycopg2
import unittest
import imp

data_retrieval = imp.load_source('data_retrieval_functions', '../data_retrieval.py')

class Test_Data_Retrieval_Functions(unittest.TestCase):
    def setUp(self):
        connection_string = "host=localhost dbname=CJtestdb user=postgres password=1234 port=5432"
        self.dbconn = psycopg2.connect(connection_string)
        self.cursor = self.dbconn.cursor()

    def tearDown(self):
        self.dbconn.close()

    def test_get_store_name_list(self):
        expected = ['Antony Morato', 'Choies.com', 'DHGate', 'DL1961 Women', 'EricDress.com',
                    'FORZIERI Italia', 'ILoveScienceStore.com', 'JEGEM.com', 'Leonisa',
                    'melijoe.com', 'Monnier Fr\xc3\xa8res FR', 'Newegg.com',
                    'Boscov\'s Department Stores', 'Casadei', 'Chinese Laundry', 'Coco de Mer',
                    'Daniel Wellington', 'Bloomingdale\'s', 'Wal-Mart.com USA, LLC']
        actual_value = data_retrieval.get_store_name_list(self.cursor)
        self.assertEqual(expected, actual_value)

    def test_get_store_id_from_stores(self):
        expected = 508
        actual_value = data_retrieval.get_store_id_from_stores("JEGEM.com", self.cursor)
        self.assertEqual(expected, actual_value)

    def test_get_store_id_list(self):
        expected = [501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511,
                    512, 513, 514, 515, 516, 517, 521, 522]
        actual_value = data_retrieval.get_store_id_list(self.cursor)
        self.assertEqual(expected, actual_value)

    def test_get_product_id_from_products(self):
        expected = 23171767
        actual_value = data_retrieval.get_product_id_from_products("40494896",
                                                                   self.cursor)
        self.assertEqual(expected, actual_value)

    def test_get_variant_id_from_variants(self):
        expected_value = 22770722
        actual_value = data_retrieval.get_variant_id_from_variants("22256726",
                                                                   self.cursor)
        self.assertEqual(expected_value, actual_value)

if __name__ == '__main__':
    unittest.main()