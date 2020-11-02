# ----------------------------------------------------------------------
# Script to filter sar and pidstat txt outputs. Filters all 15 
# repetitions of the experiment.
# ----------------------------------------------------------------------
import datetime

def filterSamples(threadNo, metric):
        print("Filtering samples...")
        repetitionNo = 15 
        filePath = "SOAP(t)/" + str(threadNo) + "/" + metric
        timeFile = open("samples/" + filePath + "/time.txt", "r")
        year = 2020
        month = 9
        day = 16
        for rep in timeFile.readlines():
                timeRep = rep.split(" ")
                repetitionNo = timeRep[0]
                startTimeArray = timeRep[1].split(':')
                endTimeArray = timeRep[2].split(':')

                print("Filtering sample no " + str(repetitionNo))

                startTime = datetime.datetime(year,month,day,int(startTimeArray[0]),int(startTimeArray[1]),int(startTimeArray[2]))
                endTime = datetime.datetime(year,month,day,int(endTimeArray[0]),int(endTimeArray[1]),int(endTimeArray[2]))

                sample = open("samples/" + filePath + "/sample_" + repetitionNo + ".txt", "r")
                result = open("output/" + filePath + "/output_" + repetitionNo + ".txt", "w+")

                # metrics variables
                firstLine = 3
                # CPU = 8
                # disk = 10
                # mem = 8
                # net = 10
                metricPosition = 10

                lineCounter = 0
                numberOfSamples = 0
                sum = 0
                for line in sample.readlines():
                        firstCharacter = line[0]
                        if(lineCounter == 0 or lineCounter < firstLine or firstCharacter == 'A' or firstCharacter == '\n'):
                                lineCounter += 1
                                continue
                        if(metric == 'disk'):
                                dev = line[15:21]
                                if(dev != 'dev8-0'):
                                        lineCounter += 1
                                        continue
                        hour = int(line[0:2])
                        minute = int(line[3:5])
                        second = int(line[6:8])
                        sampleTime = datetime.datetime(year, month, day, hour, minute, second)
                        if sampleTime >= startTime and sampleTime <= endTime:
                                s = line.split()
                                s = s[metricPosition].replace(',', '.')
                                numberOfSamples += 1
                                sum += float(s)
                                result.write(s + ',')
                        lineCounter += 1
                sample.close()
                mean = sum/numberOfSamples
                result.write('\n' + str(mean))
                result.close()

filterSamples(100, 'disk')