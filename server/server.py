import flask
import lib
import json

app = flask.Flask("Phystech Pharmacy")

local_lab = lib.Laboratory()
drug_store = lib.DrugStore(local_lab)


@app.route('/order_lab', methods=['POST'])
def create_lab_order():
    drug_name = str(flask.request.args.get('name', 'validol'))
    drug_type = str(flask.request.args.get('type', 'pills'))
    drug_amount = int(flask.request.args.get('amount', 0))
    drug_price = local_lab.AVERAGE_COST_PER_DRUG

    tmp_drug = lib.Drug(drug_name, drug_type, drug_price, drug_amount)
    tmp_id = drug_store.lab.order_drug(tmp_drug)
    return str(tmp_id)


@app.route('/get_order_status', methods=['GET'])
def get_order_status():
    id_ = int(flask.request.args['id'])
    if id_ > drug_store.lab.last_id:
        return 'overflow'
    state = drug_store.lab.get_status(id_)
    return str(state)


@app.route('/ask_for', methods=['GET'])
def ask_for_drugs():
    drug_name = str(flask.request.args.get('name', ''))
    try:
        ans = json.dumps(drug_store.ask_for(drug_name))
    except ValueError:
        ans = 'no drug in local base'
    return ans


@app.route('/sell', methods=['POST'])
def sell_drugs():
    got_name = str(flask.request.args.get('name', ''))
    got_amount = int(flask.request.args.get('amount'))
    answer_text = ''

    if got_name in drug_store.items:
        tmp_data = drug_store.items[got_name]
        tmp_drug = lib.Drug(got_name, tmp_data['type'], tmp_data['price'], got_amount)

        try:
            drug_store.sell(tmp_drug)
            answer_text = 'ok'
        except OverflowError:
            answer_text = 'amount overflow'
    else:
        answer_text = 'unknown drug'

    return answer_text


@app.route('/get_drug_list', methods=['GET'])
def get_drug_list():
    drug_store.update_data()
    return json.dumps(drug_store.items)


def main():
    app.run("localhost", port=8080, debug=True)


if __name__ == "__main__":
    main()
