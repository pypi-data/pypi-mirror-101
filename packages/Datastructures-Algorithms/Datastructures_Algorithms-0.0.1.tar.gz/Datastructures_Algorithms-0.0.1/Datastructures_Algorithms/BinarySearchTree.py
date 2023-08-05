class BinarySearchTree:
    
    def __init__(self):
        '''Function to initialize bst'''
        self.key  = None
        self.left = None
        self.right = None
       
    
    def insert(self, val):
        '''Function to insert element in bst'''
        
        if self.key == None:
            self.key = val
            return self
        else:
            if self.key == val:
                return self
            
            elif self.key > val:
                
                if self.left == None:
                    self.left = BinarySearchTree()
                    self.left.insert(val)
                else:
                    self.left.insert(val)
            
            else:
                if self.right == None:
                    self.right = BinarySearchTree()
                    self.right.insert(val)
                else:
                    self.right.insert(val)
                    
        return self.key
    
        
    def max_element(self):
        '''Function to find max element in tree'''
        if self.key == None:
            print('Empty tree')
        else:
            if self.right == None:
                return (self.key)
            else:
                return self.right.max_element()
        
        
    def min_element(self):
        '''Function to find minimum element in tree'''
        
        if self.key == None:
            print('Empty tree')
        else:
            if self.left == None:
                return self.key
            else:
                return self.left.min_element()
                
                
    def height(self):
        '''Function to calculate height of the tree'''
        if self.key == None:
            return 0
        else:
            if (self.left == None) and (self.right == None):
                return 0
            
            elif self.left == None:
                return self.right.height() + 1
            elif self.right == None:
                return self.left.height() +1
            else:
                return max(self.left.height(), self.right.height()) + 1
            
            
    def bfs_traversal(self, roots):
        '''Function to traverse tree in breadth first manner'''
        if len(roots) == 0:
            return
        
        self.new_root = []
        
        for r in roots:
            print(r.key)
        
            if r.left != None:
                self.new_root.append(r.left)
            
            if r.right != None:
                self.new_root.append(r.right)
                
        self.bfs_traversal(self.new_root)
            
    
    def pre_order_dfs(self):
        '''Function to traverse pre-order dfs'''
        
        if self.key == None:
            return
        
        else:
            print(self.key)
            
            if self.left != None:
                self.left.pre_order_dfs()
            
            if self.right != None:
                self.right.pre_order_dfs()
    
    
    def in_order_dfs(self):
        '''Function to traverse inorder dfs'''
        
        if self.key == None:
            return
        
        else:
            if self.left != None:
                self.left.in_order_dfs()
            
            print(self.key)
            
            if self.right != None:
                self.right.in_order_dfs()
                
    
    def post_order_dfs(self):
        '''Function traverese in post order'''
        
        if self.key == None:
            return
        
        else:
            if self.left != None:
                self.left.post_order_dfs()
                
            if self.right != None:
                self.right.post_order_dfs()
                
            print(self.key)
            
    
    def isBST(self):
        '''Function to check whether given tree is BST or not'''
        left_min, left_bst, right_max, right_bst = True, True, True, True
        
        if self.key == None:
            return True
        
        if self.left != None:
            left_min = self.key > self.left.min_element()
            left_bst = self.left.isBST()
                
        if self.right != None:
            right_max = self.key < self.right.max_element()
            right_bst = self.right.isBST()
                
        if left_min and left_bst and right_max and right_bst:
            return True
        else:
            return False
        
        
    def delete(self, val):
        '''Function to delete a key in BST'''
        if self.key == None:
            print('Empty tree')
        
        else:
            left, right = None, None
            
            if self.left != None and (self.key > val):
                left = self.left
                if left.key == val:
                    self.left = self.deleteUtil(left)
                else:
                    left.delete(val)
                    
                
            if self.right != None and (self.key < val):
                right = self.right
                if right.key == val:
                    self.right = self.deleteUtil(right)
                else:
                    right.delete(val)
                
            
    def deleteUtil(self, child):
        '''Utility function to delete a key'''
        if (child.left == None) and (child.right == None):
            return None
        
        elif (child.left == None) and (child.right != None):
            return child.right
        
        elif (child.left != None) and (child.right == None):
            return child.left
        
        elif (child.left != None) and (child.right != None):
            # FInd minimum in right subtree and make it child or parent
            child.min_element_node().right = child.right
            return child.min_element_node()

    
    def min_element_node(self):
        '''Helper function to get minimum node of subtree'''
        if self.left == None:
            return self
        else:
            return self.left.min_element_node()     