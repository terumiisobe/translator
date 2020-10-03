# ----------------------------------------------------------------------
# Script to translate sar and pidstat performace results into csv files.
# ----------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np
import datetime
import sys

def generateGraphic(metric, *args): # metric can be CPU, Mem, Net, Disk
        if(metric != "CPU" and metric != "Mem" and metric != "Net" and metric != "Disk"):
                print("Metric not valid.")
                return
        
        threads = [20]
        mean = []
        std = []
        for threadNo in threads:
                # ---- PROCESSING EXP. REPETITION
                filePath = "SOAP-transactional/" + str(threadNo) + "/" + metric
                repetitionNo = 3 #TODO: change to 15
                print("Processing samples for " + str(threadNo) + " threads...")
                values = []
                for n in range(repetitionNo):
                        print("Processing sample no " + str(n + 1))
                        result = open("output/" + filePath + "/output_" + str(n + 1) + ".txt", "r")
                        lines = result.readlines()
                        values.append(float(lines[1]))
                        result.close()
                mean.append(np.mean(values))
                std.append(np.std(values))
        plt.errorbar(threads, mean, std, linestyle='None', marker='^')
        plt.show()

# ---- CALLING FUNCTION ----#
generateGraphic(sys.argv[1])


