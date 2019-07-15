file = open('consonant_clusters.txt')

lines = file.readlines()
list_string = "["
for line in lines:
    line = line.rstrip()
    cc = "'" + line + "', "
    list_string += cc
list_string += ']'
print(list_string)