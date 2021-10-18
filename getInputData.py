# Checking the Transaction hash in output file and returning the Edge inputFileRowData for the same Transaction hash from Input file
# Author: Anmol Agarwal

def getInputTransactionData(userInputHash):
    hashList = []
    inputFileRowData = []
    for m in range(1,13):
        #for files of month 2010
        m = str(m)
        inputFile = open("D:/UofM Classes/Blockchain/Project/2010/inputs2010_"+m+".txt","r");
        outputFile = open("D:/UofM Classes/Blockchain/Project/2010/outputs2010_"+m+".txt","r");
        outputFileLines = outputFile.readlines()
        inputFileLines = inputFile.readlines()
        for i in range(len(outputFileLines)):
            hashList.append(outputFileLines[i].split("\t")[1])  

        # First, the user input hash is checked in Output file
        # Second, if the user input hash is available in Output file, the Input File is checked
        # Third, if the Output Transaction Hash is available in Input File, then the inputFileRowData for that transaction hash is returned
       
        if userInputHash in hashList:    
            for j in range(len(inputFileLines)):
                if userInputHash in inputFileLines[j].split("\t")[1]:
                    inputFileRowData = inputFileLines[j].split("\t")      

    if len(inputFileRowData) == 0:
        return "Input Hash is wrong or Data not found in Input File"          
    return inputFileRowData  

# Testing done for Transactions hashes from output files 1,3,5,7
print(getInputTransactionData("4d67ee35cbdabf8b6f403a75305895c032fcecf9b366d0fe81c92dad02e807b"))