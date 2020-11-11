

def write_to_file(file, data):
    data.to_csv(file)

def update_curency_file(symbol, dataframe):
    try:
        with open('CSV\\' + symbol + '.csv', 'a') as f:
            dataframe.to_csv()
            f.close()
    except FileNotFoundError:
        with open('CSV\\' + symbol + '.csv', 'w') as f:
            dataframe.to_csv()
            f.close()



