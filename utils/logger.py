from datetime import datetime

import os
class Logger:

    def __init__(self):
        self.start_time = datetime.now()

    def add_line_to_log(self, line):  
        with open('log.txt', 'a') as f:
            timestamp = '[{0}:{1}:{2}] '.format(str(datetime.now().hour),str(datetime.now().minute), str(datetime.now().second))
            f.write(timestamp + line + '\n')
            print(timestamp + line)
            f.close()


class AI_Logger:

    def __init__(self, name):
        self.name = name
        self.file = None
        self.load_file()

    def load_file(self):
        if os.path.isdir('Logs'):
            if os.path.isfile('Logs\\' + self.name + '.txt'):
                old_name = 'Logs\\' + self.name + '.txt'
                new_name = 'Logs\\' + self.name + str(datetime.now()) + '.txt'
                #os.rename(old_name, new_name)
                
                self.file = open('Logs\\' + self.name + '.txt', 'a')
            else:
                with open('Logs\\' + self.name + '.txt', 'a') as f:
                    self.file = open('Logs\\' + self.name + '.txt', 'a')
        else:
            os.mkdir('Logs')
            self.load_file()

    def write_to_trade_file(self, trade):
        self.load_file()
        self.file.write('Symbol ' + str(trade['symbol']) + '\n')
        self.file.write('Time ' + str(trade['time']) + '\n')
        self.file.write('Buy Price ' + str(trade['buy price']) + '\n')
        self.file.write('Volume ' + str(trade['volume']) + '\n')
        self.file.write('Sell Price ' + str(trade['sell price']) + '\n')
        self.file.write('Profit ' + str(trade['profit']) + '\n')
        self.file.write('Gain % ' + str(trade['gain %']) + '\n')
        self.file.write('Flag ' + str(trade['flag']) + '\n')
        self.file.write('\n')
        self.unload_file()
    def unload_file(self):
        self.file.close()