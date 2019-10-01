# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 14:53:51 2019

@author: Alain
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage

#variables à changer :

image = 'ecoli.jpg' #nom de l'image du dossier courant
margecrop0=10 #crop avant et après dans l'axeO 
margecrop1=10 #crop avant et après dans l'axe1
seuil=190 #quel seuil de détection des bactéries/rapport au fond
tmin=30 #taille au dessous de laquelle on considère qu'une bactérie n'en est pas une
#laisser a 0 avant interprétation de l'histogramme final.



image3=plt.imread(image)
plt.imshow(image3)
plt.show()

print(image3.shape)

#on passe de 3 dimensions à 2 dimensions:
image=image3[:,:,0]
plt.imshow(image)
plt.show()
print(image.shape)


#affichage de l'histogramme
image_2=np.copy(image)
plt.hist(image_2.ravel(),bins=255)
plt.show()


#crop de l'image qui présente des bandes périphériques en hyper et hyposignal
calcaxeO=image.shape[0]-margecrop0
calcaxe1=image.shape[1]-margecrop1
image_c=image_2[margecrop0:calcaxeO,margecrop1:calcaxe1]



#boolean indexing : selection des zones qui nous interessent 

image_bool=image_c<seuil
plt.imshow(image_bool) #affiche le calque bool qui sort les bactéries du fond

plt.show()

#mais il y a quelques artefacts que l'on va supprimer à l'aide des morphologies

open_x=ndimage.binary_opening(image_bool) #filtrage utilisant la morphologie dilation+erosion
plt.imshow(open_x)
plt.show()

#nomage des bactéries : 

label_image,n_labels=ndimage.label(open_x)
print("nombre de bactéries : ",n_labels)
plt.imshow(label_image)
plt.show()


# mesure et affichage de la taille apparente des bactéries :

sizes=ndimage.sum(open_x,label_image, range(n_labels))
plt.scatter(range(n_labels),sizes)
plt.show()

#ce qui permet de tracer cet histogramme : 
plt.hist(sizes,bins=255)

plt.show()
# cet histogramme montre des bactéries de trailles diverses, et on peut choisir une valeur
# au dessous de laquelle on considère que ce n'est plus une bactérie (t_min)

print("nombre de bactéries retenues au final : ",np.sum(sizes>tmin))

