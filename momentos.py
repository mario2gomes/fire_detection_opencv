# -*- coding: utf-8 -*-
"""
Created on Wed May  9 19:29:24 2018

@author: mario
"""

import cv2
import numpy as np
import pandas as pd

imagem = cv2.pyrDown(cv2.imread('./imagens/formas.jpg'))
imagemoriginal = cv2.pyrDown(cv2.imread('./imagens/formasgirada.jpg'))

def mom(imagem):
    gray = cv2.cvtColor(imagem,cv2.COLOR_BGR2GRAY)
    ret,binaria = cv2.threshold(gray,200,255,cv2.THRESH_BINARY_INV)
    borda = cv2.Canny(binaria, 20,170)
    
    kernel = np.ones((3,3), np.uint8)
    borda = cv2.dilate(borda, kernel, iterations = 1)      
    
    cv2.imshow('borda',borda)
    cv2.waitKey(0)

    
    #contornada,
    contorno, hierarquia = cv2.findContours(borda, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    ordenada = sorted(contorno, key=cv2.contourArea, reverse=False)
    ordenado = [k for k in ordenada if cv2.contourArea(k)>100]
    #filter(lambda k: 9.0 in k, ordenada)
    
    #(cv2.contourArea(k))>400 in k
    contorno = cv2.drawContours(imagem, ordenado, -1, (0,255,0), 3)
    
    #for i in range(len(ordenada)):
    #    print (cv2.contourArea(ordenada[i]))    
    av = list()
    for i in range(len(ordenado)):
        area = cv2.contourArea(ordenado[i])
        av.append(area)
    
    cv2.imshow('original',imagem)
    cv2.waitKey(0)    
    momentos = np.empty([1,7])    
    Ms = list()
    cv2.destroyAllWindows()

    for i in range(len(ordenado)):
        momento = list()
        M = cv2.moments(ordenado[i])
        momento.append(M['nu20'] + M['nu02'])
        momento.append((M['nu20'] - M['nu02'])**2 + 4*M['nu11']**2)
        momento.append((M['nu30'] - 3*M['nu12'])**2 + (3*M['nu21'] - M['nu03'])**2)
        momento.append((M['nu30'] + 3*M['nu12'])**2 + (M['nu21'] + M['nu03'])**2)
        momento.append((M['nu30'] - 3*M['nu12'])*(M['nu30'] + M['nu12']) *
                       (((M['nu30'] + M['nu12'])**2) - 3*((M['nu21'] + M['nu03'] )**2)) + 
                       (3*M['nu21'] - M['nu03']) * (M['nu21'] + M['nu03']) *
                       (3*((M['nu30'] + M['nu12'])**2) - (M['nu21'] + M['nu03'])**2))
        momento.append((M['nu20'] - M['nu02']) * ((M['nu30'] + M['nu12'])**2 - (M['nu21'] + 
                        M['nu03'])**2) + 4*M['nu11']*(M['nu30'] + M['nu12']) * (M['nu21'] + M['m03']))
        momento.append((3*M['nu21'] - M['nu03'])*(M['nu30'] + M['nu12']) *
                       (((M['nu30'] + M['nu12'])**2) - 3*((M['nu21'] + M['nu03'])**2)) + 
                       (3*M['nu12'] - M['nu03']) * (M['nu21'] + M['nu03']) *
                       (3*((M['nu30'] + M['nu12'])**2) - (M['nu21'] + M['nu03'])**2))
        if (i==0):
            momentos[i] = momento
        else:
            momentos = np.insert(momentos,len(momentos),np.array(momento),axis=0)
        Ms.append(M)
#        print ('contorno ',i,' :')
#        for j in range(len(momento)):
#            print ('momento ',j+1,' : %.20f' %momentos[i+1][j])
    return av,Ms,momentos
    
av1,Ms1,momento1 = mom(imagem)
momento_df_alterado = pd.DataFrame(momento1)
momento_dicionario_df_alterado = pd.DataFrame(Ms1)
momento_df_alterado.to_excel('./tabelas/momentos alterado.xlsx')
momento_dicionario_df_alterado.to_excel('./tabelas/dicio momentos alterado.xlsx')

av0,Ms0,momento0 = mom(imagemoriginal)
momento_df = pd.DataFrame(momento0)
momento_dicionario_df = pd.DataFrame(Ms0)
momento_df.to_excel('./tabelas/momentos original.xlsx')
momento_dicionario_df.to_excel('./tabelas/dicio momentos original .xlsx')

compara_momentos = momento_df/momento_df_alterado
compara_momentos.to_excel('./tabelas/comparando momentos(formula doida).xlsx')

compara_momentos_dicio = momento_dicionario_df/momento_dicionario_df_alterado
compara_momentos_dicio.to_excel('./tabelas/comparando momentos(dicionario).xlsx')

'''
def mul(n):
    return 1000000*n

momentos = momento1 - momento0

for i in range(len(momentos)):
        print ("Momento ",i+1,": %.20f" % mul(momentos[i]))

def dicio(M):
    print ('m00: %.20f' % M['m00'])
    print ('m10: %.20f' % M['m10'])
    print ('m01: %.20f' %M['m01'])
    print ('m20: %.20f' %M['m20'])
    print ('m11: %.20f' %M['m11'])
    print ('m02: %.20f' %M['m02'])
    print ('m30: %.20f' %M['m30'])
    print ('m21: %.20f' %M['m21'])
    print ('m12: %.20f' %M['m12'])
    print ('m03: %.20f' %M['m03'])
    print ('mu20: %.20f' %M['mu20'])
    print ('mu11: %.20f' %M['mu11'])
    print ('mu02: %.20f' %M['mu02'])
    print ('mu30: %.20f' %M['mu30'])
    print ('mu21: %.20f' %M['mu21'])
    print ('mu12: %.20f' %M['mu12'])
    print ('mu03: %.20f' %M['mu03'])
    print ('nu20: %.20f' %M['nu20'])
    print ('nu11: %.20f' %M['nu11'])
    print ('nu02: %.20f' %M['nu02'])
    print ('nu30: %.20f' %M['nu30'])
    print ('nu21: %.20f' %M['nu21'])
    print ('nu12: %.20f' %M['nu12'])
    print ('nu03: %.20f' %M['nu03'])
    
print('momentos para figura original:>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
for i in range(len(Ms0)):
    print('momentos ',i+1,':>>>>>>>>>>>>>>>>>>>>>')
    dicio(Ms0[i])
print('momentos para figura alterada:>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
for i in range(len(Ms1)):
    print('momentos ',i+1,':>>>>>>>>>>>>>>>>>>>>>')
    dicio(Ms1[i])

for i in range(len(momento1)):
        print ("Momento 1",i+1,": %.20f" % momento1[i])

for i in range(len(momento0)):
        print ("Momento 0",i+1,": %.20f" % momento0[i])
'''