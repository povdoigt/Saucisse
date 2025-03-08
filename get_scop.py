import requests
import json
from deep_translator import GoogleTranslator
import random

language_codes = [
    "af", "sq", "am", "ar", "hy", "az", "eu", "be", "bn", "bs", "bg", "ca", "ceb", "ny",
    "zh", "zh-cn", "co", "hr", "cs", "da", "nl", "en", "eo", "et", "tl", "fi",
    "fr", "fy", "gl", "ka", "de", "el", "gu", "ht", "ha", "haw", "he", "iw", "hi", "hmn",
    "hu", "is", "ig", "id", "ga", "it", "ja", "jw", "kn", "kk", "km", "ko", "ku", "ky",
    "lo", "la", "lv", "lt", "lb", "mk", "mg", "ms", "ml", "mt", "mi", "mr", "mn", "my",
    "ne", "no", "or", "ps", "fa", "pl", "pt", "pa", "ro", "ru", "sm", "gd", "sr", "st",
    "sn", "sd", "si", "sk", "sl", "so", "es", "su", "sw", "sv", "tg", "ta", "te", "th",
    "tr", "uk", "ur", "ug", "uz", "vi", "cy", "xh", "yi", "yo", "zu"
]

def get_HSCP(signe):
    url = f'https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily?sign={signe}&day=TODAY'
    respons = requests.get(url)

    if respons.status_code == 200:
        data_get = respons.json()
        horoscop_ang = data_get["data"]["horoscope_data"]
        return horoscop_ang
    else :
        return None

def translate_data(data,lg):
    return GoogleTranslator(source= 'en',target=lg).translate(data)

def get_HSCP_tr(signe):
    lg = language_codes[random.randint(0,len(language_codes))]
    return translate_data(get_HSCP(signe),lg)

def get_HSCP_fr(signe):
    lg= language_codes[random.randint(0,len(language_codes))]
    return GoogleTranslator(source= lg,target='fr').translate(translate_data(get_HSCP(signe),lg))