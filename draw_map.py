# Last updated: 2024-11-12

import tkinter as tk
from tkinter import Canvas
import tkinter.font as tkFont
from PIL import Image, ImageDraw, ImageFont



all_node = []
char_len = []


class Keyword:
    def __init__(self, *args):
        self.text = 'default'
        self.layer = 0 # depth of node
        self.pos_x = 0.0 # top-left x coordinate of text
        self.pos_y = 0.0 # top-left y coordinate of text
        self.parent = None
        self.child = []
        self.direction = -1 # -1 : left / 1: right
        self.tlen = 0 # text length(in canvas)

        if len(args) > 0:
            if isinstance(args[0], str):
                self.text = args[0]
            if isinstance(args[1], int):
                self.layer = args[1]

    def __repr__(self):
        return f'{self.text}'
    
    def __str__(self):
        # for debug
        par = 'X' if self.parent == None else self.parent.text
        return f'Keyword: {self.text}, layer: {self.layer}\n --- parent: {par}, child: {self.child}\n'

    def __lt__(self, other):
        return len(self.text) < len(self.text)
    
    def __eq__(self, other):
        return len(self.text) == len(other.text)
    
    def __len__(self):
        return len(self.text)



def add_nextline(sentence, max_words_in_line = 5):
    space_cnt = 1
    sentence_lst = list(sentence)

    for (i, j) in enumerate(sentence):
        if j == ' ':
            space_cnt += 1
        if space_cnt % (max_words_in_line+1) == 0:
            sentence_lst[i] = '\n'
            space_cnt = 1

    return ''.join(sentence_lst)

def save_canvas_as_image(canvas):
    canvas.update()
    width = canvas.winfo_width()
    height = canvas.winfo_height()
 
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    default_color = 'black'
    
    for item in canvas.find_all():
        coords = canvas.coords(item)
        item_type = canvas.type(item)
        fill = default_color

        if item_type == "line":
            #width = int(float(canvas.itemcget(item, "width")))
            #draw.line(coords, fill=fill, width=width, joint="curve")
            draw.line(coords, fill=fill)

        elif item_type == 'text':
            text = canvas.itemcget(item, 'text')
            font_name = canvas.itemcget(item, 'font')
 
            tk_font = tkFont.Font(font=font_name)
            font_size = tk_font.cget('size')
            font_path = 'C:/Windows/Fonts/arial.ttf'
            
            try:
                pillow_font = ImageFont.truetype(font_path, font_size)
            except IOError:
                pillow_font = ImageFont.load_default()
            
            draw.text((coords[0], coords[1]), text, fill=fill, font=pillow_font)

    image.save('generated_image.png')

def parsing_md(file_name: str):
    f = open(file_name, 'r')
    extracted = [i.strip() for i in f.readlines()]
    root_node = Keyword()
    prv_node2 = Keyword()
    prv_node3 = Keyword()

    for (idx, context) in enumerate(extracted):
        if context.startswith('####'): # description
            detail = context[5:].strip()
            gen_node = Keyword(detail, 4)

            gen_node.parent = prv_node3
            gen_node.tlen = len(detail)
            prv_node3.child.append(gen_node)

            all_node.append(gen_node)

        elif context.startswith('###'): # sub-sub-keyword
            detail = context[4:].strip()
            gen_node = Keyword(detail, 3)

            prv_node3 = gen_node
            gen_node.parent = prv_node2
            gen_node.tlen = len(detail)
            prv_node2.child.append(gen_node)

            all_node.append(gen_node)

        elif context.startswith('##'): # sub-keyword
            sub_topic = context[3:].strip()
            gen_node = Keyword(sub_topic, 2)

            prv_node2 = gen_node
            gen_node.parent = root_node
            gen_node.tlen = len(sub_topic)
            root_node.child.append(gen_node)

            all_node.append(gen_node)

        elif context.startswith('#'): # keyword
            main_topic = context[2:].strip()
            gen_node = Keyword(main_topic, 1)
            gen_node.tlen = len(main_topic)
            root_node = gen_node

            all_node.append(gen_node)

    f.close()

def show():
    ctx, cty = 855, 500 # center coordinate

    for now in all_node:
        match now.layer:
            case 1: # keyword
                now.pos_x = ctx-len(now.text)*12
                now.pos_y = cty

                cv.create_text(now.pos_x, now.pos_y, text=now.text, font=('Arial', 34))
                #cv.create_text(1340, 450, text='a', font=('Arial', 30))

                layer2_left = now.child[:len(now.child)//2]
                left_span = 450
                layer2_right = now.child[len(now.child)//2:]
                right_span = 450

                for (i, chd) in enumerate(layer2_left):
                    longest = max(layer2_left).tlen
                    #chd.pos_x = max(now.pos_x - longest*30 - 120, 540)
                    chd.pos_x = 490
                    chd.direction = -1
                    if len(layer2_left) == 1:
                        chd.pos_y = now.pos_y + 6
                    else:
                        chd.pos_y = now.pos_y - left_span//2 + i*(left_span//(len(layer2_left)-1))
                    
                    cv.create_line(now.pos_x-5, now.pos_y+19,
                                   chd.pos_x+chd.tlen*10, chd.pos_y+13, smooth=True)
                
                for (i, chd) in enumerate(layer2_right):
                    #chd.pos_x = min(now.pos_x + now.tlen*30 + 40, 1000)
                    chd.pos_x = 1030
                    chd.direction = 1
                    if len(layer2_right) == 1:
                        chd.pos_y = now.pos_y
                    else:
                        chd.pos_y = now.pos_y - right_span//2 + i*(right_span//(len(layer2_right)-1))

                    cv.create_line(now.pos_x+now.tlen*18+20, now.pos_y+17,
                                   chd.pos_x-5, chd.pos_y+18, smooth=True)
            
            case 2: # sub-keyword
                cv.create_text(now.pos_x, now.pos_y, text=now.text, font=('Arial', 20))
                
                layer3 = [*now.child]
                left_span = 70*len(layer3)
                right_span = 70*len(layer3)

                for (i, chd) in enumerate(layer3):
                    if now.direction == -1: # left
                        chd.direction = -1
                        longest = max(layer3).tlen
                        #chd.pos_x = min(now.pos_x - longest*12 - 40, 140)
                        chd.pos_x = 80
                        if len(layer3) == 1:
                            chd.pos_y = now.pos_y + 12
                        else:
                            chd.pos_y = now.pos_y - left_span//2 + i*(left_span//(len(layer3)-1))

                        cv.create_line(now.pos_x-3, now.pos_y+12,
                                       370, chd.pos_y+12, smooth=True)

                    elif now.direction == 1: # right
                        chd.direction = 1
                        #chd.pos_x = now.pos_x + now.tlen*12 + 40
                        chd.pos_x = 1330
                        if len(layer3) == 1:
                            chd.pos_y = now.pos_y
                        else:
                            chd.pos_y = now.pos_y - right_span//2 + i*(right_span//(len(layer3)-1))

                        cv.create_line(now.pos_x + now.tlen*11.2, now.pos_y+13,
                                       chd.pos_x-7, chd.pos_y+13, smooth=True)
            
            case 3: # sub-sub-keyword
                cv.create_text(now.pos_x, now.pos_y, text=now.text, font=('Arial', 20))
                dscrp = now.child[0]

                if now.direction == -1:
                    dscrp.pos_x = now.pos_x
                    dscrp.pos_y = now.pos_y + 28
                
                elif now.direction == 1:
                    dscrp.pos_x = now.pos_x
                    dscrp.pos_y = now.pos_y + 28

            case 4: # description
                cv.create_text(now.pos_x, now.pos_y,
                               text=add_nextline(now.text), font=('Arial', 15))



if __name__ == "__main__":
    mainWindow = tk.Tk()
    mainWindow.geometry("1710x1000") # maximum canvas size

    cv = Canvas(mainWindow, width=1710, height=1000, bg='white')
    cv.pack()

    parsing_md('test3.in')

    show()

    save_canvas_as_image(cv)
