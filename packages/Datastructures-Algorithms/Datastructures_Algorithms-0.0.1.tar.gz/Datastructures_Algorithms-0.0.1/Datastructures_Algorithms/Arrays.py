class Arrays:
    def __init__(self, size):
        self.n = size # Size of static array
        self.arr = [] 
        self.arr[:self.n] = 'o' * (size + 1) # 'o' is the empty marker
        self.end = 0 # Position of end of file marker
        

    def insert(self, element, index=None):
        ''' Inserting element in array according to index position'''
        
        if index == None:
            
            # If index is not provided push element in end of the array
            if self.end < self.n:
                # Insert there is empty space in array
                self.arr[self.end] = element
                self.end +=1
           
            else:
                # Overflow array is already full
                print('Index out of Bound Overflow')
                
                
        
        elif (index >= 0) and (index < self.n):
            # If index value is given and is under specified size of array
            for i in range(self.end-1, index-1, -1):
                # Loop to shift elements to the right
                self.arr[i+1] = self.arr[i]
            self.arr[index] = element
            
            if self.end != self.n:
                # if end marker is under size of array increment end marker
                self.end +=1
        else:
            print('Index out of bounds Overflow')
            
              
    def delete(self, index=None):
        '''Delete element from array at an index or at end'''
        if index == None:
            
            # If index is not provided pop element from end of the list
            if self.end > 0:
                # Delete only if array is not empty
                self.end -=1
           
            else:
                # Underflow
                print('Index out of Bound Underflow')
        
        elif (index >= 0) and (index < self.end):
            # If index value is given and is under specified size of array
            for i in range(index, self.end):
                # Loop to shift elements to the left
                self.arr[i] = self.arr[i+1]
            self.end -=1
        else:
            print('Index out of bounds Underflow')
            
    
    def access(self, index=None):
        '''Function to access the elements of the lists'''
        
        if index == None:
            # If index is not provided return all array
            return self.arr[:self.end]
        
        elif (index >= 0) and (index <= self.end):
            # If index is under array bound return value at array
            return self.arr[index]
        else:
            print('Index out of bounds')
            
    
    def update(self, element, index=None):
        '''Function to update and element at a given index'''
        if index == None:
            # If index is not provided
            print('Need index to update')
        
        elif (index >= 0) and (index <= self.end):
            # If index is under array bound update 
            self.arr[index] = element
        else:
            print('Index out of bounds')
        
        
    def length(self):
        length = len(self.arr) -1
        return length