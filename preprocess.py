import emoji
import re

def removeEmojis(address):
    return emoji.replace_emoji(str(address), replace='')

def removePunct(address):
    punct = "`؛;_ـ،:.-'|,"
    return re.sub(f"[{re.escape(punct)}]", " ", address)

def changeEnglishToArabic(address):
    mapping = {
        "floor": "دور",
        "st": "شارع",
        "street": "شارع",
        "apartment": "شقه",
        "apt": "شقه",
    }

    for eng, ar in mapping.items():
        address = re.sub(rf"\b{eng}\b", ar, address, flags=re.IGNORECASE)

    return address

def changeNumEngToArabic(address):
    eng = "0123456789"
    arb = "٠١٢٣٤٥٦٧٨٩"
    return address.translate(str.maketrans(eng, arb))

def convertCharToWord(address):
    mapping = {
        "ش": "شارع"
    }

    for x, y in mapping.items():
        address = re.sub(rf"\b{x}\b", y, address)

    return address

def removeDiacritics(address):
    return re.sub(r'[\u064B-\u0652]', '', address)

# def normalizeSomeChar(address):
#     src = "اأإآيىگكؤوةه"
#     dst = "ااااييككووهه"
#     return address.translate(str.maketrans(src, dst))
def normalizeSomeChar(address):
    address = re.sub("[أإآ]", "ا", address)
    address = re.sub("ى", "ي", address)
    return address
# def dropDuplicateSafeChars(address):
#     return re.sub(r"([^\d])\1+", r"\1", address)

def numArabicApt(address):
    mapping = {
        "واحد":"١",
        "الاولي":"١",
        "اثنين":"٢",
        "اتنين":"٢",
        "الثانيه":"٢",
        "التانيه":"٢",
        "ثلاثه":"٣",
        "تلاته":"٣",
        "الثالثه":"٣",
        "اربعه":"٤",
        "الرابعه":"٤",
        "خمسه":"٥",
        "سته":"٦",
        "سبعه":"٧",
        "ثمانيه":"٨",
        "تمانيه":"٨",
        "تسعه":"٩",
        "عشره":"١٠"
    }

    for w, n in mapping.items():
        address = re.sub(rf"\b{w}\b", n, address)

    return address

# def numArabicFloor(address):
#     mapping = {
#         "الاول":"١",
#         "الثاني":"٢",
#         "التاني":"٢",
#         "الثالث":"٣",
#         "التالت":"٣",
#         "الرابع":"٤",
#         "الخامس":"٥",
#         "السادس":"٦",
#         "السابع":"٧",
#         "الثامن":"٨",
#         "التامن":"٨",
#         "التاسع":"٩",
#         "العاشر":"١٠"
#     }

#     for w, n in mapping.items():
#         address = re.sub(rf"\b{w}\b", n, address)

#     return address

def preprocessing(address):
    address = str(address)
    address = removeEmojis(address)
    address = changeEnglishToArabic(address)
    address = removePunct(address)
    address = convertCharToWord(address)
    address = changeNumEngToArabic(address)
    address = removeDiacritics(address)
    address = normalizeSomeChar(address)
    # address = dropDuplicateSafeChars(address)
    address = numArabicApt(address)
    # address = numArabicFloor(address)
    address = " ".join(address.split())

    return address.lower()
