import random
import sys
sys.setrecursionlimit(9999)


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

    def set_prev(self, node, reverse_toggle):
        if reverse_toggle == False:
            self.prev_node = node
        else:
            self.next_node = node

    def get_next(self, reverse_toggle):
        if reverse_toggle == False:
            return self.next_node
        else:
            return self.prev_node

    def set_next(self, node, reverse_toggle):
        if reverse_toggle == False:
            self.next_node = node
        else:
            self.prev_node = node

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
        self.rev_toggle = False
        self.head = self.sentinel
        self.tail = self.sentinel

    def __len__(self):
        return self.size

    def __str__(self):
        return_str = ''

        if self.size != 0:
            node = self.sentinel.get_next(self.rev_toggle)
            while node.get_data() != None:
                return_str += str(node.get_data()) + " "
                node = node.get_next(self.rev_toggle)

        return return_str

    def insert(self, value):
        new_node = Node()
        new_node.set_data(value)

        new_node.set_next(self.current_node, self.rev_toggle)
        new_node.set_prev(self.current_node.get_prev(
            self.rev_toggle), self.rev_toggle)

        self.current_node.get_prev(self.rev_toggle).set_next(
            new_node, self.rev_toggle)
        self.current_node.set_prev(new_node, self.rev_toggle)

        if self.current_position == "Tail":  # to make sure the current position is changed to the end of the list
            self.current_position = self.size-1

        self.current_node = new_node
        self.size += 1

    def remove(self, current_node=None, is_remove_all=False):
        if self.current_node.get_data() == None:
            return
        if current_node == None:
            current_node = self.current_node

        next_node = current_node.get_next(self.rev_toggle)
        prev_node = current_node.get_prev(self.rev_toggle)

        next_node.set_prev(prev_node, self.rev_toggle)
        prev_node.set_next(next_node, self.rev_toggle)

        if is_remove_all == False:
            self.current_node = next_node
        self.size -= 1

    def get_value(self):
        return self.current_node.get_data()

    def move_to_next(self):
        if self.current_position != "Tail":

            if self.current_position + 1 == self.size:
                self.current_position = "Tail"
                self.current_node = self.current_node.get_next(self.rev_toggle)
            else:
                self.current_position += 1
                self.current_node = self.current_node.get_next(self.rev_toggle)

    def move_to_prev(self):
        if self.current_position == "Tail":
            self.current_position = self.size-1
            self.current_node = self.current_node.get_prev(self.rev_toggle)

        elif self.current_position - 1 != -1:
            self.current_position -= 1
            self.current_node = self.current_node.get_prev(self.rev_toggle)

    def move_to_pos(self, position):
        if 0 <= position <= self.size-1:
            # for when current position is self.sentinel
            if type(self.current_position).__name__ == "str":
                if position >= self.size/2:  # finds out which way is fastest
                    self.current_position = self.size-1
                else:
                    self.current_position = 0
                    self.current_node = self.sentinel.get_next(self.rev_toggle)

            gap = position - self.current_position
            middle = (self.size+1) // 2  # +1 accounting for sentinel node
            if gap > 0:
                if gap <= middle:  # determines which is the shorter route
                    self.__move_right(gap)
                else:
                    # calculations for the shorter route
                    self.__move_left((self.size+1)-gap)
            elif gap < 0:
                if abs(gap) <= middle:  # determines which is the shorter route
                    self.__move_left(abs(gap))
                else:
                    # calculations for the shorter route
                    self.__move_right((self.size+1)-abs(gap))
            self.current_position = position

    def remove_all(self, value, selected_node=None, selected_position=0):
        current_removed = False
        if selected_node == None:
            selected_node = self.sentinel.get_next(self.rev_toggle)

        if selected_node.get_data() != None:
            self.remove_all(value, selected_node.get_next(
                self.rev_toggle), selected_position+1)
            if selected_node.get_data() == value:
                if selected_node == self.current_node:
                    current_removed = True
                if self.current_position > selected_position:
                    self.current_node = self.current_node.get_next(
                        self.rev_toggle)
                self.remove(selected_node, True)
        if current_removed:
            self.current_node = self.sentinel.get_next(self.rev_toggle)
            self.current_position = 0

    def reverse(self):
        self.rev_toggle = not self.rev_toggle
        self.current_position = 0
        self.current_node = self.sentinel.get_next(self.rev_toggle)

    def sort(self):

        self.rev_toggle = False
        tempNode = self.mergeSort(self.sentinel.get_next(self.rev_toggle))
        tempNode.set_prev(self.sentinel, self.rev_toggle)
        self.sentinel.set_next(tempNode, self.rev_toggle)

        print()

    def mergeSort(self, left):

        if left == None or left.get_next(self.rev_toggle) == None:
            return left

        right = self.split(left)

        left = self.mergeSort(left)
        right = self.mergeSort(right)

        val = self.merge(left, right)
        return val

    def split(self, head):

        runner = head
        middle = head

        while True:
            if runner.get_next(self.rev_toggle) == None:
                break
            if runner.get_next(self.rev_toggle).get_next(self.rev_toggle) == None:
                break
            if runner.get_next(self.rev_toggle).get_data() == None:
                break
            if runner.get_next(self.rev_toggle).get_next(self.rev_toggle).get_data() == None:
                break

            runner = runner.get_next(self.rev_toggle).get_next(self.rev_toggle)
            middle = middle.get_next(self.rev_toggle)

        temp = middle.get_next(self.rev_toggle)
        middle.set_next(None, self.rev_toggle)

        return temp

    def merge(self, first, second):

        if first == None:
            second.set_next(self.sentinel, self.rev_toggle)
            return second

        if second == None:
            first.set_next(self.sentinel, self.rev_toggle)
            return first

        if first.get_data() == None:  # edge case for the sentinel
            return second

        if second.get_data() == None:
            return first

        firstVal = first.get_data()
        secondVal = second.get_data()

        if firstVal < secondVal:
            first.set_next(self.merge(first.get_next(
                self.rev_toggle), second), self.rev_toggle)
            first.get_next(self.rev_toggle).set_prev(first, self.rev_toggle)
            first.set_prev(None, self.rev_toggle)

            if first.get_next(self.rev_toggle) == first:
                first.set_next(self.sentinel, self.rev_toggle)
                self.sentinel.set_prev(first, self.rev_toggle)
                
            return first

        else:
            second.set_next(self.merge(first, second.get_next(
                self.rev_toggle)), self.rev_toggle)
            second.get_next(self.rev_toggle).set_prev(second, self.rev_toggle)
            second.set_prev(None, self.rev_toggle)

            if second.get_next(self.rev_toggle) == second:
                second.set_next(self.sentinel, self.rev_toggle)
                self.sentinel.set_prev(second, self.rev_toggle)

            return second

    # def sort(self, selected_node=None):

    #     self.rev_toggle = False
    #     selected_node = self.sentinel.get_next(self.rev_toggle)
    #     while True:
    #         self.__swap(selected_node)

    #         selected_node = selected_node.get_next(self.rev_toggle)
    #         if selected_node.get_data() == None:
    #             self.current_position = 0
    #             self.current_node = self.sentinel.get_next(self.rev_toggle)
    #             return

    #     self.rev_toggle = False
    #     if selected_node == None:
    #         selected_node = self.sentinel.get_next(self.rev_toggle).get_next(self.rev_toggle)

    #     self.__swap(selected_node)

    #     if type(selected_node.get_next(self.rev_toggle).get_data()).__name__ != 'NoneType':
    #         self.sort(selected_node.get_next(self.rev_toggle))

    # def __swap(self, selected_node):
    #     if type(selected_node.get_prev(self.rev_toggle).get_data()).__name__ != 'NoneType':

    #         if selected_node.get_data() < selected_node.get_prev(self.rev_toggle).get_data():
    #             next_node = selected_node.get_next(self.rev_toggle)
    #             prev_node = selected_node.get_prev(self.rev_toggle)

    #             selected_node.get_next(self.rev_toggle).set_prev(prev_node, self.rev_toggle)
    #             selected_node.get_prev(self.rev_toggle).set_next(next_node, self.rev_toggle)
    #             selected_node.set_prev(prev_node.get_prev(self.rev_toggle), self.rev_toggle)
    #             prev_node.get_prev(self.rev_toggle).set_next(selected_node, self.rev_toggle)
    #             prev_node.set_prev(selected_node, self.rev_toggle)
    #             selected_node.set_next(prev_node, self.rev_toggle)

    #             self.__swap(selected_node)

    def __move_left(self, gap, counter=1):
        if counter == gap:
            self.current_node = self.current_node.get_prev(self.rev_toggle)
        else:
            self.__move_left(gap, counter+1)
            self.current_node = self.current_node.get_prev(self.rev_toggle)

    def __move_right(self, gap, counter=1):
        if counter == gap:
            self.current_node = self.current_node.get_next(self.rev_toggle)
        else:
            self.__move_right(gap, counter+1)
            self.current_node = self.current_node.get_next(self.rev_toggle)


newLinkedList = DLL()
# for i in range(10):
#     newLinkedList.insert(random.randint(1, 50))

newLinkedList.insert(1)
newLinkedList.insert(4)
newLinkedList.insert(2)
newLinkedList.insert(4)
newLinkedList.insert(3)
newLinkedList.insert(5)
newLinkedList.insert(5)
newLinkedList.insert(5)
newLinkedList.insert(444)
newLinkedList.insert(5)
newLinkedList.insert(18)


print(newLinkedList)
newLinkedList.sort()
print(newLinkedList)

# newLinkedList.move_to_prev()
# newLinkedList.insert("blablíblúbla")
# print(newLinkedList.get_value())
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
