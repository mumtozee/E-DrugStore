import sys
import argparse
import json
from string import ascii_uppercase, ascii_lowercase


def caesarize(input_string, key=0):
    mod = len(ascii_lowercase)
    symbol_list = []
    for letter in input_string:
        alphabet = ''
        if letter.isupper():
            alphabet = ''.join(ascii_uppercase)
        elif letter.islower():
            alphabet = ''.join(ascii_lowercase)

        if alphabet != '':
            tmp_ord = alphabet.index(letter)
            letter_to_add = alphabet[(tmp_ord + key) % mod]
        else:
            letter_to_add = letter

        symbol_list.append(letter_to_add)

    output_string = ''.join(symbol_list)
    return output_string


def vigenerize(input_string, keyword='', method='encode'):
    symbol_list = []
    key = keyword.upper()
    key_index = 0
    mod = len(ascii_lowercase)

    base = 1
    if method == 'decode':
        base = -1

    key_symbol = ''

    for char in input_string:
        alphabet = ''
        if char.isupper():
            alphabet = ''.join(ascii_uppercase)
            key_symbol = key[key_index].upper()
        elif char.islower():
            alphabet = ''.join(ascii_lowercase)
            key_symbol = key[key_index].lower()

        if alphabet != '':
            key_order = alphabet.index(key_symbol)
            char_order = alphabet.index(char)
            letter_to_add = alphabet[(char_order + base * key_order) % mod]
            key_index += 1
        else:
            letter_to_add = char

        if key_index == len(key):
            key_index = 0

        symbol_list.append(letter_to_add)

    output_string = ''.join(symbol_list)
    return output_string


def criptify(arguments, mode='encrypt'):
    output_data = ''
    if arguments.input_file:
        with open(arguments.input_file, 'r') as in_file:
            input_data = in_file.read()
    else:
        input_data = sys.stdin.read()

    if arguments.cipher == 'caesar':
        if mode == 'encrypt':
            output_data = caesarize(input_data, int(arguments.key))
        else:
            output_data = caesarize(input_data, -int(arguments.key))
    elif arguments.cipher == 'vigenere':
        if mode == 'encrypt':
            output_data = vigenerize(input_data, arguments.key, 'encode')
        else:
            output_data = vigenerize(input_data, arguments.key, 'decode')

    if arguments.output_file:
        with open(arguments.output_file, 'w') as out_file:
            out_file.write(output_data)
    else:
        print(output_data)


def encode(arguments):
    criptify(arguments, 'encrypt')


def decode(arguments):
    criptify(arguments, 'decrypt')


def letter_count(input_string):
    result = 0
    for x in input_string:
        if x.isalpha():
            result += 1
    return result


def stat_counter(input_string):
    num_of_letters = letter_count(input_string)
    result = {}
    buffer = input_string.lower()

    for letter in ascii_lowercase:
        if letter in buffer:
            result[letter] = buffer.count(letter) / num_of_letters

    return result


def train(arguments):
    if arguments.text_file:
        with open(arguments.text_file, 'r') as in_file:
            input_string = in_file.read()
    else:
        input_string = sys.stdin.read()

    with open(arguments.model_file, 'w') as file:
        file.write(json.dumps(stat_counter(input_string), indent=2))


def count_difference(stat_a, stat_b):
    answer = 0.
    for char in ascii_lowercase:
        if char in stat_a and char in stat_b:
            answer += (stat_a[char] - stat_b[char]) ** 2
        elif char in stat_a:
            answer += stat_a[char] ** 2
        elif char in stat_b:
            answer += stat_b[char] ** 2

    return answer


def shift_dict_keys(old_stat):
    new_stat = {}
    for dict_key in old_stat:
        new_stat[caesarize(dict_key, 1)] = old_stat[dict_key]

    return new_stat


def hack(arguments):
    if arguments.input_file:
        with open(arguments.input_file, 'r') as in_file:
            input_string = in_file.read()
    else:
        input_string = sys.stdin.read()

    with open(arguments.model_file, 'r') as file:
        default_freq = json.load(file)
        iteration_time = len(ascii_lowercase) + 1
        min_key = 1
        temp_stat = stat_counter(caesarize(input_string, 1))
        min_value = count_difference(default_freq, temp_stat)

        for i in range(2, iteration_time):
            temp_stat = shift_dict_keys(temp_stat)
            delta_stat = count_difference(default_freq, temp_stat)
            if delta_stat < min_value:
                min_key = i
                min_value = delta_stat

        output_string = caesarize(input_string, min_key)

    if arguments.output_file:
        with open(arguments.output_file, 'w') as out_file:
            out_file.write(output_string)
    else:
        print(output_string)


parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers()
# encoding command
encode_parser = subparsers.add_parser('encode')
encode_parser.set_defaults(mode='encode', func=encode)
encode_parser.add_argument("--cipher")
encode_parser.add_argument("--key")
encode_parser.add_argument("--input-file")
encode_parser.add_argument("--output-file")

# decoding command
decode_parser = subparsers.add_parser('decode')
decode_parser.set_defaults(mode='decode', func=decode)
decode_parser.add_argument("--cipher")
decode_parser.add_argument("--key")
decode_parser.add_argument("--input-file")
decode_parser.add_argument("--output-file")

# training command
train_parser = subparsers.add_parser('train')
train_parser.set_defaults(mode='train', func=train)
train_parser.add_argument('--text-file')
train_parser.add_argument('--model-file')

# hacking command
hack_parser = subparsers.add_parser('hack')
hack_parser.set_defaults(mode='hack', func=hack)
hack_parser.add_argument('--input-file')
hack_parser.add_argument('--output-file')
hack_parser.add_argument('--model-file')

args = parser.parse_args()

if __name__ == "__main__":
    args.func(args)
