import shutil, os

BRAIN = "/home/samandar/.gemini/antigravity/brain/0b9da51f-0953-4d66-95b8-a80030e84615"
IMG = "/home/samandar/Desktop/python projects/proyekt/images"

files = {
    "assalomualeykum_adult_1780341580406.png": "assalomualeykum.png",
    "hayirlitong_adult_1780341593378.png":     "hayirlitong.png",
    "uy_adult_1780341609805.png":              "uy.png",
    "bugun_adult_1780341622182.png":           "bugun.png",
    "bobo_adult_1780341634096.png":            "bobo.png",
    "buvi_adult_1780341644958.png":            "buvi.png",
    "bir_adult_1780341683877.png":             "bir.png",
    "ikki_adult_1780341702970.png":            "ikki.png",
    "non_adult_1780341715369.png":             "non.png",
    "suv_adult_1780341727583.png":             "suv.png",
    "qizil_adult_1780341755408.png":           "qizil.png",
    "yashil_adult_1780341768464.png":          "yashil.png",
    "osmon_adult_1780341784490.png":           "osmon.png",
    "quyosh_adult_1780341795629.png":          "quyosh.png",
    "kitob_adult_1780341811579.png":           "kitob.png",
    "qalam_adult_1780341825703.png":           "qalam.png",
}

for src_name, dst_name in files.items():
    src = os.path.join(BRAIN, src_name)
    dst = os.path.join(IMG, dst_name)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"✅ {dst_name}")
    else:
        print(f"❌ topilmadi: {src_name}")

print(f"\nJami {len(files)} ta rasm ko'chirildi.")
