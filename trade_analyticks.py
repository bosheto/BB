
f = open('Logs\\Desy.txt', 'r')
ld = f.readlines()
f.close()

def extract_value(line):
    line = line.split(' ')
    return line[-1]

total_profit = 0

for line in ld:
    if line == '\n':
        pass
    if 'Profit' in line:
        total_profit += float(extract_value(line))

print(total_profit)