import requests
import argparse
import json


def create_main_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', default=8000, type=int)

    return parser


def ask_drugs(args):
    drug_name = input("Enter the name of the drug, you want: ")

    result = requests.get(f'http://{args.host}:{args.port}/ask_for', params=dict(
        name=drug_name
    )).text

    if result == 'no drug in local base':
        print("It seems, we don't have this drug currently.")
        print("Try to make an order in our lab. Type help for the command list :)")
    else:
        got_drug_data = dict(json.loads(result))
        print(f"Type: {got_drug_data['type']}")
        print(f"Price: ${got_drug_data['price']}")
        print(f"Amount: {got_drug_data['amount']}")


def make_order(args):
    drug_name = input("Enter the drug name: ")
    drug_type = input("Enter the drug type: ")
    drug_amount = input("Enter the amount of drug: ")

    order_id = requests.post(f'http://{args.host}:{args.port}/order_lab', params=dict(
        name=drug_name,
        type=drug_type,
        amount=drug_amount
    )).text

    print(f"ID of your order in out lab is: {order_id}")


def get_status(args):
    id_ = input('Enter ID of the order: ')
    stats = requests.get(f'http://{args.host}:{args.port}/get_order_status', params=dict(
        id=id_
    )).text

    if stats == 'in process':
        print("Your order is being prepared in the lab!")
    elif stats == 'finished':
        print("Your order is ready. Soon it will be yours :)")
    elif stats == 'overflow':
        print("We don't have this order in lab")


def buy_drugs(args):
    drug_name = input("Enter drug name: ")
    drug_amount = input("Enter amount of your purchase: ")

    result = requests.post(f'http://{args.host}:{args.port}/sell', params=dict(
        name=drug_name,
        amount=drug_amount
    )).text

    if result == 'amount overflow':
        print("Sorry, it seems we don't have that amount of drugs :(")
    elif result == 'unknown drug':
        print("Seems we don't have this drug currently")
        print("Try to order it in our lab. Type 'help' for the list of commands")
    elif result == 'ok':
        card_num = input("Enter your card number (XXXX-XXXX-XXXX-XXXX): ")
        if len(card_num) == 19:
            print("Payment was executed successfully!")
        else:
            print("Sorry, something went wrong. Try again")


def print_list(args):
    items_raw = requests.get(f'http://{args.host}:{args.port}/get_drug_list').text
    items = dict(json.loads(items_raw))

    print("Name\t\tType\t\tPrice\t\tAmount")
    for name in items:
        amount_ = items[name]['amount']
        type_ = items[name]['type']
        price_ = items[name]['price']
        print(f"{name}\t\t{type_}\t{price_}\t{amount_}")


def exit_function():
    choice = input("Are your sure, you want to exit? (y/n) ")

    if choice == 'y':
        print("Good bye! Take care of yourself! ^^")
        exit()
    elif choice == 'n':
        print('ok then, let\'s carry on')
    else:
        print('invalid input, please try again')


def print_help():
    COMMAND_LIST = ['ask-drugs', 'order', 'get-status', 'buy', 'print-list', 'exit', ]
    print("We have these commands: ")

    for cmd in COMMAND_LIST:
        print(cmd)


def main():
    main_parser = create_main_parser()
    program_args = main_parser.parse_args()

    while True:
        try:
            command = input('$ ')

            if command == 'ask-drugs':
                ask_drugs(program_args)
            elif command == 'order':
                make_order(program_args)
            elif command == 'get-status':
                get_status(program_args)
            elif command == 'buy':
                buy_drugs(program_args)
            elif command == 'print-list':
                print_list(program_args)
            elif command == 'help':
                print_help()
            elif command == "exit":
                exit_function()
        except KeyboardInterrupt:
            exit_function()


if __name__ == "__main__":
    main()
