import requests
import argparse
import json


def address(args):
    return f'http://{args.host}:{args.port}'


def handle_error(response):
    print(response["error_message"])
    exit_function(response)


def create_main_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', default=8000, type=int)

    return parser


def ask_drugs(args, response):
    drug_name = input(response["ask_drug_name"])

    try:
        result = requests.get(f'{address(args)}/ask_for', params=dict(
            name=drug_name
        )).text

        if result == 'no drug in local base':
            print(response["no_drug_local"])
        else:
            got_drug_data = dict(json.loads(result))
            print(f"Type: {got_drug_data['type']}")
            print(f"Price: ${got_drug_data['price']}")
            print(f"Amount: {got_drug_data['amount']}")
    except requests.exceptions.ConnectionError:
        handle_error(response)


def make_order(args, response):
    drug_name = input(response["ask_drug_name"])
    drug_type = input(response["ask_type"])
    drug_amount = input(response["ask_amount"])

    try:
        order_id = requests.post(f'{address(args)}/order_lab', params=dict(
            name=drug_name,
            type=drug_type,
            amount=drug_amount
        )).text

        print(f'{response["say_ID"]}{order_id}')
    except requests.exceptions.ConnectionError:
        handle_error(response)


def get_status(args, response):
    id_ = input(response["ask_ID"])
    try:
        stats = requests.get(f'{address(args)}/get_order_status', params=dict(
            id=id_
        )).text

        if stats == 'in process':
            print(response["status_in_process"])
        elif stats == 'finished':
            print(response["status_finished"])
        elif stats == 'overflow':
            print(response["status_overflow"])
    except requests.exceptions.ConnectionError:
        handle_error(response)


def buy_drugs(args, response):
    drug_name = input(response["ask_drug_name"])
    drug_amount = input(response["ask_amount"])

    try:
        result = requests.post(f'{address(args)}/sell', params=dict(
            name=drug_name,
            amount=drug_amount
        )).text

        if result == 'amount overflow':
            print(response["buy_amount_overflow"])
        elif result == 'unknown drug':
            print(response["buy_unknown_drug"])
        elif result == 'ok':
            card_num = input(response["ask_card_num"])
            if len(card_num) == 19:
                print(response["buy_payment_success"])
            else:
                print(response["buy_payment_error"])
    except requests.exceptions.ConnectionError:
        handle_error(response)


def print_list(args, response):
    try:
        items_raw = requests.get(f'{address(args)}/get_drug_list').text
        items = dict(json.loads(items_raw))

        print("Name\t\tType\t\tPrice\t\tAmount")
        for name in items:
            amount_ = items[name]['amount']
            type_ = items[name]['type']
            price_ = items[name]['price']
            print(f"{name}\t\t{type_}\t\t{price_}\t\t{amount_}")
    except requests.exceptions.ConnectionError:
        handle_error(response)


def exit_function(response):
    choice = input(response["ask_exit"])

    if choice == 'y':
        print(response["exit_yes"])
        exit()
    elif choice == 'n':
        print(response["exit_no"])
    else:
        print(response["invalid_input"])


def print_help(commands, response):
    print(response["our_commands"])

    for cmd in commands:
        print(f"{cmd} - {commands[cmd]}")


def main():
    main_parser = create_main_parser()
    program_args = main_parser.parse_args()

    with open('config.json', 'r') as conf_file:
        configs = json.load(conf_file)
        text_response = configs["text_responses"]
        while True:
            try:
                command = input('$ ')

                if command == 'ask-drugs':
                    ask_drugs(program_args, text_response)
                elif command == 'order':
                    make_order(program_args, text_response)
                elif command == 'get-status':
                    get_status(program_args, text_response)
                elif command == 'buy':
                    buy_drugs(program_args, text_response)
                elif command == 'print-list':
                    print_list(program_args, text_response)
                elif command == 'help':
                    print_help(configs["commands"], text_response)
                elif command == "exit":
                    exit_function(text_response)
                else:
                    print(text_response["unknown_cmd"])
            except KeyboardInterrupt:
                exit_function(text_response)


if __name__ == "__main__":
    main()
