import aiohttp
import urllib.parse
from uuid import uuid4

async def fetch_image_for_word(text, source_lang='uz'):
    """
    Translates the word to English using MyMemory API, 
    then fetches a generated image from Pollinations AI.
    Returns the URL of the generated image.
    """
    # 1. Translate to English (Pollinations AI understands English best)
    en_word = text
    try:
        # MyMemory translation API (Free, no key required)
        langpair = f"{source_lang}|en"
        trans_url = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(text)}&langpair={langpair}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(trans_url, timeout=5) as response:
                if response.status == 200:
                    data = await response.json()
                    en_word = data.get('responseData', {}).get('translatedText', text)
    except Exception as e:
        print(f"Translation error: {e}")
        # Falback to the original word if translation fails
        pass

    # 2. Get AI Image URL based on the English word
    # Adding some prompt engineering to get better standalone object photos
    prompt = f"A high quality clear photo of {en_word}, white background, single object"
    encoded_prompt = urllib.parse.quote(prompt)
    seed = uuid4().int % 100000 # Random seed for variety
    
    img_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=400&height=400&nologo=true&seed={seed}"
    return img_url
