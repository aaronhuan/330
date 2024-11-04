import sys
import numpy as np
import os




##################################################
# Code for input and output
#
# You shouldn't need to change these functions.
##################################################

def parseInput(filename = None):
    if filename == None:
        try:
            weights = readIntList(sys.stdin)
        except:
            return False, "Error parsing standard input as sequence of integers."
    else:
        try:
            with open(filename, 'r') as f:
                weights = readIntList(f)
        except FileNotFoundError:
            return False, "File {} was not found.".format(filename)
        except:
            return False, "Error parsing file {} as sequence of integers.".format(filename)
    return True, weights

def readIntList(f):
    ints_list = []
    for line in f.readlines():
        if line != '\n':
            ints_list.append(int(line))
    return ints_list

def writeOutput(optset, filename = None):
    assert type(optset) == list
    if filename == None:
        writeIntList(optset, sys.stdout)
    else:
        with open(filename, 'w') as f:
            writeIntList(optset, f)


def writeIntList(optset, f):
    for x in optset:
        f.write(str(int(x)) + "\n")
    return




##################################################
# Coffee shop solution

# Look for "your code here"
##################################################


test_WTC_input = [5, 5, 9, 5, 5]
test_WTC_output = [0, 1, 3, 4]

def computeMaxValues(values):
    # values is a list of nonnegative integers 
    # values[i] is the serving capacity of location i
    assert len(values) >= 3
    n = len(values)
    # Fill the table:
    # opt[i] is the value of the heaviest ok set 
    # among vertices 0,1,...,i.
    opt = [0] * n # This is a list of n zeros.
    ########################################
    # Your code here. #opt should be just the optimal value per index

#here are the values we are guarenteed 
    opt[0] = values[0]
    opt[1] = values[0]+values[1]
    opt[2]= max (opt[1], values[0] + values[2], values[1] +values[2]) #at least 3 values, not guarenteed more 

    #opt[3]= max(opt[2], opt[1]+values[3], opt[0]+values[2]+values[3] )        not include ind 3, not include ind 2 w/ ind 3, not include ind 1 w/ ind3       if we include j we have to exclude 2 or 1

    for j in range(3,n):
        opt[j] = max(opt[j-1], opt[j-2]+values[j], opt[j-3]+ values[j-1] +values[j])

    ########################################
    return opt

def computeOptSet(values, opt):
    assert len(values) >= 3
    n = len(values)
    #Now compute the optimal set
    optset = []
    ########################################
    # Your code here. opt in input = opt output from above function
    start_val= opt[n-1]
    indice_track = n-1
    while indice_track >=0: #while we are in indicies
        if indice_track ==0:      
            optset.append(indice_track)
            start_val-= values[0]
            break 

        if indice_track==1: #if the remaining value is opt[1] then indice 0 and 1 is included 
            if start_val== opt[1]:
                optset.append(indice_track)
                optset.append(indice_track-1) #add both
                indice_track-=2            #skip the above if statement
                start_val-= opt[1]
                break
            elif start_val  == values[1]: #else just 1  
                optset.append(indice_track)
                start_val-=values[1]        #this would make it so its = 0
                break
            else: #just 0 ind 
                indice_track-=1

        if indice_track==2:       #max (opt[1], values[0] + values[2], values[1] +values[2]) 
            if start_val== values[0]+values[2]:
                optset.append(0)
                optset.append(2)
                start_val-=values[0]+values[2]
                break #done
            elif start_val== values[1]+values[2]:
                optset.append(1)
                optset.append(2)
                start_val-=values[1]+values[2]
                break #done
            else:
                indice_track-=1


        if start_val ==  opt[indice_track-1]:
            indice_track= indice_track-1
        elif start_val == opt[indice_track-2]+values[indice_track]:
            optset.append(indice_track)
            start_val= start_val- values[indice_track]
            indice_track= indice_track-2
        else:
            optset.append(indice_track)
            optset.append(indice_track-1)
            start_val-= values[indice_track] 
            start_val-= values[indice_track-1]
            indice_track=indice_track-3

    ########################################
    
    return sorted(optset) # you should return optset, once you've written code to compute it.






##################################################
# The following code allows you to run the Python file from the command line. 
# It expects two arguments: an input file and an output file.
# You should not need to modify it. 
##################################################

def main(args=[]):
    if len(args) != 2:
        print("Problem! There were {} arguments instead of 2.".format(len(args)))
        return 
    success, result = parseInput(filename = args[0])
    if success:
        values = result
        opt = computeMaxValues(values)
        optset = computeOptSet(values, opt)
        writeOutput(optset, filename = args[1])
    else:
        print(result)
    return

if __name__ == "__main__":
    main(sys.argv[1:])    


