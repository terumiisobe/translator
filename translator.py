# ----------------------------------------------------------------------
# Script to translate sar and pidstat performace results into csv files.
# ----------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np
import datetime
import sys

def generateGraphic(metric, *args): # metric can be CPU, Mem, Net, Disk
        if(metric != "CPU" and metric != "mem" and metric != "net" and metric != "disk"):
                print("Metric not valid.")
                return
        
        threads = [20, 40, 60, 80, 100]
        mean = []
        std = []
        for threadNo in threads:
                # ---- PROCESSING EXP. REPETITION
                filePath = "SOAP(t)/" + str(threadNo) + "/" + metric
                repetitionNo = 15
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
        if(metric == 'CPU'):
                plt.title("Porcentagem de utilização do CPU por número de threads \n (SOAP(t) browsing mix)")
                plt.ylabel("Utilização do CPU pela task (%)")
                plt.ylim(0, 100)
        elif(metric == 'disk'):
                plt.title("Porcentagem de tempo decorrido durante o qual as solicitações de I / O \n foram emitidas para o dispositivo \n (utilização de largura de banda para o dispositivo)")
                plt.ylabel("Utilização do tempo (%)")
                plt.ylim(0, 20)
        elif(metric == 'mem'):
                plt.title("Porcentagem de memória utilizada por número de threads \n (SOAP(t) browsing mix)")
                plt.ylabel("Utilização de memória pela task (%)")
                plt.ylim(11.2, 13.1)
        elif(metric == 'net'):
                plt.title("Porcentagem de utilização da interface de internet por número de threads \n (SOAP(t) browsing mix)")
                plt.ylabel("Utilização (%)")
                plt.ylim(0, 0.07)
        plt.xlabel("Número de threads")
        plt.xlim(0, 100)
        plt.grid(linestyle=':')
        plt.errorbar(threads, mean, std, linestyle='-', marker='^')
        for a,b in zip(threads, mean):
                #plt.text(a, b, str(round(b, 2)))
                plt.annotate(str(round(b, 2)), xy=(a, b))
        plt.show()

# ---- CALLING FUNCTION ----#
generateGraphic("mem")


