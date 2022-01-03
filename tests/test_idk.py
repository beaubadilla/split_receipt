#!/usr/bin/python3
import unittest
import split_receipt

class TestIdk(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()
    def tearDown(self) -> None:
        return super().tearDown()

    def test_calculate_price_per_person_num__people(self):
        subtotal = 249.48
        num_ids = 12
        people = [
            split_receipt.Person('Alan'), # 0
            split_receipt.Person('April'), # 1
            split_receipt.Person('Brad'), # 2
            split_receipt.Person('Bryson'), # 3
            split_receipt.Person('Eric'), # 4
            split_receipt.Person('Jared+Priscilla'), # 5
            split_receipt.Person('Mikaela+Braxton'), # 6
            split_receipt.Person('Ryan+Kristin'), # 7
            split_receipt.Person('Thor'), # 8
        ]
        cppp = split_receipt.calculate_price_per_person
        self.assertEqual(cppp(subtotal, num_ids, people, 2), 20.79)
        self.assertEqual(cppp(subtotal, num_ids, people, 5), 41.58)

    def test_calculate_price_per_person__subtotal(self):
        num_ids = 12
        people = [
            split_receipt.Person('Alan'), # 0
            split_receipt.Person('April'), # 1
            split_receipt.Person('Brad'), # 2
            split_receipt.Person('Bryson'), # 3
            split_receipt.Person('Eric'), # 4
            split_receipt.Person('Jared+Priscilla'), # 5
            split_receipt.Person('Mikaela+Braxton'), # 6
            split_receipt.Person('Ryan+Kristin'), # 7
            split_receipt.Person('Thor'), # 8
        ]
        cppp = split_receipt.calculate_price_per_person
        self.assertEqual(cppp(0, num_ids, people, 0), 0)
        self.assertEqual(cppp(0, num_ids, people, 6), 0)
        self.assertEqual(cppp(300, num_ids, people, 0), 25.0)
        self.assertEqual(cppp(300, num_ids, people, 6), 50.0)
        self.assertEqual(cppp(300.0, num_ids, people, 0), 25.0)
        self.assertEqual(cppp(300.0, num_ids, people, 6), 50.0)
        with self.assertRaises(ValueError):
            cppp(-1, num_ids, people, 0)
        with self.assertRaises(ValueError):
            cppp(-1, num_ids, people, 6)
    
    def test_add_purchase(self):
        person1 = split_receipt.Person('Brad')
        ap = person1.add_purchase

        ap('kickin crab', 'garlic noodles', 12.99, 0.1025, 0.18)
        self.assertEqual(person1.purchases['kickin crab']['total'], 16.659675)
        ap('kickin crab', 'extra sauce', 2.50, 0.1025, 0.18) # 3.20625
        self.assertEqual(person1.purchases['kickin crab']['total'], 19.865925)

    def test_get_event_total(self):
        person1 = split_receipt.Person('Brad')
        person1.purchases = {
            'test_event1': {
                'total': 100
            },
            'test_event2': {
                'total': 100.0
            },
            'test_event3': {
                'total': 100.09
            },
            'test_event4': {
                'total': 100.091
            },
        }
        et = person1.get_event_total
        self.assertEqual(et('test_event1'), 100.00)
        self.assertEqual(et('test_event2'), 100.00)
        self.assertEqual(et('test_event3'), 100.09)
        self.assertEqual(et('test_event4'), 100.09)

    #test tip
    #test tax

if __name__ == '__main__':
    unittest.main()
