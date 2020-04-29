import sys
import argparse
import json
from string import ascii_uppercase, ascii_lowercase


def caesarize(input_string, key=0):
    mod = len(ascii_lowercase)
    output_string = ''
    for letter in input_string:
        tmp_ord = 0
        letter_to_add = ''
        if letter.isupper():
            tmp_ord = ascii_uppercase.index(letter)
            letter_to_add = ascii_uppercase[(tmp_ord + key) % mod]
        elif letter.islower():
            tmp_ord = ascii_lowercase.index(letter)
            letter_to_add = ascii_lowercase[(tmp_ord + key) % mod]
        else:
            letter_to_add = letter

        output_string += letter_to_add
    return output_string


def encode(arguments):
    output_data = ''
    if arguments.input_file:
        with open(arguments.input_file, 'r') as in_file:
            input_data = in_file.read()
        in_file.close()
    else:
        input_data = sys.stdin.read()

    if arguments.cipher == 'caesar':
        output_data = caesarize(input_data, int(arguments.key))
    elif arguments.cipher == 'vigenere':
        output_data = vigenerize(input_data, arguments.key, 'encrypt')

    if arguments.output_file:
        with open(arguments.output_file, 'w') as out_file:
            out_file.write(output_data)
        out_file.close()
    else:
        print(output_data)


def decode(arguments):
    output_data = ''
    if arguments.input_file:
        with open(arguments.input_file, 'r') as in_file:
            input_data = in_file.read()
        in_file.close()
    else:
        input_data = sys.stdin.read()

    if arguments.cipher == 'caesar':
        output_data = caesarize(input_data, -1 * int(arguments.key))
    elif arguments.cipher == 'vigenere':
        output_data = vigenerize(input_data, arguments.key, 'decrypt')

    if arguments.output_file:
        with open(arguments.output_file, 'w') as out_file:
            out_file.write(output_data)
        out_file.close()
    else:
        print(output_data)


def vigenerize(input_string, keyword='', mode='encrypt'):
    output_string = ''
    key = keyword.upper()
    key_index = 0
    mod = len(ascii_lowercase)

    base = 1
    if mode == 'decrypt':
        base = -1

    for char in input_string:
        if char.isupper():
            key_order = ascii_uppercase.index(key[key_index])
            char_order = ascii_uppercase.index(char)
            letter_to_add = ascii_uppercase[(char_order + base * key_order) % mod]
            key_index += 1
        elif char.islower():
            key_order = ascii_lowercase.index(key[key_index].lower())
            char_order = ascii_lowercase.index(char)
            letter_to_add = ascii_lowercase[(char_order + base * key_order) % mod]
            key_index += 1
        else:
            letter_to_add = char

        output_string += letter_to_add

        if key_index == len(key):
            key_index = 0

    return output_string


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
            result[letter] = round((buffer.count(letter) / num_of_letters) * 100, 2)
        else:
            result[letter] = 0

    return result


def train(arguments):
    if arguments.text_file:
        with open(arguments.text_file, 'r') as in_file:
            input_string = in_file.read()
        in_file.close()
    else:
        input_string = sys.stdin.read()

    with open(arguments.model_file, 'w') as file:
        file.write(json.dumps(stat_counter(input_string), indent=2))
    file.close()


def count_difference(stat_a, stat_b):
    answer = 0.
    for char in ascii_lowercase:
        answer += (stat_a[char] - stat_b[char]) ** 2
    return answer


def hack(arguments):
    if arguments.input_file:
        with open(arguments.input_file, 'r') as in_file:
            input_string = in_file.read()
        in_file.close()
    else:
        input_string = sys.stdin.read()

    with open(arguments.model_file, 'r') as file:
        default_freq = json.load(file)
        min_key = 1
        min_value = 15000000
        for i in range(1, 27):
            temp_stat = stat_counter(caesarize(input_string, i))
            delta_stat = count_difference(default_freq, temp_stat)
            if delta_stat < min_value:
                min_key = i
                min_value = delta_stat

        output_string = caesarize(input_string, min_key)

    file.close()

    if arguments.output_file:
        with open(arguments.output_file, 'w') as out_file:
            out_file.write(output_string)
        out_file.close()
    else:
        print(output_string)


if __name__ == '__main__':
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
    args.func(args)
