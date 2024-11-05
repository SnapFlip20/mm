import tkinter as tk

class Keyword:
    def __init__(self, *args):
        self.text = 'default'
        self.layer = 0
        self.pos_x = 0.0
        self.pos_y = 0.0
        self.parent = None
        self.child = []
        self.num = 0

        if len(args) > 0:
            if isinstance(args[0], str):
                self.text = args[0]
            if isinstance(args[1], int):
                self.layer = args[1]

    def __repr__(self):
        return f'{self.text}'
    
    def __str__(self):
        # for test
        par = 'X' if self.parent == None else self.parent.text
        return f'Keyword: {self.text}, layer: {self.layer}\n --- parent: {par}, child: {self.child}\n'

all_node = []

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
            prv_node3.child.append(gen_node)

            all_node.append(gen_node)

        elif context.startswith('###'): # sub-sub-keyword
            detail = context[4:].strip()
            gen_node = Keyword(detail, 3)

            prv_node3 = gen_node
            gen_node.parent = prv_node2
            prv_node2.child.append(gen_node)

            all_node.append(gen_node)

        elif context.startswith('##'): # sub-keyword
            sub_topic = context[3:].strip()
            gen_node = Keyword(sub_topic, 2)

            prv_node2 = gen_node
            gen_node.parent = root_node
            root_node.child.append(gen_node)

            all_node.append(gen_node)

        elif context.startswith('#'): # keyword
            main_topic = context[2:].strip()
            gen_node = Keyword(main_topic, 1)
            root_node = gen_node

            all_node.append(gen_node)

    f.close()

def show():
    ctx, cty = 800, 400
    main_keyword = all_node[0]
    main_keyword.pos_x = ctx - len(main_keyword.text)*12
    main_keyword.pos_y = cty - 30

    label_lst = [tk.Label(mainWindow) for _ in range(len(all_node)+1)]

    for now in all_node:
        match now.layer:
            case 1:
                now.pos_x = ctx-len(now.text)*12
                now.pos_y = cty-40
                print(now.pos_x, now.pos_y)

                node = label_lst.pop()
                node.config(font=('Times New Roman', 20), text=now.text)
                node.place(x=now.pos_x, y=now.pos_y)

                layer2_left = now.child[:len(now.child)//2]
                left_span = 400
                layer2_right = now.child[len(now.child)//2:]
                right_span = 400

                for (i, chd) in enumerate(layer2_left):
                    # one character = 14px(maybe)
                    chd.pos_x = now.pos_x - len(chd.text)*14 - 80
                    if len(layer2_left) == 1:
                        chd.pos_y = now.pos_y
                    else:
                        chd.pos_y = now.pos_y - left_span//2 + i*(left_span//(len(layer2_left)-1))
                
                for (i, chd) in enumerate(layer2_right):
                    chd.pos_x = now.pos_x + len(now.text)*14 + 80
                    if len(layer2_right) == 1:
                        chd.pos_y = now.pos_y
                    else:
                        chd.pos_y = now.pos_y - right_span//2 + i*(right_span//(len(layer2_right)-1))
            
            case 2:
                node = label_lst.pop()
                node.config(font=('Times New Roman', 20), text=now.text)
                node.place(x=now.pos_x, y=now.pos_y)



def main():
    parsing_md('test3.in')
    #for i in all_node:
        #print(i)
    
    #test1 = tk.Label(mainWindow, font = ('Times New Roman', 20), text = 'key')
    #test1.place(x=458, y=310)

    show()
    
    mainWindow.mainloop()



if __name__ == "__main__":
    mainWindow = tk.Tk()
    width = mainWindow.winfo_screenwidth()
    height = mainWindow.winfo_screenheight()
    mainWindow.geometry(f"1600x800")
    mainWindow.resizable(width = False, height = False)
    main()
