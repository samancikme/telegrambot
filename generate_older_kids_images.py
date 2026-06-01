import os
import urllib.request

# 26 vocabulary words mapped to high-quality, professional, stylish Unsplash photos
# perfectly suited for older kids / teenagers
UNSPLASH_IDS = {
    # Salomlashuv
    "assalomualeykum.png": "photo-1511632765486-a01980e01a18",  # Diverse teens waving and smiling
    "hayirlitong.png":      "photo-1470252649378-9c29740c9fa8",  # Beautiful sunrise over mountains
    
    # Kundalik hayot
    "uy.png":               "photo-1513694203232-719a280e022f",  # Ultra-modern smart architectural home
    
    # Vaqt va kunlar
    "bugun.png":            "photo-1506784983877-45594efa4cbe",  # Clean elegant aesthetic planner / "Today"
    
    # Oila a'zolari
    "bobo.png":             "photo-1544161515-4ab6ce6db874",  # Cool smiling older grandfather with trendy glasses
    "buvi.png":             "photo-1509198397868-475647b2a1e5",  # Warm, happy, smiling grandmother
    
    # Sonlar
    "bir.png":              "photo-1616469829581-73993eb86b02",  # Sleek neon glowing number 1 sign
    "ikki.png":             "photo-1618005182384-a83a8bd57fbe",  # Sleek neon glowing number 2 sign
    
    # Oziq-ovqat
    "non.png":              "photo-1509440159596-0249088772ff",  # Perfect golden freshly-baked bread
    "suv.png":              "photo-1548839140-29a749e1cf4d",  # Cool refreshing glass of ice water with splashes
    
    # Ranglar
    "qizil.png":            "photo-1541701494587-cb58502866ab",  # Elegant abstract red fluid art
    "yashil.png":           "photo-1501004318641-b39e6451bec6",  # Cool aesthetic green leaves wallpaper
    
    # Tabiat
    "osmon.png":            "photo-1419242902214-272b3f66ee7a",  # Stunning starry night sky with Milky Way galaxy
    "quyosh.png":           "photo-1506318137071-a8e063b4bec0",  # Majestic golden sun shining over clouds
    
    # O'qish
    "kitob.png":            "photo-1495446815901-a7297e633e8d",  # Beautiful stack of modern books
    "qalam.png":            "photo-1516962215378-7fa2e137ae93",  # Sleek drafting pencil on a blueprint
    
    # Kiyimlar
    "koylak.png":           "photo-1595777457583-95e059d581b8",  # Modern elegant casual dress in a boutique
    "oyoqkiyim.png":        "photo-1542291026-7eec264c27ff",  # Cool trendy red high-top streetwear sneakers
    
    # Hayvonlar
    "mushuk.png":           "photo-1514888286974-6c03e2ca1dba",  # Highly-detailed striking portrait of a cat
    "kuchuk.png":           "photo-1543466835-00a7907e9de1",  # Handsome, cool golden retriever dog portrait
    
    # Mevalar
    "olma.png":             "photo-1560806887-1e4cd0b6cbd6",  # Glossy fresh red apple with water drops
    "banan.png":            "photo-1571771894821-ce9b6c11b08e",  # Minimalist stylish bananas pop-art background
    
    # O'yinchoqlar
    "koptok.png":           "photo-1579952363873-27f3bade9f55",  # Professional soccer ball on grass under stadium lights
    "mashina.png":          "photo-1617788138017-80ad40651399",  # Sleek modern electric sports car driving under city lights
    
    # Tana a'zolari
    "bosh.png":             "photo-1507668077129-56e32842fceb",  # Cool neon head silhouette / digital brain art
    "koz.png":              "photo-1576243345690-4e4b79b63288"   # Stunning macro photo of a detailed human eye iris
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")

def download_image(filename, unsplash_id):
    target_path = os.path.join(IMAGES_DIR, filename)
    url = f"https://images.unsplash.com/{unsplash_id}?w=512&h=512&fit=crop&auto=format"
    
    try:
        # Mock standard web browser User-Agent
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        
        with urllib.request.urlopen(req, timeout=15) as response:
            data = response.read()
            with open(target_path, 'wb') as f:
                f.write(data)
        
        print(f"✅ Successfully downloaded Unsplash image for {filename} ({len(data) / 1024:.1f} KB)")
        return True
    except Exception as e:
        print(f"❌ Failed to download {filename} (ID: {unsplash_id}): {e}")
        return False

def main():
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)
        
    print(f"🚀 Starting download of {len(UNSPLASH_IDS)} premium Unsplash images...")
    
    success_count = 0
    for filename, unsplash_id in UNSPLASH_IDS.items():
        if download_image(filename, unsplash_id):
            success_count += 1
            
    print(f"\n📊 Final Summary: {success_count}/{len(UNSPLASH_IDS)} downloaded successfully.")

if __name__ == "__main__":
    main()
