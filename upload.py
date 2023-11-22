import firebase_admin
from firebase_admin import credentials, firestore, storage
import os

# Initialize Firebase Admin SDK with your service account key JSON file
cred = credentials.Certificate("praktyk-cb1c1-firebase-adminsdk-628to-cb4b937937.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'praktyk-cb1c1.appspot.com'
})

db = firestore.client()
bucket = storage.bucket()

AUDIO_DIR = 'Afrikaans days'

def upload_audio_to_storage(file_name, file_path):
    # Set the destination path for the audio file on Firebase
    destination_path = f"Audio/Days Of The Week/{file_name}"
    blob = bucket.blob(destination_path)
    blob.upload_from_filename(file_path)
    blob.make_public()
    return blob.public_url

# Fetch the document
doc_ref = db.collection('Match The Column').document('Days Of The Week')
doc = doc_ref.get()
# go in collection audio
#new doc folder name
# read from csv 
#the map audio

if doc.exists:
    mappings = doc.to_dict().get('Questions', [])  # Replace 'mappings' with the actual field name of your array

    # Iterate over audio files in the 'Afrikaans days' folder
    for index, mapping in enumerate(mappings):
        file_name = f"sound_{index + 1}.mp3"  # Adjust the naming pattern if different
        file_path = os.path.join(AUDIO_DIR, file_name)
        
        if os.path.exists(file_path):
            audio_url = upload_audio_to_storage(file_name, file_path)
            mapping['audio'] = audio_url  # Add audio URL to the mapping

    # Update the document
    doc_ref.update({'mappings': mappings})
    print("Updated document with audio references.")
else:
    print("Document does not exist.")
