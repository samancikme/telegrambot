import requests

word = "olma"
# 1. Translate Uz -> En
url_trans = f"https://api.mymemory.translated.net/get?q={word}&langpair=uz|en"
res = requests.get(url_trans)
if res.status_code == 200:
    en_word = res.json()['responseData']['translatedText']
    print(f"Translated '{word}' to '{en_word}'")
    
    # 2. Get AI Image URL
    img_url = f"https://image.pollinations.ai/prompt/A high quality photo of {en_word}?width=400&height=400&nologo=true"
    print(f"Image URL: {img_url}")
    
    # Check if download works
    img_res = requests.get(img_url)
    print("Image download status:", img_res.status_code)
