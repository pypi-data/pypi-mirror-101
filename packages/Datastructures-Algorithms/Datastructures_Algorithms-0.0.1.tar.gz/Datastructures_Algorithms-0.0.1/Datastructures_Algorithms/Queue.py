class Queue:
    
    def __init__(self):
        self.queue = []
        self.head = 0
        self.tail = 0
        
    
    def head(self):
        '''Function returns position of head'''
        return self.head
    
    
    def tail(self):
        '''Function returns position of tail'''
        return self.tail
    
    
    def dequeue(self):
        '''Function to dequeue elements from queue'''
        if self.head == self.tail:
            print('No element to dequeue')
        else:
            temp = self.head
            self.head += 1
            return self.queue[temp]
    
    
    def enqueue(self, element):
        '''Function to insert and element'''
        self.tail +=1
        try:
            self.queue[self.tail] = element
        except:
            self.queue.append(element)
        return element
        
    
    def access(self, index=None):
        '''Function to access queue'''
        if index == None:
            print(self.queue[self.head:self.tail])
            return
        try:
            index = self.head + index
            print(self.queue[index])
            return
        except:
            print('Index out of bounds')