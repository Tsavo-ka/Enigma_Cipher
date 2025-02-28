import string

LETTERS = string.ascii_uppercase

'''
Rotor numbers, configurations, and notches for:
(1) Service Enigma rotors
(2) Enigma K rotors
(3) Railway Enigma rotors
'''
ROTORS_DICT = {
    1:{
        1:('EKMFLGDQVZNTOWYHXUSPAIBRCJ','Q'), 
        2:('AJDKSIRUXBLHWTMCQGZNPYFVOE','E'), 
        3:('BDFHJLCPRTXVZNYEIWGAKMUSQO','V'), 
        4:('ESOVPZJAYQUIRHXLNFTGKDCMWB','J'), 
        5:('VZBRGITYUPSDNHLXAWMJQOFECK','Z')
    },
    2:{
        1:('LPGSZMHAEOQKVXRFYBUTNICJDW','Y'), 
        2:('SLVGBTFXJQOHEWIRZYAMKPCNDU','E'), 
        3:('CJGDPSHKTURAWZXFMYNQOBVLIE','N')
    },
    3:{
        1:('JGDQOXUSCAMIFRVTPNEWKBLZYH','N'), 
        2:('NTZPSFBOKMWRCJDIVLAEYUXHGQ','E'), 
        3:('JVIUBHTCDYAKEQZPOSGXNRMWFL','Y')
    }
}

'''
Reflector numbers, configurations, and names for:
(1) Service Enigma reflectors
(2) Enigma K Reflectors
(3) Railway Enigma Reflectors
'''
REFLECTORS_DICT = {
    1: {
        1:('EJMZALYXVBWFCRQUONTSPIKHGD','UKW-A'), 
        2:('YRUHQSLDPXNGOKMIEBFZCWVJAT','UKW-B'), 
        3:('FVPJIAOYEDRZXWGCTKUQSBNMHL','UKW-C')
    },
    2: {
        1:('IMETCGFRAYSQBZXWLHKDVUPOJN','UKW'), 
        2:('QWERTZUIOASDFGHJKPYXCVBNML','ETW')
    },
    3: {1:('QYHOGNECVPUZTFDJAXWMKISRBL','UKW'), 
        2:('QWERTZUIOASDFGHJKPYXCVBNML','ETW')
       }
}


#Names, number of rotors, number of reflectors, and reflector names for various enigma types
MACHINE_TYPES = {
    1:("Service Enigma (Enigma I)", 5, 3, 
       {
        1:'UKW-A', 
        2:'UKW-B', 
        3:'UKW-C'
    }
      ), 
    2:("Enigma K", 3, 2, 
       {
        1:'UKW',
        2:'ETW'
    }
      ), 
    3:("Railway Enigma", 3, 2, 
       {
        1:'UKW',
        2:'ETW'
    }
      )
}

class Rotor:

    def __init__(self, name, setting, notch, offset, position):
        self.name = name
        self.setting = setting
        self.notch = notch
        self.offset = offset
        self.position= position

    def __str__(self):
        return f'\nRotor name {self.name}\nSetting {self.setting}\nNotch'

    def encrypt(self, letter):
        letter = (LETTERS.index(letter) + self.position - self.offset) % 26
        new_letter = self.setting[letter]
        exit_letter = LETTERS[(LETTERS.index(new_letter) - self.position + self.offset) % 26]
        return exit_letter

    def reverse_encrypt(self, letter):
        letter = LETTERS[(LETTERS.index(letter) + self.position - self.offset) % 26]
        new_letter = LETTERS[self.setting.index(letter)]
        exit_letter = LETTERS[(LETTERS.index(new_letter) - self.position + self.offset) % 26]
        return exit_letter

    def rotate(self):
        self.position = (self.position + 1) % 26

class Reflector:

    def __init__(self, name, setting):
        self.name = name
        self.setting = setting

    def __str__(self):
        return f'\nReflector {self.name}\nSetting {self.setting}'

    def encrypt(self, letter):
        return self.setting[LETTERS.index(letter)]

class Enigma:

    def __init__(self, name, rotor_1, rotor_2, rotor_3, reflector, plugboard=None):
        self.name = name
        self.rotor_1 = rotor_1
        self.rotor_2 = rotor_2
        self.rotor_3 = rotor_3
        self.reflector = reflector
        self.plugboard = plugboard if plugboard else {}

    def step(self):

        if self.rotor_2.notch == LETTERS[self.rotor_2.position]:
            self.rotor_1.rotate()
            self.rotor_2.rotate()
            self.rotor_3.rotate()
        elif self.rotor_3.notch == LETTERS[self.rotor_3.position]:
            self.rotor_2.rotate()
            self.rotor_3.rotate()
        else:
            self.rotor_3.rotate()

    def encryption(self, letter):

        self.step()
        print (f'{self.rotor_1.position}, {self.rotor_2.position}, {self.rotor_3.position}')
        
        if letter in self.plugboard:
            letter = self.plugboard[letter]

        change_1 = self.rotor_3.encrypt(letter)
        change_2 = self.rotor_2.encrypt(change_1)
        change_3 = self.rotor_1.encrypt(change_2)
        change_4 = self.reflector.encrypt(change_3)
        change_5 = self.rotor_1.reverse_encrypt(change_4)
        change_6 = self.rotor_2.reverse_encrypt(change_5)
        change_7 = self.rotor_3.reverse_encrypt(change_6)
        
        if change_7 in self.plugboard:
            change_7 = self.plugboard[change_7]

        return change_7

def get_user_input(prompt, valid_values):
    while True:
        answer = input(prompt)
        if answer in valid_values:
            return answer
        else:
            print("Invalid input. Please try again.")

def setup_enigma():
    
    enigma_type = int(get_user_input("Choose your enigma type (1: Service Enigma, 2: Enigma K, 3: Railway Enigma): ", ['1','2','3']))
    
    rotors = [x for x in range(1, MACHINE_TYPES[enigma_type][1]+1)]
    reflectors = [f"{k}: {v}" for k,v in MACHINE_TYPES[enigma_type][3].items()]
    used_rotors = []
    used_reflectors = []
    
    for i in range(3):
        rotor_pick = int(get_user_input(f"Choose rotor {i+1} - ({', '.join(str(x) for x in rotors)}): ", [str(x) for x in rotors]))
        used_rotors.append(rotors.pop(rotors.index(rotor_pick)))
                         
    reflector_pick = int(get_user_input(f"Choose reflector - ({', '.join(reflectors)}): ", [str(x+1) for x in range(len(reflectors))]))
    
    def offset_rotor(rotor_number):
        offset = get_user_input(f'Choose a ring setting for rotor {rotor_number} (A-Z): ', LETTERS+LETTERS.lower())
        offset = LETTERS.index(offset[0].upper())
        print(f"Offset: {offset}")
        return offset
    
    def rotor_start_position(rotor_number):
        start_position = get_user_input(f'Choose a start position for rotor {rotor_number} (A-Z): ', LETTERS+LETTERS.lower())
        start_position = LETTERS.index(start_position[0].upper())
        print(f"Start position: {start_position}")
        return start_position
    
    def setup_plugboard():
        sockets = {}
        open_sockets = list(LETTERS)
        plugs =  int(get_user_input("Choose number of plugs for plugboard (0-13): ", [str(x) for x in range(14)]))
        if not plugs:
            return None
        for i in range(plugs):
            socket_1 = get_user_input(f"Choose 1st socket for plug {i+1} ({open_sockets}): ", ''.join(open_sockets)+''.join(open_sockets).lower()).upper()
            open_sockets.pop(open_sockets.index(socket_1))
            socket_2 = get_user_input(f"Choose 2nd socket for plug {i+1} ({open_sockets}): ", ''.join(open_sockets)+''.join(open_sockets).lower()).upper()
            open_sockets.pop(open_sockets.index(socket_2))
            sockets[socket_1] = socket_2
            sockets[socket_2] = socket_1
            
        return sockets
        
    plugboard = setup_plugboard()
    offset_1, offset_2, offset_3 = offset_rotor(1), offset_rotor(2), offset_rotor(3)
    position_1, position_2, position_3 = rotor_start_position(1), rotor_start_position(2), rotor_start_position(3)

    return enigma_type, used_rotors, reflector_pick, offset_1, offset_2, offset_3, position_1, position_2, position_3, plugboard

def build(enigma_type, used_rotors, reflector_pick, offset_1, offset_2, offset_3, position_1, position_2, position_3, plugboard):
        
    rotor_1 = Rotor("Rotor 1", ROTORS_DICT[enigma_type][used_rotors[0]][0], ROTORS_DICT[enigma_type][used_rotors[0]][1], offset_1, position_1)
    rotor_2 = Rotor("Rotor 2", ROTORS_DICT[enigma_type][used_rotors[1]][0], ROTORS_DICT[enigma_type][used_rotors[1]][1], offset_2, position_2)
    rotor_3 = Rotor("Rotor 3", ROTORS_DICT[enigma_type][used_rotors[2]][0], ROTORS_DICT[enigma_type][used_rotors[2]][1], offset_3, position_3)
    
    reflector = Reflector(REFLECTORS_DICT[enigma_type][reflector_pick][1], REFLECTORS_DICT[enigma_type][reflector_pick][0])
    
    return MACHINE_TYPES[enigma_type], rotor_1, rotor_2, rotor_3, reflector, plugboard

def main():

    reuse = False

    while True:

        if not reuse:
            enigma_type, used_rotors, reflector_pick, offset_1, offset_2, offset_3, position_1, position_2, position_3, plugboard = setup_enigma()

        enigma, rotor_1, rotor_2, rotor_3, reflector, plugboard = build(enigma_type, used_rotors, reflector_pick, offset_1, offset_2, offset_3, position_1, position_2, position_3, plugboard)
        enigma = Enigma(enigma, rotor_1, rotor_2, rotor_3, reflector, plugboard)

        text = input("Enter your message: ").upper().replace(" ","")
    
        cipher_text = ''.join([enigma.encryption(letter) for letter in text if letter.isalpha()])
        print(f"Cipher text: {' '.join(cipher_text[i:i+5] for i in range(0,len(cipher_text),5))}")
        
        go_again = get_user_input("Perform another operation? (y/n): ", ('y','n','Y','N'))

        if go_again == 'n':
            break

        save_setting = get_user_input("Do you want to reuse the previous configuration? (y/n): ", ('y','n','Y','N'))

        if save_setting in ('Y','y'):
            reuse = True
        else:
            reuse = False

if __name__ == "__main__":
    main()
