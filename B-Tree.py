class Node:
    def __init__(self, parent= None):
        self.__channelNames = [] #Dict with channelName and members
        self.__parent = parent #Sets parent of given node
        self.__child = [] #All children of node

    # Getter for __parent
    def get_parent(self):
        return self.__parent

    # Setter for __parent
    def set_parent(self, parent):
        self.__parent = parent

    # Getter for __child
    def get_children(self):
        return self.__child

    # Setter for __child
    def set_children(self, children):
        self.__child = children
    
    def __lt__(self, node): # allow sorted function to work
        return self.__channelNames[0] < node.__channelNames[0]
    
    def _add(self, newNode):
        for child in newNode.__child:
            child.__parent = self #set each childs parent to self
        
        self.__channelNames.extend(newNode.__channelNames) #combine both lists
        self.__channelNames.sort()
        self.__child.extend(newNode.__child) #extend self's children to new nodes children

    def _isLeaf(self):
        return len(self.__child)
    
    def _insert(self, newNode):

        #add if node is leaf
        if self._isLeaf:
            self._add(newNode)
        
        # if not leaf, correctly add
        elif newNode.__channelNames[0] > self.__channelNames[-1]: #compare new node data to last piece of data in self
            self.__child[-1]._insert(newNode)
        else:
            for i in range(0, len(self.data)):
                if newNode.__channelNames[0] > self.__channelNames[i]:
                    self.child[i]._insert(newNode)
                    break
        

        



class Tree:
    def __init__(self):
        self.__root = None
    
    


