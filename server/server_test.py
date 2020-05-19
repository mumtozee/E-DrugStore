import lib
import unittest

lab = lib.Laboratory()
pharm = lib.DrugStore(lab)
test_drug = lib.Drug('aspirin', 'pills', 20, 300)


class MainClassTest(unittest.TestCase):
    def test_object_type(self):
        global lab
        global pharm
        global test_drug
        self.assertIsInstance(lab, lib.Laboratory)
        self.assertIsInstance(pharm, lib.DrugStore)
        self.assertIsInstance(test_drug, lib.Drug)


class OrderTest(unittest.TestCase):
    def test_order(self):
        global lab
        global test_drug
        temp_id = lab.last_id
        new_id = lab.order_drug(test_drug)
        self.assertEqual(new_id, temp_id + 1)
        self.assertEqual(test_drug, lab.orders[new_id].drug)


class OrderFinishTest(unittest.TestCase):
    def test_order_finish(self):
        global lab
        test_drug_2 = lib.Drug('analgin', 'pills', 45, 230)
        new_id = lab.order_drug(test_drug_2)
        lab.finish_preparation(new_id)
        self.assertEqual(lab.orders[new_id].status, 'finished')


class OrderStatusTest(unittest.TestCase):
    def test_order_status(self):
        global lab
        test_drug_3 = lib.Drug('espumizan', 'pills', 11, 230)
        new_id = lab.order_drug(test_drug_3)
        self.assertEqual(lab.orders[new_id].status, lab.get_status(new_id))


class OrderReceiveTest(unittest.TestCase):
    def test_order_receive(self):
        global lab
        test_drug_1 = lib.Drug('analgin', 'pills', 45, 230)
        test_drug_2 = lib.Drug('espumizan', 'pills', 11, 230)
        id_1 = lab.order_drug(test_drug_1)
        id_2 = lab.order_drug(test_drug_2)
        pharm.lab.finish_preparation(id_2)
        self.assertEqual(lab.orders[id_2].drug, lab.receive_ready_drug(id_2))
        with self.assertRaises(ValueError):
            lab.receive_ready_drug(id_1)


class AskDrugsTest(unittest.TestCase):
    def test_store_ask(self):
        global pharm
        self.assertEqual(pharm.items['aspirin'], pharm.ask_for('aspirin'))
        with self.assertRaises(ValueError):
            pharm.ask_for('validol')


class SellDrugsTest(unittest.TestCase):
    def test_sell(self):
        global pharm
        test_drug_4 = lib.Drug('aspirin', 'pills', 25, 2)
        tmp_balance = pharm.balance
        tmp_amount = pharm.items[test_drug_4.name]["amount"]
        pharm.sell(test_drug_4)
        self.assertEqual(tmp_balance + 25 * 2, pharm.balance)
        self.assertEqual(tmp_amount - 2, pharm.items[test_drug_4.name]['amount'])
        test_drug_4.amount = 2000
        with self.assertRaises(ValueError):
            pharm.sell(test_drug_4)


if __name__ == "__main__":
    unittest.main()
