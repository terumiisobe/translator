# ----------------------------------------------------------------------
# Script to filter sar and pidstat txt outputs. Filters all 15 
# repetitions of the experiment.
# ----------------------------------------------------------------------
import datetime

def filterSamples(webservice, mix):
        threads = [20, 40, 60, 80, 100]
        for thread in threads:
                metrics = ['CPU', 'mem', 'disk', 'net']
                for metric in metrics:
                        print("Filtering samples for " + webservice + " metric " + metric + " ...");
                        print("> Thread number " + str(thread))
                        repetitionNo = 15 
                        filePath = webservice + "/" + mix + "/" + str(thread) + "/" + metric
                        timeFile = open("samples/" + webservice + "/" + mix + "/" + str(thread) + "/time.txt", "r")
                        year = 2020
                        month = 9
                        day = 16
                        for rep in timeFile.readlines():
                                timeRep = rep.split(" ")
                                repetitionNo = timeRep[0]
                                startTimeArray = timeRep[1].split(':')
                                endTimeArray = timeRep[2].split(':')

                                print("--> Sample " + str(repetitionNo))

                                startTime = datetime.datetime(year,month,day,int(startTimeArray[0]),int(startTimeArray[1]),int(startTimeArray[2]))
                                endTime = datetime.datetime(year,month,day,int(endTimeArray[0]),int(endTimeArray[1]),int(endTimeArray[2]))

                                sample = open("samples/" + filePath + "/sample_" + repetitionNo + ".txt", "r")
                                result = open("output/" + filePath + "/output_" + repetitionNo + ".txt", "w+")

                                # metrics variables
                                firstLine = 3
                                if(metric == 'CPU' or metric == 'mem'):
                                        metricPosition = 8
                                elif(metric == 'net'):
                                        metricPosition = 10
                                elif(metric == 'disk'):
                                        metricPosition = 3

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
                                                if((mix == 'browsing' and dev != 'dev8-0') or (mix == 'shopping' and dev != 'v253-0')):
                                                        lineCounter += 1
                                                        continue
                                        if(metric == 'net'):
                                                iface = line[15:21]
                                                if(iface != 'enp0s3'):
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

filterSamples('SOAP(t)', 'browsing')
# parameters:
# - webservice = 
#       -SOAP(t)
#       -REST(t)
# - mix = 
#       -browsing
#       -shopping