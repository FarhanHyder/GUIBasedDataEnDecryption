'''
Author: Farhan Hyder, Andrew Truett
Last modified : 11/28/2017
'''

import random

'''
what it does: makes sure the shifted char_value is always within range [starting_index,ending_index]
pre-condition:
    >> parameters: int,int,int
post-condition:
    - it checks only for the conditions where char_value is out of range
    - if char_value is greater than ending_index
        -then adds the difference to the starting_index
    - if less than starting_index
        -subtracts the difference from the ending_index
    >> returns : int
helper method for : encryption()
'''
def shift_char_value_encrypt(char_value, starting_index, ending_index):
   if char_value > ending_index:
       diff = char_value - ending_index
       char_value = (starting_index - 1) + diff
   elif char_value < starting_index:
       diff = starting_index - char_value
       char_value = (ending_index + 1) - diff
   return char_value

'''
helper method for encryption()
'''
def random_number():
   return random.randint(-1, 25)

'''
helper method for encryption()
'''
def random_alpha_char():
   random_upper = random.randint(65, 90);
   random_lower = random.randint(97, 122);
   random_coin_flip = random.randint(0, 1);
   if random_coin_flip == 0:
       return chr(random_upper)
   else:
       return chr(random_lower)

'''
pre-condition:
    >> parameters: string, int, string(single char) 
post-condition:
    - does encryption for any upper and lower case alphabets
        - except: the special_char
    - if any character is shifted and it's new value is same as special_char
        - stores the index for later identification in the decryption process
    >> returns: string, list[int]
'''
def encryption(text, n, special_char):
   encrypted = ""

   collision_indices = []  # list of indices of characters that have been shifted to the special character
   index_counter = 0
   for symbol in text:
       if symbol.isalpha() and symbol != special_char:
           char_value = ord(symbol) + n  # getting the symbol char_value and adding the n value to it

           if symbol.isupper():
               char_value = shift_char_value_encrypt(char_value, 65, 90)    #uppercase utf-8 value range (A,Z)
           elif symbol.islower():
               char_value = shift_char_value_encrypt(char_value, 97, 122)   ##lowercase utf-8 value range (a,z)

           if (chr(char_value) == special_char):
               collision_indices.append(index_counter)  # storing index of the symbol that shifted to the special_char

           encrypted += chr(char_value)
       else:
           encrypted += symbol

       index_counter = index_counter + 1
   return encrypted, collision_indices


'''
what it does: makes sure the shifted char_value is always within range [starting_index,ending_index]
pre-condition:
    >> parameters: int,int,int
post-condition:
    - it checks only for the conditions where char_value is out of range
    - if char_value is less than starting_index
        - subtracts the difference from the ending_index
    - if greater than ending_index
        -then adds the difference to the starting_index
    
    >> returns : int
helper method for : decryption()
'''
def shift_index_decrypt(index, starting_index, ending_index):
   if index < starting_index:
       diff = starting_index - index
       index = (ending_index + 1) - diff
   elif index > ending_index:
       diff = index - ending_index
       index = (starting_index + 1) - diff
   return index

'''
pre-condition:
    >> parameters: string, int, string(single char), list[int]
post-condition:
    - does decryption for any upper and lower case alphabets
        - except: the special_char
    - from the collision_indices[] list it checks on which indices it
        has to perform shifting even if it is a special_char
    >> returns: string
'''
def decryption(encrypted_text, n, special_char, collision_indices):
   decrypted = ""

   counter = 0
   for symbol in encrypted_text:

       if symbol.isalpha():
           size = len(collision_indices)
           if size > 0 and symbol == special_char and counter == collision_indices[size - 1]:
               index = ord(symbol) - n

               if symbol.isupper():
                   index = shift_index_decrypt(index, 65, 90)
               elif symbol.islower():
                   index = shift_index_decrypt(index, 97, 122)
               decrypted += chr(index)

               collision_indices.pop()

           elif symbol != special_char:
               index = ord(symbol) - n

               if symbol.isupper():
                   index = shift_index_decrypt(index, 65, 90)
               elif symbol.islower():
                   index = shift_index_decrypt(index, 97, 122)
               decrypted += chr(index)

           else:
               decrypted += symbol         # if the symbol.isalpha is the special char
       else:
           decrypted += symbol     # if the symbol is anything but a alpha

       counter = counter + 1
   return decrypted








'''
returns >> string, string
helper method for menu()
'''
def open_file_as_r():
    #asks for user prompt
   input_file_name = input("Enter file name (without extension): ") + ".txt"
   text = ""
    #opening the file as readable only and stores the data in a string (text)
   with open(input_file_name, "r") as myfile:
       text = myfile.read()
   myfile.close()
   return input_file_name, text

'''
post-condition: converts a list to a string
    >> returns: string 
'''
def list_to_string(list):
   string = ""
   for item in list:
       string = str(item) + " " + string
   return string

'''
post-condition: converts a string to a list[of integers]
    >> returns: list[int]
'''
def string_to_numList(string):
   list = string.split()
   counter = 0
   for item in list:
       list[counter] = int(list[counter])
       counter = counter + 1

   return list



def menu():
   print("Enter your choice below."
         "\n\n"
         "[1] Encrypt a text file\n"
         "[2] Decrypt a text file\n"
         "[3] Exit application\n")
   user_input = int(input("Enter your choice: "))

   translated = ""
   if user_input == 1:
       # opening file and saving everything to a string
       print("|==File ENCRYPTION==|")
       input_file_name, text = open_file_as_r()
       # encryption process
       num = random_number()
       char = random_alpha_char()
       translated, collision_indices = encryption(text, num, char)
       # exporting the encrypted data to a text file
       encrypted_file = open("encrypted_" + input_file_name, "w")
       encrypted_file.write(translated)
       encrypted_file.close()
       # exporting the random number and random alphabet to a text file
       encrypted_file_key = open("key_" + input_file_name, "w")

       encrypted_file_key.write(str(num) + " \n" + char + "\n" + list_to_string(collision_indices))
       return True

   elif user_input == 2:
       # opening file and saving everything to a string
       print("|==File DECRYPTION==|")
       input_file_name, text = open_file_as_r()
       # opening the key file and saving the random num and random char to local var
       print("\nEnter key file name (without extension): ")
       key_file_name, key_file_str = open_file_as_r()
       num_str, char, list_str = key_file_str.splitlines()
       collision_indices = string_to_numList(list_str)
       num = int(num_str)
       # decrypting the data
       translated = decryption(text, num, char, collision_indices)
       # exporting the decrypted data to a text file
       decrypted_file = open("decrypted_" + input_file_name, "w")
       decrypted_file.write(translated)
       decrypted_file.close()
       return True
   elif user_input == 3:
       return False


print("Welcome to text encryption/decryption application.\n")
run = True
while (run):
   run = menu()


