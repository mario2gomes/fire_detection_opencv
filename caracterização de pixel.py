# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 18:37:19 2018

@author: mario
"""

#no posicionameto físico de um pixel a ordem é: x,y, na localização do pixel na matriz linha x coluna é y,x
import cv2
#captura.release()
captura = cv2.VideoCapture(0)

#imagem = cv2.imread('imagens/babuino.jpg')

while True:
    ret,frame = captura.read()
    frame = cv2.flip(frame,1)
    
 #   frame = imagem
    
    x_centro = int(frame.shape[1]/2)    #x central
    y_centro = int(frame.shape[0]/2)    #y central
    
    x = x_centro
    y= y_centro
    
    b,g,r = cv2.split(frame)
    
    azul = 'Azul: '+ str(b[y,x])
    vermelho = 'Vermelho: '+ str(r[y,x])
    verde = 'Verde: '+ str(g[y,x])
    
    '''
    azul = 'Azul: '+ str(frame[:,:,0][y,x])
    vermelho = 'Vermelho: '+ str(frame[:,:,2][y,x])
    verde = 'Verde: '+str(frame[:,:,1][y,x])
    '''
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    hue = 'Matiz: '+str(hsv[:,:,0][y,x])
    sat = 'Saturacao: '+str(hsv[:,:,1][y,x])
    value = 'intensidade: '+str(hsv[:,:,2][y,x])
    
    tamanhoFonte = 1
    espessura = 1
    
    cv2.circle(frame,(x,y),2,(0,255,255),espessura)
    cv2.rectangle(frame,(x-10,y-10),(x+10,y+10),(0,0,255),espessura)    
    
    
    cv2.putText(frame,azul,(x_centro+100,y_centro-100),cv2.FONT_HERSHEY_COMPLEX,tamanhoFonte,(255,0,0),espessura)
    cv2.putText(frame,verde,(x_centro+100,y_centro),cv2.FONT_HERSHEY_COMPLEX,tamanhoFonte,(0,255,0),espessura)
    cv2.putText(frame,vermelho,(x_centro+100,y_centro+100),cv2.FONT_HERSHEY_COMPLEX,tamanhoFonte,(0,0,255),espessura)
    cv2.putText(frame,hue,(x_centro-400,y_centro-100),cv2.FONT_HERSHEY_COMPLEX,tamanhoFonte,(0,255,255),espessura)
    cv2.putText(frame,sat,(x_centro-400,y_centro),cv2.FONT_HERSHEY_COMPLEX,tamanhoFonte,(255,0,255),espessura)
    cv2.putText(frame,value,(x_centro-400,y_centro+100),cv2.FONT_HERSHEY_COMPLEX,tamanhoFonte,(255,255,0),espessura)
    
    
    cv2.imshow('videooo',frame)

    if cv2.waitKey(1) == 13:      
        cv2.imwrite('frame final.jpg',frame)          
        break
    
#captura.release()
cv2.destroyAllWindows()