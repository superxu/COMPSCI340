#!/usr/bin/env python3
#add by Name: Shupeng Xu  UPI: sxu487   Student ID: 8260026


class Stack():
    """ simulate a stack using list """
    def __init__(self):
        self.items = []
        
    def isEmpty(self):
        return len(self.items) == 0 
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if not self.isEmpty():
            return self.items.pop() 

        return None
    
    def topitem(self):
        if not self.isEmpty():
            stacksize = self.size()
            return self.items[stacksize-1]
        
    def size(self):
        return len(self.items) 


    def topindex(self):
        return (len(self.items)-1)


    def find_item(self, id):
        if not self.isEmpty():
            for process in self.items:
              if id == process.id:
                return process

        return None

   
    def remove_item(self, process):
        if not self.isEmpty():
            self.items.remove(process)

        return None


    def get_item_index(self, process):
        if not self.isEmpty():
            return self.items.index(process)


    def show_stack(self):
        if not self.isEmpty():
            for process in self.items:
                print("process.id = %s" % process.id)

        return None



    