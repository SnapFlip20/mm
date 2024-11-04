from tkinter import Tk

class Keyword:
    def __init__(self, *args):
        self.text = 'default'
        self.layer = 0
        self.pos_x = 0.0
        self.pos_y = 0.0
        self.parent = None
        self.child = []

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

def main():
    parsing_md('test2.in')
    for i in all_node:
        print(i)


if __name__ == "__main__":
    main()