class Stack:
    
    def __init__(self):
        '''Function to Initialize stack '''
        self.stack = []
        self.top = -1
        
    
    def push(self, element):
        '''Function to insert element at top of the stack'''
        self.top +=1
        self.stack.append(element)
        return self.stack[self.top]
        
    
    def pop(self):
        '''Function to delete an element from top of the stack'''
        if self.top >= 0:
            temp = self.stack[self.top]
            self.stack[self.top] = None
            self.top -=1
            return temp
        else:
            print('Stack is already empty')
    
    
    def n_elements(self):
        '''Function to return number of elemnt on Stack'''
        return (self.top + 1)
    
    
    def top_element(self):
        ''' Function to return element on top of stack'''
        
        if self.top >= 0:
            return self.stack[self.top]
        
        else:
            print('No element on top, stack is empty')