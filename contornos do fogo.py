# -*- coding: utf-8 -*-
"""
Created on Tue May  8 16:39:56 2018

@author: mario
"""
import time
import winsound as som
import pandas as pd
import cv2
#captura.release()

captura = cv2.VideoCapture(0)

#imagem = cv2.imread('imagens/luzes.jpg')
inicio = 0
fogo =0
areas0 = pd.DataFrame(columns=['contorno','area','x','y'])
areas1 = pd.DataFrame(columns=['contorno','area','x','y'])
area_comparacao = pd.DataFrame(columns=['contorno','area','x','y'])

while True:

    areas0 = areas0.drop(areas0.index)
    area_comparacao = area_comparacao.drop(area_comparacao.index)

    ret,clip = captura.read()
    clip = cv2.flip(clip,1)
    
    #clip = cv2.pyrDown(imagem)
    gray = cv2.cvtColor(clip,cv2.COLOR_BGR2GRAY)    
        
    ret,binaria = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    bordas = cv2.Canny(binaria,20, 170)    

    contornos, hierarquia = cv2.findContours(bordas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contornos = sorted(contornos, key=cv2.contourArea, reverse=True)
    tamanhoFonte = 1
    espessura = 1

    #Verifica se algum contorno foi encontrado
    if (len(contornos)>0):
        #loop em cada contorno
        for i in range(len(contornos)):            
            
            M = cv2.moments(contornos[i])
            #escolhe contornos com área maior que 20 pixels
            if (M['m00'] > 20):
                
                x,y = int(M['m10']/M['m00'])	, int(M['m01']/M['m00']) #cordenada x do centroide e cordenada y do centroide

                #desenha um círculo e um quadrado no centro do contorno
                cv2.circle(binaria,(x,y),2,(0,255,255),espessura)
                cv2.rectangle(binaria,(x-10,y-10),(x+10,y+10),(0,0,255),espessura)

                #area do contorno
                area = cv2.contourArea(contornos[i])
                
                areas0 = areas0.append({'contorno':contornos[i],
                                        'area':area,
                                        'x':x,'y':y
                                        },ignore_index=True)

#VERIFICAR SE DÁ PRA COMPARAR O MATCH DOS CONTORNOS AO INVES DOS CENTROIDES    
    
    if (inicio!=0):
        
        print ('111 areas0: ',areas0)
        print 'areas1: ',areas1
                    
        if (len(areas0)!=0):
            for i in range(len(areas0)):
                for j in range(len(areas1)):

                    print "x de areas 1: ", areas1['x'][j]
                    print "x de areas 0: ", areas0['x'][i]
                    print "y de areas 1: ", areas1['y'][j]
                    print "y de areas 0: ", areas0['y'][i]
                    
                    if (areas1['x'][j]>(areas0['x'][i]-10) and
                        areas1['x'][j]<(areas0['x'][i]+10) and
                        areas1['y'][j]>(areas0['y'][i]-10) and
                        areas1['y'][j]<(areas0['y'][i]+10)):
                        
                        area_comparacao = area_comparacao.append({'contorno':areas0['contorno'][i],
                                        'area':(areas1['area'][j] - areas0['area'][i]),
                                        'x':areas0['x'][i],'y':areas0['y'][i]
                                        },ignore_index=True)
                            
    else:
        inicio = 1

    if (len(area_comparacao)!=0):

        for i in range(len(area_comparacao['contorno'])):
            #se houver um aumento (maior que 20 pixels) na área de algum contorno
            print ('area das diferenca',area_comparacao['area'][i])
            
            if (area_comparacao['area'][i]>10):
                print ('9 - iferenca maior que 10')
                
                fogo = fogo+1
                
                M = cv2.moments(area_comparacao['contorno'][i])
                x,y = int(M['m10']/M['m00'])	, int(M['m01']/M['m00']) #cordenadas x e y do centroide
    
                #desenha um círculo e um quadrado no centro do contorno
                cv2.circle(binaria,(x,y),2,(255,255,0),espessura+2)
                cv2.rectangle(binaria,(x-10,y-10),(x+10,y+10),(255,0,255),espessura+2)
                cv2.putText(binaria,'fogo',(x-400,y-100),cv2.FONT_HERSHEY_COMPLEX,tamanhoFonte,(0,255,255),espessura)
                som.Beep(1000,10000)

    #print ('area0: ',areas0)
    #print ('area1: ',areas1)
    #Cópia de areas0 pra comparar as áreas e os centroides em momentos diferentes
    areas1 = areas0.copy()

#FAZER AQUI COMPARAÇÃO ENTRE AS ÁREAS
                #ESCOLHER ENTRE AS OPÇÕES:
                    #COMPARAR DENTRO DO ARRAY, COM WHERE'S
                    #COMPARAR OS CENTROS CONTORNO A CONTORNO E QUANDO DER MATCH COMPARAR AS ÁREAS (USANDO UM FOR)
                    #ORDENAR OS CONTORNOS DE ACORDO COM A POSIÇÃO DO CENTROIDE E COMPARAR OS DE ACORDO COM A ORDEM
    
    cv2.imshow('original',binaria)
    #time.sleep(5)

#para de filmar ao pressionar a tecla "enter"
    if cv2.waitKey(1) == 13:
        cv2.imwrite('clip final bordas.jpg',bordas)
        cv2.imwrite('clip final.jpg',clip)
        break
    
captura.release()
cv2.destroyAllWindows()

#print (areas1)
#print (areas0)


'''
if (len(areas0) > 0):                   
   if ((areas1[i]-areas0[i])>100):
       print ('area: ',area)
       
       cv2.circle(clip,(x,y),2,(0,255,255),espessura+1)
       cv2.rectangle(clip,(x-10,y-10),(x+10,y+10),(0,0,255),espessura+1)
       cv2.putText(clip,'FOGO',(x,y),cv2.FONT_HERSHEY_COMPLEX,tamanhoFonte,(0,255,255),espessura)'''
#cv2.imshow('imagem binaria: ', binaria)
#cv2.imshow('bordas: ', bordas)
