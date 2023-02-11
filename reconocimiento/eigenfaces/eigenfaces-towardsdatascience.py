# https://towardsdatascience.com/eigenfaces-face-classification-in-python-7b8d2af3d3ea
# de Dario Radečić

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.metrics import confusion_matrix, classification_report

# para callar sklearn, que avisa cuando se dan divisiones por cero
import warnings
warnings.filterwarnings('ignore')

# el dataset es un csv 
#    columnas: pixeles normalizados: entre 0 y 1. 4097 features porque cada imagen tiene 64x64 pixeles + la columna del individuo
df = pd.read_csv('Python-Eigenfaces-master/face_data.csv')
# 40 elementos unicos en la columna "target", 40 individuos en las 400 filas (una por foto)
# print(df.head())
# print(df.shape)
# print(df['target'].unique())

# VISUALIZACIÓN
# funcion para pintar imagen con las caras. Pasa vector 1d (fila) a matriz 2d (bitmap) y lo pinta como imagen
def plot_faces(pixels):
    fig, axes = plt.subplots(5, 5, figsize=(6, 6))
    for i, ax in enumerate(axes.flat):
        ax.imshow(np.array(pixels)[i].reshape(64, 64), cmap='gray')
    plt.show()

# separa la columna que identifica al individuo para entrenar con una matrix 64x64
X = df.drop('target', axis=1)
y = df['target']

plot_faces(X)

# PRINCIPAL COMPONENT ANALYSIS
# antes de pcs hace falta cortar el dataset en porciones de entrenamiento y puesta a prueba
X_train, X_test, y_train, y_test = train_test_split(X, y)

# pca reduce las dimensiones, se queda con los valores que tienen mas variación
pca = PCA().fit(X_train)

# solo para confirmar, pintar el grafico enseña que a partir de 100 hay una meseta
# pinta la CUSUM "suma cumulativa" se usa para monitorizar y detectar cambios 
plt.figure(figsize=(18, 7))
plt.plot(pca.explained_variance_ratio_.cumsum(), lw=3)
plt.show()
# a partir de 105, la variación es pequeña
print(np.where(pca.explained_variance_ratio_.cumsum() > 0.95))

# vuelve a ejecutar el PCA pero con menos componentes
pca = PCA(n_components=105).fit(X_train)

X_train_pca = pca.transform(X_train)

# ENTRENAMIENTO Y EVALUACIÓN
# Entrena el modelo (Support Vector Machine), le basta con hacer una instancia y alimentarle los datos
classifier = SVC().fit(X_train_pca, y_train)

# hay que hacerle lo mismo a los datos de pruebas que de entrenamiento "pasarlos al mismo 'feature space'"
X_test_pca = pca.transform(X_test)
predictions = classifier.predict(X_test_pca)
print(classification_report(y_test, predictions))

