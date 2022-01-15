import face_recognition
import pickle
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, "dataset")
ACCEPTED_FILES = [".png", ".jpg", ".jpeg"]

for root, dirs, files in os.walk(image_dir):
  all_face_encodings = []
  label = os.path.basename(root)
  print(f'training {label}')

  for file in files:
    try:
      if (os.path.splitext(file)[1] in ACCEPTED_FILES):
        path = os.path.join(root, file)
        image = face_recognition.load_image_file(path)
        all_face_encodings.append(face_recognition.face_encodings(image)[0])
    except e:
      print(f'Não foi possivel treinar a foto {file}')


  if (label != 'dataset'):
    with open(f'pickles/{label}.pickle', 'wb') as f:
      pickle.dump(all_face_encodings, f)