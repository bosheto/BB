
f = open('Logs\\Desy.txt', 'r')
ld = f.readlines()
f.close()

def extract_value(line):
    line = line.split(' ')
    return line[-1]

total_profit = 0
total_profit_percent = 0
for line in ld:
    if line == '\n':
        pass
    if 'Profit' in line:
        total_profit += float(extract_value(line))
    if 'Gain' in line:
        total_profit_percent += float(extract_value(line))  
    

print(total_profit)
print(total_profit_percent)