
def searchInputTransaction(thash):
    #result=[0,1,2]
    inputTransactionsArray=[]
    # for all months input files of 2010
    for month in range (1,13):
      m=str(month)
      
      #print(path)
      file =open("Data/edges2010/inputs2010_"+m+".txt", "r")
      lines=file.readlines()
      file.close()
      reslen=len(lines)
      #print("for loop in python")
    
      for i in range(0,reslen):
       lineArray=lines[i].split("\t")
       if(thash in lineArray):
         #used inputTransaction Array to hold different input transactions of given Transaction hash of Output file
        inputTransactionsArray.append(lineArray)
        
    return inputTransactionsArray
   

