# Checking the Transaction hash in output file and returning the Edge inputFileRowData and outputFileRowData for the same Transaction hash from Input file and Output file
# Author: Anmol Agarwal

def getInputTransactionData(userInputHash):
    hashList = []
    inputFileRowData = []
    for m in range(1,13):
        #for files of month 2010
        m = str(m)
        
        with open("D:/UofM Classes/Blockchain/Project/2010/outputs2010_"+m+".txt","r") as outputFile:
            with open("D:/UofM Classes/Blockchain/Project/2010/inputs2010_"+m+".txt","r") as inputFile:
                outputFileLines = outputFile.readlines()
                inputFileLines = inputFile.readlines()
                for i in range(len(outputFileLines)):
                    hashList.append(outputFileLines[i].split("\t")[1])  
                    
                # 1. the user input hash is checked in Output file
                # 2. if the user input hash is available in Output file, then Input File is checked
                # 3. if the Output Transaction Hash is available in Input File, then the inputFileRowData for that transaction hash is returned
                # 4. outputFileRowData is also returned containing Output File data for same Hash
                if userInputHash in hashList:  
                    for k in range(len(outputFileLines)):
                        if userInputHash in outputFileLines[k].split("\t")[1]:
                            outputFileRowData = outputFileLines[k].split("\t")
                    for j in range(len(inputFileLines)):
                        if userInputHash in inputFileLines[j].split("\t")[1]:
                            inputFileRowData = inputFileLines[j].split("\t")  
        
    if len(inputFileRowData) == 0:
        return "Input Hash is wrong or Data not found"          
    return inputFileRowData, outputFileRowData 

# Testing done for Transactions hashes from all output files 
#print(getInputTransactionData("b6af26bf360c141937de55a88ef8033852c372d188d38863a3e0ec1c71bd63eb"))