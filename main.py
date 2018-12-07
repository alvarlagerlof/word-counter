import os
import sys
import re
import operator
from binaryornot.check import is_binary
from tkinter import *

CANVAS_WIDTH = 1600
CANVAS_HEIGHT = 800
CANVAS_PADDING = 50
FONT_MIN = 10
FONT_MAX = 100
FONT_FAMILIY = "Kollektif"
EXCLUDE_LIST = ["libtomcrypt"] #["node_modules"]


class Text:
    def getText(self, src):
        files = self.get_files(src)
        text = self.read_files(files)

        return text


    def get_files(self, src):
        files = []

        for (path, dirnames, filenames) in os.walk(src):
            files.extend(os.path.join(path, name) for name in filenames)
            print(files[-1])

        return files

    
    def read_files(self, files):
        all_text = ""

        for filename in files:
            if not is_binary(filename) and not any(exclude in filename for exclude in EXCLUDE_LIST):
                with open(filename, 'r') as myfile:
                    data = myfile.read()

                    all_text += data

        return all_text



class Counter:
    def count(self, text):
        return self.create_list(self.process(text))

    def process(self, text):
        print("text", text)

        new_text = re.sub(r"\B([A-Z])", r" \1", text)
        new_text = new_text.lower()
        new_text = re.sub(r'[\W_]+', ' ', new_text)
        new_text = re.sub(' \d+', ' ', new_text)
        new_text = re.sub(' +', ' ', new_text)
        char_list = [new_text[j] for j in range(len(new_text)) if ord(new_text[j]) in range(65536)]
        new_text = ''
        for j in char_list:
            new_text += j

        return new_text

    def create_list(self, text):
        array = dict()

        for word in text.split(' '):
            print(word, end=", ", flush=True)
            if len(word) < 30:
                if not word in array:
                    array[word] = 1
                else:
                    array[word] += 1

        return sorted(array.items(), key=operator.itemgetter(1), reverse=True)




class Draw:

    def calculate_size(self, array, size):
        OldRange = (array[0][1] - array[-1][1])  
        NewRange = (FONT_MAX - FONT_MIN)  

        return int(round((((size - array[-1][1]) * NewRange) / OldRange) + FONT_MIN))



    def calculate_factor(self, array, size):
        return FONT_MAX / array[0][1]


    def draw_grouped(self, array):
        master = Tk()

        w = Canvas(
            master,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT
        )
        w.pack()


        y = CANVAS_PADDING
        x = 100

        for item in array: 
            text = item[0]
            size = self.calculate_size(array, item[1])

            w.create_text(x, y, font=(FONT_FAMILIY, size), text=text)
            y += size

            print(x, y)

            if y > CANVAS_HEIGHT-50:
                print("move sideways")
                x += 200
                y = CANVAS_PADDING

        mainloop()



    def draw_vertial(self, array):
        master = Tk()

        w = Canvas(
            master,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT
        )
        w.pack()


        y = CANVAS_PADDING

        for item in array: 
            x = 100
            text = item[0]
            size = item[1]*3 + FONT_MIN

            w.create_text(100, y, font=(FONT_FAMILIY, size), text=text)
            y += size


        mainloop()

"""
words = Text().getText("./")
counter = Counter().count(words)

for item in counter: 
    #print(item[0], item[1])
    print()

draw = Draw().draw_grouped(counter)
"""


if __name__ == "__main__":
    src = sys.argv[1]
    words = Text().getText(src)
    counter = Counter().count(words)
    draw = Draw().draw_grouped(counter)