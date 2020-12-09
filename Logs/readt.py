
with open('VersionTwo\\2020-12-09.txt', 'r') as f:
    lines = f.readlines()
    profit = 0
    profit_trades = 0
    loss_trades = 0
    for line in lines:
        if 'Profit ' in line:
            s = line.split(' ')
            d = float(s[-1])
            profit = profit + d
            if d > 0:
                profit_trades += 1
            elif d < 0:
                loss_trades += 1

        

    print(profit)
    print(profit_trades)
    print(loss_trades)