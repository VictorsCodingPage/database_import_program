import unittest
import imp

file_to_dict = imp.load_source('data_reading', '../scan_file_to_dict.py')
file_to_list = imp.load_source('data_reading', '../scan_file_to_list.py')

class Test_Data_Reading_Functions(unittest.TestCase):
    def test_scan_file_to_dict(self):
        expected = {'Dresses':1, 'Tops & Tees':2, 'Sweaters':3, 'Hoodies & Sweatshirts':4, 'Jeans':5,
                    'Pants':6, 'Skirts':7, 'Shorts':8, 'Leggings':9, 'Swimsuits & Cover Ups':10,
                    'Lingerie Sleep & Lounge':11, 'Jumpsuits Rompers & Overalls':12,
                    'Coats Jackets & Vests':13, 'Suiting & Blazers':14, 'Socks & Hosiery':15,
                    'Shoes':16, 'Jewelry':17, 'Watches':18, 'Bags & Wallets':19, 'Belts':20, 'Shirts':21,
                    'Hoodies & Sweatshirts':22, 'Sweaters':23, 'Jackets & Coats':24, 'Jeans':25, 'Pants':26,
                    'Shorts':27, 'Swim':28, 'Suits & Sport Coats':29, 'Underwear':30, 'Socks':31, 'Shoes':32,
                    'Jewelry':33, 'Watches':34, 'Accessories':35, 'Sunglasses':36, 'Belts':37, 'Sunglasses':38,
                    'Accessories':39, 'Woman':40, 'Man':41}
        actual_value = file_to_dict.scan_file_to_dict("../../HotCatToID.csv", 1, 0, ",")
        self.assertEqual(expected, actual_value)

    def test_scan_file_to_list(self):
        expected = ["asdpsdp", "pkdapsdkapsdk", "0930k0sf00fk0kfpkpdfk", "pkfk0k3kpfkpsf", "kpfk-3k0kd30kd", "dk0ck0dck"]
        actual_value = file_to_list.scan_file_to_list("../../test_file_list.txt", "\t")
        self.assertEqual(expected, actual_value)

if __name__ == '__main__':
    unittest.main()