# -*- coding: utf-8 -*-
"""
Created on Tue May  8 16:39:56 2018

@author: mario
"""
import winsound as som
import numpy as np
import cv2
#captura.release()

captura = cv2.VideoCapture(0)

imagem = cv2.imread('imagens/luzes.jpg')
som.Beep(1000,10000)

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

    areas1 = np.zeros([1,len(contornos)])
    areas0 = np.zeros([1,len(contornos)])
    #print('tamanho do contorno: ', len(contornos))
    if (len(contornos)>0):
        for i in range(len(contornos)):            
            #print ('area1: ', areas1)
            #print ('area0: ', areas0)
            #print(i)
            M = cv2.moments(contornos[i])                                   
            if (M['m00'] > 20):
                #print('entrou no if do for')
                x = int(M['m10']/M['m00'])	#cordenada x do centroide
                y = int(M['m01']/M['m00']) #cordenada y do centroide
                cv2.circle(frame,(x,y),2,(0,255,255),espessura)
                cv2.rectangle(frame,(x-10,y-10),(x+10,y+10),(0,0,255),espessura)
                area = cv2.contourArea(contornos[i])
                #print('area: ', area)
                areas1[0,i] = area
            else:
                areas1[0,i] = 0
            
            if (i == 0):
                diferencas_areas = areas0
            else:
                diferencas_areas = areas1 - areas0
                
            #print ('diferencas: ', diferencas_areas)
            
            for i in range(len(diferencas_areas)):
                if (diferencas_areas[0,i] > 0):
                    print ('diferenca: ',diferenca_areas)
                    print ('areas0',areas0)
                    print ('areas1',areas1)
                    print ("fogo no contorno: ", i)
                    som.Beep(1000,10000)
                
            areas0 = areas1
            
            
            
    #cv2.putText(frame,fogo,(x_centro-400,y_centro-100),cv2.FONT_HERSHEY_COMPLEX,tamanhoFonte,(0,255,255),espessura)
    cv2.imshow('original',frame)
    
#para de filmar ao pressionar a tecla "enter"
    if cv2.waitKey(1) == 13:
        print('ddd')
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
