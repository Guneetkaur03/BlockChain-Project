import time
start_time = time.time()
f = open("Data/edges2015/outputs2015_1.txt", "r") 
end_time = time.time()
print("Time taken to load the file is {}".format(end_time - start_time))


lines = f.readlines()
print("checking some of the contents of the file, printing top 5 details")
for i in range(5):
    print(lines[i].split("\t")[0])
