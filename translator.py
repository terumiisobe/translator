# ----------------------------------------------------------------------
# Script to translate sar and pidstat performace results into charts.
# ----------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np
import datetime
import sys

def returnGraphSpec(mix, metric):
        variables = {}
        
        if(metric == 'time'):
                variables['title']= "Tempo médio de execução do experimento (mix)"
                variables['ylabel'] = "Segundos"
                variables['ylim'] = 110

        if(metric == 'CPU'):
                variables['title'] = "Porcentagem de utilização do CPU por número de threads"
                variables['ylabel'] = "Utilização do CPU pela task (%)"
                if(mix == 'browsing'):
                        variables['ylim'] = 55
                if(mix == 'shopping'):
                        variables['ylim'] = 55
    
        elif(metric == 'disk'):
                variables['title']= "Número total de transferências (requisições I/O) por segundo"
                variables['ylabel'] = "Número de transferências"
                if(mix == 'browsing'):
                        variables['ylim'] = 55
                if(mix == 'shopping'):
                        variables['ylim'] = 55

        elif(metric == 'mem'):
                variables['title']= "Porcentagem de memória utilizada por número de threads"
                variables['ylabel'] = "Utilização de memória pela task (%)"
                if(mix == 'browsing'):
                        variables['ylim'] = 14
                if(mix == 'shopping'):
                        variables['ylim'] = 14

        elif(metric == 'net'):
                variables['title']= "Porcentagem de utilização da interface de internet por número de threads"
                variables['ylabel'] = "Utilização (%)"
                if(mix == 'browsing'):
                        variables['ylim'] = 0.07
                if(mix == 'shopping'):
                        variables['ylim'] = 0.07

        return variables

def generateChart(comparison, webserviceA, webserviceB,  mix): 
        threads = [20, 40, 60, 80, 100]
        metrics = ["CPU", "mem", "disk", "net", "time"]
        for metric in metrics:
                print("Processing " + mix + " for metric " + metric + "...")
                meanA = []
                stdA = []
                meanB = []
                stdB = []
                for thread in threads:
                        filePathA = webserviceA + "/" + mix + "/" + str(thread) 
                        if(metric != 'time'):
                                filePathA = filePathA + "/" + metric
                        if comparison:
                                filePathB = webserviceB + "/" + mix + "/" + str(thread)
                                if(metric != 'time'):
                                        filePathB = filePathB + "/" + metric
                        repetitionNo = 15
                        values = []
                        # ---- processing samples for A
                        if(metric == 'time'):
                                result = open("samples/" + filePathA + "/avgTime.txt", "r")
                                lines = result.readlines()
                                values = lines[0].split(',')
                                meanA.append(float(values[0]))
                                stdA.append(float(values[1]))
                                result.close()
                        else:
                                for n in range(repetitionNo):
                                        result = open("output/" + filePathA + "/output_" + str(n + 1) + ".txt", "r")
                                        lines = result.readlines()
                                        values.append(float(lines[1]))
                                        result.close()
                                # ---- adding mean and standand deviation to A chart arrays 
                                meanA.append(np.mean(values))
                                stdA.append(np.std(values))
                        if not comparison:
                                continue
                        values = []
                        # ---- processing samples for B
                        if(metric == 'time'):
                                result = open("samples/" + filePathB + "/avgTime.txt", "r")
                                lines = result.readlines()
                                values = lines[0].split(',')
                                meanB.append(float(values[0]))
                                stdB.append(float(values[1]))
                                result.close()
                        else:
                                for n in range(repetitionNo):
                                        result = open("output/" + filePathB + "/output_" + str(n + 1) + ".txt", "r")
                                        lines = result.readlines()
                                        values.append(float(lines[1]))
                                        result.close()
                                # ---- adding mean and standand deviation to A chart arrays 
                                meanB.append(np.mean(values))
                                stdB.append(np.std(values))

                # ---- creates graph tables
                if comparison:
                        table = open("graphs/comparison/" + mix + "/Comparison - " + mix + " - " + metric + "(table).txt", "w+")
                        table.write("Número de threads," + webserviceA + "," + webserviceB + ",std(" + webserviceA + "),std(" + webserviceB + ")\n")
                        i = 0
                        for thread in threads:
                                #if(metric == 'time'):
                                #        table.write(str(thread) + "," + str(meanB[i]) + "," + str(meanA[i]) + "," + str(stdB[i]) + "," + str(stdA[i]) + "\n")
                                #else:
                                table.write(str(thread) + "," + str(round(meanA[i], 3)) + "," + str(round(meanB[i], 3)) + "," + str(round(stdA[i], 3)) + "," + str(round(stdB[i], 3)) + "\n")
                                i = i+1
                        table.close()

                # ---- generating chart
                graphVaribles = returnGraphSpec(mix, metric)
                plt.suptitle(graphVaribles['title'])
                plt.ylabel(graphVaribles['ylabel'])
                plt.ylim(0, graphVaribles['ylim'])

                plt.xlabel("Número de threads")
                plt.xlim(0, 120)
                plt.grid(linestyle=':')
                plt.errorbar(threads, meanA, stdA, linestyle='-', marker='^')
                plt.legend()

                if comparison:
                        plt.errorbar(threads, meanB, stdB, linestyle='-', marker='^')
                if comparison:
                        savePath = "graphs/comparison/" + mix + "/Comparison - " + mix + " - " + metric + ".png"
                else:
                        savePath = "graphs/" + webserviceA + "/" + mix + "/" + webserviceA + " - " + mix + " - " + metric + ".png"
                plt.show()
                plt.clf()
                print("Chart plotted!")


# ---- CALLING FUNCTION ----#
generateChart(True, "SOAP(t)", "REST(t)", "browsing")