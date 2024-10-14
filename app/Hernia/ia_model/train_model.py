import os
import numpy as np
import cv2
from skimage.feature import hog
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pickle

# Definir dimensiones de las imágenes
width = 300
height = 300

# Ruta a los datos de entrenamiento
ruta_train = 'app/Hernia/ia_model/data/train'

# Ruta para guardar el modelo y las etiquetas
model_path = 'app/Hernia/ia_model/mimodelo.pkl'
labels_path = 'app/Hernia/ia_model/labels.pkl'

# Función para extraer características
def extract_features(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    features, _ = hog(gray_image, visualize=True, block_norm='L2-Hys')
    return features

# Inicializar listas de características y etiquetas
train_x = []
train_y = []

# Obtener etiquetas
print("Obteniendo etiquetas de las clases...")
labels = os.listdir(ruta_train)
print(f"Etiquetas encontradas: {labels}")

# Limitar el número de imágenes a procesar por clase
max_images_to_process = 13

print("Comenzando el procesamiento de imágenes...")

# Procesar imágenes y extraer características
for i in labels:
    images_processed = 0
    print(f"Procesando imágenes para la clase: {i}...")
    for j in os.listdir(os.path.join(ruta_train, i)):
        if images_processed >= max_images_to_process:
            break
        img_path = os.path.join(ruta_train, i, j)
        img = cv2.imread(img_path)
        resized_image = cv2.resize(img, (width, height))
        features = extract_features(resized_image)
        train_x.append(features)
        train_y.append(i)
        images_processed += 1
        print(f"Procesando {j} de la clase {i}...")

print("Procesamiento de imágenes completado.")

# Convertir a arrays numpy
x_data = np.array(train_x)
y_data = np.array(train_y)

# Mostrar las clases y el número de imágenes por clase
print("\nClases encontradas y número de imágenes por clase:")
for label in labels:
    print(f"{label}: {np.sum(y_data == label)} imágenes")

# Verificar si hay más de una clase
if len(np.unique(y_data)) < 2:
    raise ValueError("El número de clases tiene que ser mayor que una. Por favor, asegúrate de que el conjunto de datos contenga imágenes de al menos dos clases diferentes.")

# Dividir datos en entrenamiento y prueba
print("\nDividiendo datos en entrenamiento y prueba...")
x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.2, random_state=42)
print("División completada.")

# Definir modelo con pipeline
print("\nDefiniendo el modelo...")
model = Pipeline([
    ('scaler', StandardScaler()),
    ('svc', SVC(kernel='linear', probability=True))
])

# Cargar el modelo existente si está presente
if os.path.exists(model_path):
    print(f"Cargando modelo existente desde {model_path}...")
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    print("Modelo cargado.")

# Entrenar modelo
print("Entrenando el modelo...")
model.fit(x_train, y_train)
print("Entrenamiento completado.")

# Guardar el modelo actualizado
print(f"\nGuardando el modelo en {model_path}...")
with open(model_path, 'wb') as f:
    pickle.dump(model, f)
print(f"Modelo guardado como '{model_path}'.")

# Guardar las etiquetas
print(f"Guardando las etiquetas en {labels_path}...")
with open(labels_path, 'wb') as f:
    pickle.dump(labels, f)
print(f"Etiquetas guardadas como '{labels_path}'.")
