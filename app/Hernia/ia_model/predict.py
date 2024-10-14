import cv2
import pickle
from skimage.feature import hog

# Definir dimensiones de las imágenes
width = 300
height = 300

# Función para extraer características
def extract_features(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    features, _ = hog(gray_image, visualize=True, block_norm='L2-Hys')
    return features

# Cargar el modelo guardado
def load_model():
    print("\nCargando el modelo guardado...")
    with open('app/Hernia/ia_model/mimodelo.pkl', 'rb') as f:
        model = pickle.load(f)
    print("Modelo cargado.")
    return model

# Cargar las etiquetas
def load_labels():
    print("Cargando etiquetas...")
    with open('app/Hernia/ia_model/labels.pkl', 'rb') as f:
        labels = pickle.load(f)
    print("Etiquetas cargadas.")
    return labels

# Realizar una predicción sobre una imagen
def predict_image(image_path):
    model = load_model()
    labels = load_labels()

    # Cargar la imagen y extraer características
    my_image = cv2.imread(image_path)
    my_image = cv2.resize(my_image, (width, height))
    my_image_features = extract_features(my_image)

    # Realizar la predicción
    result = model.predict_proba([my_image_features])[0]
    porcentaje = max(result) * 100
    grupo = labels[result.argmax()]

    return grupo, round(porcentaje)
