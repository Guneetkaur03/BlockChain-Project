class Node:
    inputs = []
    outputs = []

    # parameterized constructor
    def _init_(self, inp, outp):
        self.inputs = inp  
        self.outputs = outp
		

    # a method
    def read_time(self):
        print(self.inputs[0])
        return inputs[0]
	
    def read_hash(self):
	    print (self.inputs[1] )
	    return inputs[1]
		
    def inputs_as_tuples(self):
	    listofTuples = []
	    i = 2
	    while i < len(self.inputs):
		    #tup = []
			# tup.append(test_tup[i:i+2])
			# tup.append(test_tup[i+1])
		    listofTuples.append(self.inputs[i:i+2])
		    i = i+2
        
        #print(listofTuples[])
	    return (listofTuples)
	
	    
    def ouputs_as_tuples(self):
	    listofTuples2 = []
	    j = 2
	    while j < len(self.outputs):
		    #tup = []
			# tup.append(test_tup[i:i+2])
			# tup.append(test_tup[i+1])
		    listofTuples2.append(self.inputs[j:j+2])
		    j = j+2
        
        #print(listofTuples[])
	    return (listofTuples2)

#inp = [1264078326,f2fca47e593029b6e689d9514a1762bf7dadd5e238cc5269f9043ccec0dbbadc,3bce20d496a06035e0b938fd50b53d7040623da019132ce67163b647cf6820b9,1]
#outp = [1264078326,"f2fca47e593029b6e689d9514a1762bf7dadd5e238cc5269f9043ccec0dbbadc","18nM13Qq7hHf2hVkV2aZx8QhvWfFBMY14h",1000000,"noaddress",4574000000]
inp=['i1','i2','i3','i4']
outp=['o1','o2','o3','o4','o5','o6']
Obj1 = Node(inp,outp) # here, inp = inputFileRowData and outp = outputFileRowData 