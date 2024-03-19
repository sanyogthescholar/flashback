#import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import chromadb
import uuid
ENV = "BACK"
chroma_client = chromadb.PersistentClient(path="chromadb")

try:
    collection = chroma_client.create_collection(name="my_collection")
except:
    collection = chroma_client.get_collection(name="my_collection")

if ENV == "WEB":
    print("Environment for Web Development, model loading skipped")
else:
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

def caption_image(path):
    if ENV == "WEB":
        collection.add(
        documents=["dummy caption"],
        metadatas=[{"path": path, "owner":path.split("\\")[-2]}],
        ids=[str(uuid.uuid4())]
        )
        return "dummy caption"
    else:
        raw_image = Image.open(path).convert('RGB')
        inputs = processor(raw_image, return_tensors="pt")
        out = model.generate(**inputs)
        caption = processor.decode(out[0], skip_special_tokens=True)
        collection.add(
            documents=[caption],
            metadatas=[{"path": path, "owner":path.split("\\")[-2]}],
            ids=[str(uuid.uuid4())]
            )
        results = collection.query(
        query_texts=["animal"],
        n_results=2
    )
        #print(f"{results = }")
        return caption