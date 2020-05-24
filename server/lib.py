import json


class Drug:
    def __init__(self, name_, type_, price_=0, amount_=0):
        self.name = name_
        self.type = type_
        self.price = price_
        self.amount = amount_


class LabOrder:
    def __init__(self, id_, drug_):
        self.drug = drug_
        self.id = id_
        self.status = 'in process'


class Laboratory:
    AVERAGE_COST_PER_DRUG = 12

    def __init__(self):
        self.orders = {}
        self.last_id = 0

    def order_drug(self, drug_):
        self.last_id += 1
        new_id_ = self.last_id
        self.orders[new_id_] = LabOrder(new_id_, drug_)
        return new_id_

    def get_status(self, id_):
        return self.orders[id_].status

    def finish_preparation(self, id_):
        self.orders[id_].status = 'finished'

    def receive_ready_drug(self, id_):
        ready_drug = self.orders[id_].drug
        if self.orders[id_].status == 'finished':
            del self.orders[id_]
            return ready_drug
        else:
            raise ValueError


class DrugStore:
    def __init__(self, lab_=Laboratory, balance_=0):
        with open('data.json', 'r') as drugs_file:
            self.items = json.load(drugs_file)
        self.lab = lab_
        self.balance = balance_

    def ask_for(self, name):
        if name in self.items:
            return self.items[name]
        else:
            raise ValueError

    def sell(self, drug_):
        tmp_item_key = self.items[drug_.name]
        if tmp_item_key["amount"] >= drug_.amount:
            tmp_item_key["amount"] -= drug_.amount
            self.balance += drug_.amount * drug_.price
        else:
            raise ValueError

    def update_data(self):
        with open('data.json', 'w') as file:
            file.write(json.dumps(self.items, indent=2))

        with open('data.json', 'r') as file:
            self.items = json.load(file)
