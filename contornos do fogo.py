# -*- coding: utf-8 -*-
"""
Created on Tue May  8 16:39:56 2018

@author: mario
"""
import time
import winsound as som
import numpy as np
import cv2
#captura.release()

captura = cv2.VideoCapture(0)

#imagem = cv2.imread('imagens/luzes.jpg')
inicio = 0
areas1 = np.empty

while True:
    ret,frame = captura.read()
    frame = cv2.flip(frame,1)
    #frame = cv2.pyrDown(imagem)
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)    
        
    ret,binaria = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    bordas = cv2.Canny(binaria,20, 170)
    
    cv2.imshow('canny', bordas)
    
    contornos, hierarquia = cv2.findContours(bordas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contornos = sorted(contornos, key=cv2.contourArea, reverse=True)
    tamanhoFonte = 1
    espessura = 1

    #Array vazio com as N(quantidade de contornos) tuplas: (x do centro, y do centro, área) em relação ao contorno
    areas0 = np.zeros([1,len(contornos),4])
    area_comparacao = np.zeros([1,len(contornos),4])

    #Verifica se algum contorno foi encontrado
    if (len(contornos)>0):
        #loop em cada contorno
        for i in range(len(contornos)):
            
            M = cv2.moments(contornos[i])
            #escolhe contornos com área maior que 20 pixels
            if (M['m00'] > 20):
                x,y = int(M['m10']/M['m00'])	, int(M['m01']/M['m00']) #cordenada x do centroide e cordenada y do centroide

                #desenha um círculo e um quadrado no centro do contorno
                cv2.circle(frame,(x,y),2,(0,255,255),espessura)
                cv2.rectangle(frame,(x-10,y-10),(x+10,y+10),(0,0,255),espessura)

                #area do contorno
                area = cv2.contourArea(contornos[i])
                areas0[0,i] = contornos[i],x,y,area

#VERIFICAR SE DÁ PRA COMPARAR O MATCH DOS CONTORNOS AO INVES DOS CENTROIDES    
    if (inicio!=0):
        for i in range(len(areas0)):
            for j in areas1:
                if (areas1[0,j,1]>(areas0[0,i,1]-10) &
                    areas1[0,j,1]<(areas0[0,i,1]+10) &
                    areas1[0,j,2]>(areas0[0,i,2]-10) & 
                    areas1[0,j,2]<(areas0[0,i,2]+10)):
                    area_comparacao[0,i] = areas0[0,i]
                    area_comparacao[0,i,3] = areas1[0,j,3] - areas0[0,i,3]
    else:
        inicio = 1    
    
    for i in range(len(area_comparacao)):
        #se houver um aumento (maior que 20 pixels) na área de algum contorno
        if (area_comparacao[0,i,3]>20):
            M = cv2.moments(area_comparacao[0,i,0])
            x,y = int(M['m10']/M['m00'])	, int(M['m01']/M['m00']) #cordenadas x e y do centroide

            #desenha um círculo e um quadrado no centro do contorno
            cv2.circle(frame,(x,y),2,(255,255,0),espessura+2)
            cv2.rectangle(frame,(x-10,y-10),(x+10,y+10),(255,0,255),espessura+2)
            cv2.putText(frame,'fogo',(x-400,y-100),cv2.FONT_HERSHEY_COMPLEX,tamanhoFonte,(0,255,255),espessura)
            som.Beep(1000,10000)
            
    #Cópia de areas0 pra comparar as áreas e os centroides em momentos diferentes
    areas1 = np.copy(areas0)
    time.sleep(1000)

#FAZER AQUI COMPARAÇÃO ENTRE AS ÁREAS
                #ESCOLHER ENTRE AS OPÇÕES:
                    #COMPARAR DENTRO DO ARRAY, COM WHERE'S
                    #COMPARAR OS CENTROS CONTORNO A CONTORNO E QUANDO DER MATCH COMPARAR AS ÁREAS (USANDO UM FOR)
                    #ORDENAR OS CONTORNOS DE ACORDO COM A POSIÇÃO DO CENTROIDE E COMPARAR OS DE ACORDO COM A ORDEM
    
    cv2.imshow('original',frame)
    
#para de filmar ao pressionar a tecla "enter"
    if cv2.waitKey(1) == 13:
        cv2.imwrite('frame final bordas.jpg',bordas)
        cv2.imwrite('frame final.jpg',frame)
        break
    
captura.release()
cv2.destroyAllWindows()

#print (areas1)
#print (areas0)


'''
if (len(areas0) > 0):                   
   if ((areas1[i]-areas0[i])>100):
       print ('area: ',area)
       
       cv2.circle(frame,(x,y),2,(0,255,255),espessura+1)
       cv2.rectangle(frame,(x-10,y-10),(x+10,y+10),(0,0,255),espessura+1)
       cv2.putText(frame,'FOGO',(x,y),cv2.FONT_HERSHEY_COMPLEX,tamanhoFonte,(0,255,255),espessura)'''
#cv2.imshow('imagem binaria: ', binaria)
#cv2.imshow('bordas: ', bordas)
