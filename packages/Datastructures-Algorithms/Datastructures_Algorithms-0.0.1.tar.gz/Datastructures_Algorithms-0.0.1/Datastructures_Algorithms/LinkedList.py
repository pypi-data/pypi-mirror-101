class LinkedList:
    
    def __init__(self, data=None, next_node=None):
        '''Initializing variables of class'''
        self.data = data # Initializing data
        self.next_node = next_node # Initializind next node
        
    
    def insert(self, data, pos=None):
        '''Function to insert an element in linked list'''
        
        if pos == None:
            # If no argumen is provided insert at front of list
            temp1 = self.next_node
            temp = LinkedList(data, next_node=temp1) #
            self.next_node = temp
            
        elif pos > 0:
            ''' Insertion at nth position'''
            temp = self
            
            for i in range(pos):
                if temp.next_node == None:
                    print('Index out of bound')
                    return
                else:
                    temp = temp.next_node
    
            temp1 = temp.next_node
            temp2 = LinkedList(data, next_node=temp1)
            temp.next_node = temp2
            
        elif pos < 0:
            '''Insert at end of the list'''
            temp = self
            
            while temp.next_node != None:
                temp = temp.next_node
            
            # inserting data at end
            temp1 = temp.next_node
            temp2 = LinkedList(data, next_node=temp1)
            temp.next_node = temp2     
                
            
    def access(self, pos = None):
        '''Function to acess elements'''
        
        if pos == None:
            '''If no position is given print all data'''
            temp = self.next_node
            if temp != None:
                # Check to evaluate whether list is empty or not
                while True:
                    print(temp.data)

                    if temp.next_node != None:
                        temp = temp.next_node
                    else:
                        break
            else:
                print('Empty list')
                
        
        elif pos >0:
            temp = self.next_node
            for i in range(1, pos+1):              
                if pos == i:
                    print(temp.data)
                    
                if temp.next_node == None:
                    print('Index out of bound')
                    break
                temp = temp.next_node
        
        else :
            print('Index out of bound Underflow')


    def delete(self, pos=None):
        '''Function to delete element from linked list'''
        
        if pos == None:
            # Deleting at head
            temp1 = self.next_node
            temp2 = temp1.next_node
            self.next_node = temp2
        
        elif pos > 0 :
            # Deleting from an index
            temp = self
            
            for i in range(1, pos):
                temp = temp.next_node
            temp1 = temp.next_node
            temp2 = temp1.next_node
            temp.next_node = temp2
            
        else:
            print('Index out of bound Underflow')


    def  length(self):
        '''Function to return length of list'''
        temp = self
        count = 0
        while temp.next_node != None:
            count += 1
            temp = temp.next_node
        return count