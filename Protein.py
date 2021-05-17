data = open("proteins.txt", "r")
data_read = data.read()

AA_dict = {}
acid_charge = {}
base_charge = {}


# functions

def floating(list_of_string):
    for i in range(len(list_of_string)):
        list_of_string[i] = float(list_of_string[i])
    return list_of_string


# scrape the data for names and pKr
data_data_read = data_read.split()
full_letter_names = (data_data_read[4:44])[::2]
three_letter_names = (data_data_read[48:88])[::2]
single_letter_names = (data_data_read[92:132])[::2]
terminal_end_both = (data_data_read[176:180])
terminal_end_names = (data_data_read[176:180])[::2]
terminal_end_values = (data_data_read[176:180])[1::2]
# print(terminal_end_both)
pKr = (data_data_read[4:44])[1::2]
pKr_long = pKr + pKr + pKr + terminal_end_values
names = full_letter_names + three_letter_names + single_letter_names + terminal_end_names

# I will recycle the acidic condition names since it is in the same order as basic condition names
acidic_condition_both_full = data_data_read[135:153]
acidic_condition_both_triple = data_data_read[200:218]
acidic_condition_both_single = data_data_read[244:262]
acidic_condition_names_full = (data_data_read[135:153])[::2]
acidic_condition_names_triple = (data_data_read[200:218])[::2]
acidic_condition_names_single = (data_data_read[244:262])[::2]
acidic_condition_values = (data_data_read[135:153])[1::2]

acidic_condition_names_total = (
        acidic_condition_names_single + acidic_condition_names_triple + acidic_condition_names_full)
acidic_condition_values_master = acidic_condition_values + acidic_condition_values + acidic_condition_values
# making the charges floats
floating(acidic_condition_values)
basic_condition_both_full = data_data_read[156:174]
basic_condition_both_triple = data_data_read[222:240]
basic_condition_both_single = data_data_read[266:284]
basic_condition_names_full = (data_data_read[156:174])[::2]
basic_condition_names_triple = (data_data_read[222:240])[::2]
basic_condition_names_single = (data_data_read[266:284])[::2]
basic_condition_values = (data_data_read[156:174])[1::2]

basic_condition_names_total = (basic_condition_both_single + basic_condition_names_triple + basic_condition_names_full)
basic_condition_values_master = (basic_condition_values + basic_condition_values + basic_condition_values)
# making the charges floats
floating(basic_condition_values)

# acidic conditions dictionary
for key in acidic_condition_names_total:
    for value in acidic_condition_values_master:
        acid_charge[key] = value
        acidic_condition_values_master.remove(value)
        break

# basic conditions dictionary
for key in acidic_condition_names_total:
    for value in basic_condition_values_master:
        base_charge[key] = value
        basic_condition_values_master.remove(value)
        break

# make the pKr floats so we can treat them like numbers
floating(pKr)
list(pKr)

# make a dictionary for each, [name] : pKr
for key in names:
    for value in pKr_long:
        AA_dict[key] = value
        pKr_long.remove(value)
        break

pH = float(input("Input the pH of the environment:"))
# make sure its separated by spaces
# AA_sequence = input("Input the sequence of the amino acids, separated with spaces.
# You can use any capitalization/3 letter/1 letter variation)
AA_sequence = "cys ala"
sequence = AA_sequence.split(" ")

# make it all uppercase so its standardized
for i in range(len(sequence)):
    sequence[i] = sequence[i].upper()

# handle the terminal ends
N_terminus = "NH2"
C_terminus = "COOH"

sequence.append(C_terminus)
sequence.insert(0, N_terminus)

print("The inputted sequence is: {}".format(sequence))
AA_pkr_sequence = []
for i in range(len(sequence)):
    if sequence[i] in AA_dict.keys():
        AA_pkr_sequence.append(AA_dict[sequence[i]])

print("The corresponding pKr(s) to the sequence is: {}".format(AA_pkr_sequence))
floating(AA_pkr_sequence)
neo = []
for i in range(len(AA_pkr_sequence)):
    if sequence[i] in acidic_condition_names_total:
        if pH < AA_pkr_sequence[i]:
            neo.append(acid_charge[sequence[i]])
        if pH > AA_pkr_sequence[i]:
            neo.append(base_charge[sequence[i]])
        if pH == AA_pkr_sequence[i]:
            neo.append(0.5)
    else:
        neo.append(0)
print("The sequence of charges at pH {} is {}".format(pH, neo))
floating(neo)
print("Net charge at pH", pH, "is", sum(neo))



