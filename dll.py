
class Node():
    def __init__(self):
        self.prev_node = self
        self.data = None
        self.next_node = self

    def get_prev(self, reverse_toggle):
        if reverse_toggle == False:
            return self.prev_node
        else:
            return self.next_node

    def set_prev(self, node):
        self.prev_node = node

    def get_next(self, reverse_toggle):
        if reverse_toggle == False:
            return self.next_node
        else:
            return self.prev_node

    def set_next(self, node):
        self.next_node = node

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

class DLL:
    def __init__(self):
        self.sentinel = Node()
        self.current_position = 0
        self.current_node = self.sentinel
        self.size = 0
        self.reverse_toggle = False

    def __len__(self):
        return self.size

    def insert(self, value):
        new_node = Node()
        new_node.set_data(value)

        new_node.set_next(self.current_node)
        new_node.set_prev(self.current_node.get_prev(self.reverse_toggle))
        
        self.current_node.get_prev(self.reverse_toggle).set_next(new_node)
        self.current_node.set_prev(new_node)
        
        self.current_node = new_node
        self.size += 1
        
    def remove(self, current_node = None, is_remove_all = False):
        if current_node == None:
            current_node = self.current_node

        next_node = current_node.get_next(self.reverse_toggle)
        prev_node = current_node.get_prev(self.reverse_toggle)

        next_node.set_prev(prev_node)
        prev_node.set_next(next_node)

        if is_remove_all == False:
            self.current_node = next_node
        self.size -= 1

    def get_value(self):
        return self.current_node.get_data()

    def move_to_next(self):
        if self.current_position + 1 <= self.size-1:
            self.current_position += 1
            self.current_node = self.current_node.get_next(self.reverse_toggle)

    def move_to_prev(self):
        if self.current_position - 1 >= 0:
            self.current_position -= 1
            self.current_node = self.current_node.get_prev(self.reverse_toggle)

    def move_to_pos(self, position):
        if 0 <= position <= self.size-1:
            gap = position - self.current_position
            middle = (self.size+1) // 2 # +1 accounting for sentinel node
            if gap > 0:
                if gap <= middle: # determines which is the shorter route
                    self.__move_right(gap)
                else:
                    self.__move_left((self.size+1)-gap) # calculations for the shorter route
            elif gap < 0:
                if abs(gap) <= middle: # determines which is the shorter route
                    self.__move_left(abs(gap))
                else:
                    self.__move_right((self.size+1)-abs(gap)) # calculations for the shorter route
            self.current_position = position

    def remove_all(self, value, selected_node = None, selected_position = 0):
        if selected_node == None:
            selected_node = self.sentinel.get_next(self.reverse_toggle)
        
        if selected_node.get_data() != None:
            self.remove_all(value,selected_node.get_next(self.reverse_toggle), selected_position+1)
            if selected_node.get_data() == value:
                if selected_node.get_data() == self.current_node.get_data():
                    self.current_node = self.sentinel.get_next(self.reverse_toggle)
                    self.current_position = 0
                if self.current_position > selected_position:    
                    self.current_node = self.current_node.get_next(self.reverse_toggle)
                self.remove(selected_node,True)
        
    def reverse(self):
        self.reverse_toggle = not self.reverse_toggle
        self.current_position = 0
        self.current_node = self.sentinel.get_next(self.reverse_toggle)

    def sort(self, selected_node = None):
        self.reverse_toggle = False
        selected_node = self.sentinel.get_next(self.reverse_toggle)
        while True:
            self.__swap(selected_node)
            
            selected_node = selected_node.get_next(self.reverse_toggle)
            if selected_node.get_data() == None:
                return
        
        
        # self.reverse_toggle = False
        # if selected_node == None:
        #     selected_node = self.sentinel.get_next(self.reverse_toggle).get_next(self.reverse_toggle)
        # selected_node = self.__swap(selected_node)
        # if type(selected_node.get_next(self.reverse_toggle).get_data()).__name__ != 'NoneType':
        #     self.sort(selected_node.get_next(self.reverse_toggle))

        # self.current_node = self.sentinel.get_next(self.reverse_toggle)

    def __swap(self, selected_node):
        if type(selected_node.get_prev(self.reverse_toggle).get_data()).__name__ != 'NoneType':
        
            if selected_node.get_data() < selected_node.get_prev(self.reverse_toggle).get_data():
                next_node = selected_node.get_next(self.reverse_toggle)
                prev_node = selected_node.get_prev(self.reverse_toggle)
                
                selected_node.get_next(self.reverse_toggle).set_prev(prev_node)
                selected_node.get_prev(self.reverse_toggle).set_next(next_node)
                selected_node.set_prev(prev_node.get_prev(self.reverse_toggle))
                prev_node.get_prev(self.reverse_toggle).set_next(selected_node)
                prev_node.set_prev(selected_node)
                selected_node.set_next(prev_node)

                self.__swap(selected_node)
            
            
    def __move_left(self, gap, counter = 1):
        if counter == gap:
            self.current_node = self.current_node.get_prev(self.reverse_toggle)
        else:
            self.__move_left(gap, counter+1)
            self.current_node = self.current_node.get_prev(self.reverse_toggle)

    def __move_right(self, gap, counter = 1):
        if counter == gap:
            self.current_node = self.current_node.get_next(self.reverse_toggle)
        else:
            self.__move_right(gap, counter+1)
            self.current_node = self.current_node.get_next(self.reverse_toggle)



newLinkedList = DLL()

for i in range(996):
    newLinkedList.insert(i)
newLinkedList.sort()


# for i in range(12,0,-1):
#     newLinkedList.insert(i)

# newLinkedList.get_value()
# newLinkedList.move_to_next()
# newLinkedList.move_to_next()
# print(newLinkedList.get_value())
# newLinkedList.reverse()
# print(newLinkedList.get_value())
# newLinkedList.move_to_next()
# print(newLinkedList.get_value())

print()
