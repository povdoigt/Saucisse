from random import choice,randint
from get_scop import get_HSCP_tr,get_HSCP_fr
signes = [
    "Bélier",  
    "Taureau",  
    "Gémeaux",  
    "Cancer",  
    "Lion",  
    "Vierge",  
    "Balance",  
    "Scorpion",  
    "Sagittaire",  
    "Capricorne",  
    "Verseau",  
    "Poissons"
]
signes_astrologiques_dict = {
    "Bélier": "Aries",
    "Taureau": "Taurus",
    "Gémeaux": "Gemini",
    "Cancer": "Cancer",
    "Lion": "Leo",
    "Vierge": "Virgo",
    "Balance": "Libra",
    "Scorpion": "Scorpio",
    "Sagittaire": "Sagittarius",
    "Capricorne": "Capricorn",
    "Verseau": "Aquarius",
    "Poissons": "Pisces"
}
def get_response(user_input):
    lowered= user_input.lower()
    if lowered == '':
        return 'Well you\'re awfully scilent...'
    elif lowered == '??':
        return 'nique ta race'
    elif lowered == 'help':
        return"""Bonjours je suis le bot ***Saucisse***
voici un petit aperçu de mes capacitées:
* je peux repondre en publique ou en privée, pour que je reponde en privée, commencez votre requete par '///'
* je vous insulte sui vous utilisez la locution suivant: \"??\"
* je peux aussi envoyer une image de saucisse si vous utilisez le mot saucisse
* je peux aussi vous donner l'horoscope du jour  
    * horoscope #signe# vous donne l'oroscope du signe dans une langue aléatoire
    * hscope_fr #signe# vous donne l'horoscope du signe en français 
De rien, bonne journée"""
    elif 'horoscope' in lowered:
        print(lowered)
        for i,j in enumerate(signes):
            if j.lower() in lowered:
                print(j)
                print(signes_astrologiques_dict[j])
                return get_HSCP_tr(signes_astrologiques_dict[j])
        else:
            return 'signe inconnu'
    elif 'hscope_fr' in lowered:
        print(lowered)
        for i,j in enumerate(signes):
            if j.lower() in lowered:
                print(j)
                print(signes_astrologiques_dict[j])
                return get_HSCP_fr(signes_astrologiques_dict[j])
        else:
            return 'signe inconnu'
    elif 'quoi' in lowered[-5:]:
        return '# FEUR'
    elif 'qui' in lowered[-5:] or lowered[:3] == 'qui':
        return '# Pratick Kanner'
    else:
        return ''
    """else :
        return choice(['???',
                       'je comprend pas',
                       'NTM'])"""
    
