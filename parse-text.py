import time
from search_input import searchInputTransaction

start_time = time.time()
f = open("Data/edges2010/outputs2010_1.txt", "r") 
end_time = time.time()
print("Time taken to load the file is {}".format(end_time - start_time))

lines = f.readlines()
 
 #for one input of thash from output transaction
result=searchInputTransaction("a710033b81291d68372605237bfb4358474dce49a5099dd499f4de57d5db60ea")
#result=searchInputTransaction("32b4f53a2921a0eeafc136df61f568e7d091d18b1a2fc128f6287579942ce5b4")
resultLen=len(result)
for i in range (0,resultLen):
    print ("Transaction Hash " +str(i+1)+"    " +result[i])

