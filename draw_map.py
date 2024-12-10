# Last updated: 2024-12-10

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


# ********** Settings ********** #
all_node = []
adjusted = 80

# canvas size(pix) settings
cv_width  = 3840*2 + 960
cv_height = 2160*2
cv_width_block = cv_width/5

# font settings
default_font = ImageFont.truetype("arial.ttf", 10)
font1 = ImageFont.truetype("arial.ttf", 150)
font2 = ImageFont.truetype("arial.ttf", 100)
font3 = ImageFont.truetype("arial.ttf", 75)
txt_fill = (0, 0, 0) # black
# ********** Settings end ********** #


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
    
    def __eq__(self, other):
        return self.text == other
    
    def __len__(self):
        return len(self.text)



def add_nextline(sentence, max_words_in_line = 10) -> str:
    space_cnt = 1
    sentence_lst = list(sentence)

    for (i, j) in enumerate(sentence):
        if j == ' ':
            space_cnt += 1
        if space_cnt % (max_words_in_line+1) == 0:
            sentence_lst[i] = '\n'
            space_cnt = 1

    return ''.join(sentence_lst)

def add_nextline2(sentence, max_chars_in_line = 50) -> str:
    sentence_lst = list(sentence)

    for (i, j) in enumerate(sentence):
        if (i+1) % max_chars_in_line == 0:
            sentence_lst[i] += '\n'

    return ''.join(sentence_lst)

def extract(): # extract canvas image to .png file
    pil2opencv = cv2.cvtColor(np.array(pImg), cv2.COLOR_RGB2BGR) 
    cv2.imwrite("test.png", pil2opencv)
    cv2.destroyAllWindows()

def parsing_md(file_name: str):
    f = open(file_name, 'r', encoding='UTF8')
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

            if prv_node3 != 'default':
                prv_node3.child.append(gen_node)

                all_node.append(gen_node)

        elif context.startswith('###'): # sub-sub-keyword
            detail = (subsubkw := context[4:].strip())

            if len(detail) > 0:
                gen_node = Keyword(detail, 3)

                
                gen_node.tlen = cv.textlength(subsubkw, font=font3)
                gen_node.parent = prv_node2
                
                if len(prv_node2.child) < 3:
                    prv_node3 = gen_node
                    prv_node2.child.append(gen_node)

                    all_node.append(gen_node)
                else:
                    prv_node3 = Keyword()

        elif context.startswith('##'): # sub-keyword
            sub_topic = (subkw := context[3:].strip())
            print(root_node.child, len(root_node.child))
            if len(sub_topic) > 0:
                gen_node = Keyword(sub_topic, 2)

                prv_node2 = gen_node
                gen_node.tlen = cv.textlength(subkw, font=font2)
                gen_node.parent = root_node
                
                if len(root_node.child) < 6:
                    root_node.child.append(gen_node)

                    all_node.append(gen_node)

        elif context.startswith('#'): # keyword
            main_topic = (mainkw := context[2:].strip())
            gen_node = Keyword(main_topic, 1)
            gen_node.tlen = cv.textlength(mainkw, font=font1)
            root_node = gen_node

            all_node.append(gen_node)

    f.close()

def show():
    # center(actually, top-left) coordinate of main keyword text
    ctx, cty = cv_width_block*2 + adjusted, cv_height/2

    for now in all_node:
        match now.layer:
            case 1: # main keyword
                global layer2_left, layer2_right, layer2_left_span, layer2_right_span
                now.pos_x = ctx
                now.pos_y = cty

                cv.text((now.pos_x, now.pos_y), now.text, font=font1, fill=txt_fill)

                if len(now.child) > 6:
                    now.child = now.child[:6]

                layer2_left = now.child[:len(now.child)//2]

                layer2_right = now.child[len(now.child)//2:]

                layer2_left_span = cv_height - 1440
                layer2_right_span = cv_height - 1440

                for (i, chd) in enumerate(layer2_left): # left child of main keyword
                    chd.pos_x = cv_width_block + adjusted*4
                    chd.direction = -1
                    if len(layer2_left) == 1:
                        chd.pos_y = now.pos_y + 6
                    else:
                        chd.pos_y = now.pos_y - layer2_left_span//2 + i*(layer2_left_span//(len(layer2_left)-1))
                
                for (i, chd) in enumerate(layer2_right): # right child of main keyword
                    chd.pos_x = now.pos_x + now.tlen + adjusted*6
                    chd.direction = 1
                    if len(layer2_right) == 1:
                        chd.pos_y = now.pos_y
                    else:
                        chd.pos_y = now.pos_y - layer2_right_span//2 + i*(layer2_right_span//(len(layer2_right)-1))
            
            case 2: # sub-keyword
                cv.text((now.pos_x, now.pos_y), add_nextline2(now.text, 20), font=font2, fill=txt_fill)
                
                layer3 = [*now.child]
                left_span = (2*layer2_left_span/(len(layer2_left)+1))//1.25 - 420
                right_span = (2*layer2_right_span/(len(layer2_right)+1))//1.25 - 420

                for (i, chd) in enumerate(layer3): # left(only) child of sub-keyword
                    if now.direction == -1:
                        chd.direction = -1
                        chd.pos_x = adjusted+10
                        if len(layer3) == 1:
                            chd.pos_y = now.pos_y + 12
                        else:
                            chd.pos_y = now.pos_y - left_span//2 + i*(left_span//(len(layer3)-1))

                    elif now.direction == 1: # right(only) child of sub-keyword
                        chd.direction = 1
                        chd.pos_x = cv_width_block*4 - adjusted
                        if len(layer3) == 1:
                            chd.pos_y = now.pos_y
                        else:
                            chd.pos_y = now.pos_y - right_span//2 + i*(right_span//(len(layer3)-1))
                        
            case 3: # sub-sub-keyword
                #clen = now.tlen//5
                cv.text((now.pos_x, now.pos_y), text=add_nextline2(now.text), font=font3, fill=txt_fill)
                if now.child:
                    dscrp = now.child[0]
                    if now.direction == -1: # left(only) child of sub-keyword
                        dscrp.pos_x = now.pos_x
                        dscrp.pos_y = now.pos_y + 80
                    
                    elif now.direction == 1: # right(only) child of sub-keyword
                        dscrp.pos_x = now.pos_x
                        dscrp.pos_y = now.pos_y + 80

            case 4: # description
                #clen = now.tlen//5
                cv.text((now.pos_x, now.pos_y), text=add_nextline2(now.text), font=font3, fill=txt_fill)
                # add_nextline --- to be updated



if __name__ == "__main__":
    window = np.zeros((cv_height, cv_width, 3), dtype=np.uint8) + 255
    pImg = Image.fromarray(cv2.cvtColor(window, cv2.COLOR_BGR2RGB))
    cv = ImageDraw.Draw(pImg)

    parsing_md('output.md')
    show()
    extract()
