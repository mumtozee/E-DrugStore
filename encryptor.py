import sys
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("action", type=str, help="encode, decode, train or hack")
parser.add_argument("--cipher", help="set the cipher type")
parser.add_argument("--key")
parser.add_argument("--input-file")
parser.add_argument("--text-file")
parser.add_argument("--output-file")
parser.add_argument("--model-file")
args = parser.parse_args()


def caesarize(input_string, key=0):
    output_string = ''
    for i in range(len(input_string)):
        tmp_ord = ord(input_string[i])
        if input_string[i].isupper():
            output_string += chr((tmp_ord + key - 65) % 26 + 65)
        elif input_string[i].islower():
            output_string += chr((tmp_ord + key - 97) % 26 + 97)
        else:
            output_string += input_string[i]
    return output_string


def vigenerize(input_string, keyword='', mode='encrypt'):
    output_string = ''
    key = keyword.upper()
    key_index = 0
    for char in input_string:
        if char.isupper():
            key_order = ord(key[key_index]) - 65
            char_order = ord(char) - 65
            if mode == 'encrypt':
                output_string += chr((char_order + key_order) % 26 + 65)
            else:
                output_string += chr((char_order - key_order) % 26 + 65)

            key_index += 1
        elif char.islower():
            key_order = ord(key[key_index].lower()) - 97
            char_order = ord(char) - 97
            if mode == 'encrypt':
                output_string += chr((char_order + key_order) % 26 + 97)
            else:
                output_string += chr((char_order - key_order) % 26 + 97)

            key_index += 1
        else:
            output_string += char

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
    letters = "abcdefghijklmnopqrstuvwxyz"
    num_of_letters = letter_count(input_string)
    result = {}
    buffer = input_string.lower()

    for letter in letters:
        if letter in buffer:
            result[letter] = round((buffer.count(letter) / num_of_letters) * 100, 2)
        else:
            result[letter] = 0

    return result


def train(input_string, output_file):
    with open(output_file, 'w') as file:
        file.write(json.dumps(stat_counter(input_string), indent=2))
    file.close()


def count_difference(stat_a, stat_b):
    letters = "abcdefghijklmnopqrstuvwxyz"
    answer = 0.
    for char in letters:
        answer += (stat_a[char] - stat_b[char]) ** 2
    return answer


def hack(input_string, stat_file):
    output_string = ''
    with open(stat_file, 'r') as file:
        default_freq = json.load(file)
        min_key, min_value = 1, 15000000
        for i in range(1, 26):
            temp_stat = stat_counter(caesarize(input_string, i))
            delta_stat = count_difference(default_freq, temp_stat)
            if delta_stat < min_value:
                min_key, min_value = i, delta_stat

        output_string = caesarize(input_string, min_key)

    file.close()
    return output_string


input_data = ''
output_data = ''

if args.input_file:
    with open(args.input_file, 'r') as in_file:
        input_data = in_file.read()
    in_file.close()
elif args.text_file:
    with open(args.text_file, 'r') as in_file:
        input_data = in_file.read()
    in_file.close()
else:
    input_data = sys.stdin.read()

if args.action == 'encode':
    if args.cipher == 'caesar':
        output_data = caesarize(input_data, int(args.key))
    elif args.cipher == 'vigenere':
        output_data = vigenerize(input_data, args.key, 'encrypt')
elif args.action == 'decode':
    if args.cipher == 'caesar':
        output_data = caesarize(input_data, -1 * int(args.key))
    elif args.cipher == 'vigenere':
        output_data = vigenerize(input_data, args.key, 'decrypt')
elif args.action == 'train':
    train(input_data, str(args.model_file))
elif args.action == 'hack':
    output_data = hack(input_data, str(args.model_file))

# after the whole process ends
if args.output_file:
    with open(args.output_file, 'w') as out_file:
        out_file.write(output_data)
    out_file.close()
else:
    print(output_data)
