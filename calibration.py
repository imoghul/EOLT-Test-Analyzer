import csv, glob, os, sys
from numpy import mean


def average(x):
    if len(x) == 0: return 0
    return mean(x)


def retrieveData(fileName):
    isReading = False
    with open(fileName, newline='') as file:
        for row in csv.reader(file, delimiter='\n', quotechar=','):
            for r in row:
                v = r.split(",")
                if (v[0] == "Calibration Data"): isReading = True
                if (v[0] == "Post Calibration Data"): isReading = False
                if (isReading and v[0] == "Air"):
                    if v[4] != '': return (float(v[4]))
                    else: return None
        return None


baselineOffsets = {}
with open("calibration results.csv", mode="w", newline='') as out:
    writer = csv.writer(out)
    #output header to csv
    header = [
        "Test", "Run", "Serial Number", "Offset", "Delta Offset to Baseline"
    ]
    writer.writerow(header)

    # get list of directories to run
    if len(sys.argv) > 1:
        dirs = sys.argv[1:]
    else:
        dirs = [os.getcwd()]
    dirs.insert(0, "baseline")
    original = os.getcwd()

    for dir in dirs:
        os.chdir(dir)
        fileNames = glob.glob("*SUM*.csv", recursive=True)
        fileNames.sort()
        runs = {}
        for fileName in fileNames:
            outlist = [dir]
            try:
                offset = retrieveData(fileName)
                serialNum = fileName.split("_")[1]
                test = dir
                # check if a offset was retreived
                if offset == None: continue
                # increment number of runs
                try:
                    runs[serialNum] += 1
                except:
                    runs[serialNum] = 1
                dbOffset = 0
                if (dir == "baseline"):
                    baselineOffsets[serialNum] = offset
                else:
                    try:  # delta baseline calculation
                        dbOffset = offset - baselineOffsets[serialNum]
                    except:  # no baseline found
                        pass
                outlist = [test, runs[serialNum], serialNum, offset, dbOffset]
                print(outlist)
                writer.writerow(outlist)
            except:
                print(fileName + " couldn't be read")

        os.chdir(original)  # return to original dir
