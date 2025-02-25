import os
import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt

def analyze_and_resize_images(input_folder, output_folder, resize_dim=(256,256)):
    # Extensions d'image courantes
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff']
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(input_folder, ext)))
        
    if not image_files:
        print("Aucune image trouvée dans le dossier :", input_folder)
        return
    
    heights = []
    widths = []
    areas = []
    
    # Création du dossier de sortie s'il n'existe pas
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Parcours de toutes les images
    for file in image_files:
        img = cv2.imread(file)
        if img is None:
            continue
        h, w = img.shape[:2]
        heights.append(h)
        widths.append(w)
        areas.append(h * w)
        
        # Redimensionnement de l'image
        resized_img = cv2.resize(img, resize_dim)
        # Enregistrement de l'image redimensionnée dans le dossier de sortie
        base_name = os.path.basename(file)
        output_path = os.path.join(output_folder, base_name)
        cv2.imwrite(output_path, resized_img)
    
    if len(areas) == 0:
        print("Aucune image valide trouvée.")
        return
    
    # Calcul des statistiques
    avg_area = np.mean(areas)
    median_height = np.median(heights)
    median_width = np.median(widths)
    max_height = np.max(heights)
    min_height = np.min(heights)
    max_width = np.max(widths)
    min_width = np.min(widths)
    
    # Affichage des résultats
    print("Nombre d'images analysées :", len(areas))
    print("Dimension moyenne (aire) : {:.2f}".format(avg_area))
    print("Hauteur médiane : {:.2f}".format(median_height))
    print("Largeur médiane : {:.2f}".format(median_width))
    print("Hauteur maximale : {}".format(max_height))
    print("Hauteur minimale : {}".format(min_height))
    print("Largeur maximale : {}".format(max_width))
    print("Largeur minimale : {}".format(min_width))
    
    # Affichage des histogrammes
    plt.figure(figsize=(12,5))
    
    plt.subplot(1,2,1)
    plt.hist(heights, bins=30, color='skyblue', edgecolor='black')
    plt.title("Histogramme des hauteurs")
    plt.xlabel("Hauteur (pixels)")
    plt.ylabel("Nombre d'images")
    
    plt.subplot(1,2,2)
    plt.hist(widths, bins=30, color='salmon', edgecolor='black')
    plt.title("Histogramme des largeurs")
    plt.xlabel("Largeur (pixels)")
    plt.ylabel("Nombre d'images")
    
    plt.tight_layout()
    plt.show()
    
    print("Les images redimensionnées ont été sauvegardées dans :", output_folder)

# Exemple d'utilisation
input_folder = "augmented"             # Remplacez par le chemin vers votre dossier source d'images
output_folder = "augmented_256" # Remplacez par le chemin du dossier de sortie
analyze_and_resize_images(input_folder, output_folder, resize_dim=(256,256))
