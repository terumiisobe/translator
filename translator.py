# ----------------------------------------------------------------------
# Script to translate sar and pidstat performace results into charts.
# ----------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np
import datetime
import sys

def returnGraphSpec(mix, metric):
        variables = {}
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
                        variables['ylim'] = 5
                if(mix == 'shopping'):
                        variables['ylim'] = 100

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
        metrics = ["CPU", "mem", "disk", "net"]
        for metric in metrics:
                print("Processing " + mix + " for metric " + metric + "...")
                meanA = []
                stdA = []
                meanB = []
                stdB = []
                for thread in threads:
                        filePathA = webserviceA + "/" + mix + "/" + str(thread) + "/" + metric
                        if comparison:
                                filePathB = webserviceB + "/" + mix + "/" + str(thread) + "/" + metric
                        repetitionNo = 15
                        values = []
                        # ---- processing samples for A
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
                        table.write("Número de threads, REST, SOAP, std(REST), std(SOAP)\n")
                        i = 0
                        for thread in threads:
                                table.write(str(thread) + "," + str(round(meanA[i], 3)) + "," + str(round(meanB[i], 3)) + "," + str(round(stdA[i], 3)) + "," + str(round(stdB[i], 3)) + "\n")
                                i = i+1
                        table.close()

                # ---- generating chart
                graphVaribles = returnGraphSpec(mix, metric)
                plt.suptitle(graphVaribles['title'])
                plt.ylabel(graphVaribles['ylabel'])
                plt.ylim(0, graphVaribles['ylim'])

                if(metric == "CPU"):
                        #plt.title("Porcentagem de utilização do CPU por número de threads")
                        #plt.ylabel("Utilização do CPU pela task (%)")
                        #plt.ylim(0, 55)
                        disX=2
                        disY=-2
                elif(metric == "disk"):
                        #plt.title("Porcentagem de tempo decorrido durante o qual as solicitações de I / O \n foram emitidas para o dispositivo \n (utilização de largura de banda para o dispositivo)")
                        #plt.ylabel("Utilização do tempo (%)")
                        #plt.ylim(0, 20)
                        disX=0
                        disY=1
                elif(metric == "mem"):
                        #plt.title("Porcentagem de memória utilizada por número de threads")
                        #plt.ylabel("Utilização de memória pela task (%)")
                        #plt.ylim(0, 14)
                        disX=0
                        disY=0.5
                elif(metric == "net"):
                        #plt.title("Porcentagem de utilização da interface de internet por número de threads")
                        #plt.ylabel("Utilização (%)")
                        #plt.ylim(0, 0.07)
                        disX=0.01
                        disY=-0
                plt.xlabel("Número de threads")
                plt.xlim(0, 120)
                plt.grid(linestyle=':')
                plt.errorbar(threads, meanA, stdA, linestyle='-', marker='^')
                plt.legend()

                #for a,b in zip(threads, meanA):
                #        plt.annotate(str(round(b, 2)), xy=(a+disX, b+disY))
                if comparison:
                        plt.errorbar(threads, meanB, stdB, linestyle='-', marker='^')
                        #for a,b in zip(threads, meanB):
                        #        plt.annotate(str(round(b, 2)), xy=(a-disX, b-disY))
                if comparison:
                        savePath = "graphs/comparison/" + mix + "/Comparison - " + mix + " - " + metric + ".png"
                else:
                        savePath = "graphs/" + webserviceA + "/" + mix + "/" + webserviceA + " - " + mix + " - " + metric + ".png"
                plt.show()
                ##plt.savefig(savePath)
                plt.clf()
                print("Chart plotted!")


# ---- CALLING FUNCTION ----#
generateChart(False, "REST(t)", "REST(t)", "shopping")