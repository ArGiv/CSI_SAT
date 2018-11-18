import uuid
import os
import random
# 
print('Generates values for the Constrained Minimal Support Set problem\nand writes them into a MiniZinc .dzn file\n')
print('Use default values? (y/n)')
if input() == 'n':
    print('Enter value for t (number of attributes):')
    t = int(input()) # number of attributes
    print('Enter value for k (maximum size of support set):')
    k = int(input()) # maximum size of support set
    print('Enter value for n (number of positive instances):')
    n = int(input()) # number of positive instances
    print('Enter value for m (number of negative instances):')
    m = int(input()) # number of negative instances
    print('Enter value for c (number of atMostOne Constraints):')
    c = int(input()) # number of atMostOne Constraints
else:
    t = 8 # number of attributes
    k = 3 # maximum size of support set
    n = 5 # number of positive instances
    m = 3 # number of negative instances
    c = 4 # number of atMostOne Constraints

# transforms and writes given data into .dzn file, data is a list of lists
def file_write_omega(file, var_name, data):
    data_string = '\n' + var_name + '=[| '
    for value_list in data:
        for value in value_list:
            data_string += value + ','
        #remove ',' at end of line
        data_string = data_string[:-1] + '|\n'
    data_string = data_string[:-2] + '\n|];\n'
    print(data_string)
    file.write(data_string)
        
# Generate positive instances
omegap = list()
for i in range(n):
    generated = list()
    for j in range(t):
        generated.append("1") if random.random() < 0.5 else generated.append("0")
    omegap.append(generated)

# Generate negative instances
omegan = list()
for i in range(m):
    generated = list()
    # Make sure positive and negative instances are disjoint
    while(len(generated) == 0 or generated in omegap):
        del generated[:]
        for j in range(t):
            generated.append("1") if random.random() < 0.5 else generated.append("0")
    omegan.append(generated)

#generate constraints
constraints = list()
for i in range(c):
    constr = list()
    # make sure there are no empty/duplicate constraints
    while(len(constr) == 0 or constr in constraints):     
        del constr[:]       
        for j in range(t):
            if random.random() < 0.5:
                constr.append(j + 1)
    constraints.append(constr)

id = (str(uuid.uuid4())[:8])

current_directory = os.getcwd()
final_directory = os.path.join(current_directory, r'data/')
if not os.path.exists(final_directory):
   os.makedirs(final_directory)
print(final_directory)
f = open(final_directory + 'data_' + id + '.dzn', 'w')

# write variable declarations to file
f.write("""t = """ + str(t) + """; %number of attributes
k = """ + str(k) + """; %maximum size of support set
n = """ + str(n) + """; %number of positive instances
m = """ + str(m) + """; %number of negative instances
c = """ + str(c) + """; %number of atMostOne Constraints\n""")

# write omegap and omegan to file
file_write_omega(f, 'omegap', omegap)
file_write_omega(f, 'omegan', omegan)

# transform constraint data into .dzn conform format
constraint_string = '\natMostOne =\n['
for constraint in constraints:
    constraint_string += '{'
    for value in constraint:
        constraint_string += str(value) + ','
    # remove ',' and add '}' at end of line
    constraint_string = constraint_string[:-1] + '},\n'
constraint_string = constraint_string[:-2] + '];'

print(constraint_string)

f.write(constraint_string)

f.close()
 