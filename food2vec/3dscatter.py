import os
import pickle
import tensorflow as tf
import tensorflow.keras as k
from tensorflow.keras import layers, models
import numpy as np
from tqdm import tqdm

from sklearn.manifold import TSNE
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
import matplotlib

from make_tfr import FoodTFrecord
from dataloader import FoodDataLoader_with_TFRecord
from make_tfr import FoodTFrecord

with open("extracted_vector.pkl", "rb") as f:
    extracted_vector_re = pickle.load(f)
    
with open("food2vec_data.pkl", "rb") as f:
    food2vec_data_re = pickle.load(f)
    
Y = [i/30.0 for i in food2vec_data_re[1]]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# x = extracted_vector_re[:,0]
# y = extracted_vector_re[:,1]
# z = extracted_vector_re[:,2]
# ax.scatter(x, y, z, c= Y)
# ax.text(x, y, z, '%s' % (str(food2vec_data_re[1])), size=20)

for i in tqdm(range(len(extracted_vector_re))): #plot each point + it's index as text above
    ax.scatter(extracted_vector_re[i,0],extracted_vector_re[i,1],extracted_vector_re[i,2]) 
    ax.text(extracted_vector_re[i,0],extracted_vector_re[i,1],extracted_vector_re[i,2], '%s' % (str(food2vec_data_re[1][i])), size=20)
    


plt.show()
