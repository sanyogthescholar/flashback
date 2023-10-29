#import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

def caption_image(path):
    raw_image = Image.open(path).convert('RGB')
    inputs = processor(raw_image, return_tensors="pt")
    out = model.generate(**inputs)
    return processor.decode(out[0], skip_special_tokens=True)

#img_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/demo.jpg' 
#raw_image = Image.open(requests.get(img_url, stream=True).raw).convert('RGB')

# conditional image captioning
"""text = "a photography of"
inputs = processor(raw_image, text, return_tensors="pt")

out = model.generate(**inputs)
print(processor.decode(out[0], skip_special_tokens=True))"""

# unconditional image captioning
#inputs = processor(raw_image, return_tensors="pt")

#out = model.generate(**inputs)
#print(processor.decode(out[0], skip_special_tokens=True))