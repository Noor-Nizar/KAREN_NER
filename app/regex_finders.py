import re
from typing import List

def regex_en_colors(text):
    pattern = r"\b(?:very\s|extremely\s|slightly\s|light\s|dark\s|bright\s|pale\s|deep\s|vivid\s|dull\s|rich\s|soft\s|warm\s|cool\s|muted\s|neon\s|pastel\s)?(?:black|white|red|green|blue|yellow|orange|purple|pink|brown|gray|grey|violet|indigo|cyan|magenta|beige|maroon|navy|teal|olive|turquoise|gold|silver|bronze|lavender|peach|coral|amber|aqua|cream|charcoal|khaki|mustard|tan)\b"
    matches = re.finditer(pattern, text)
    return_list = []
    
    for match in matches:
        return_list.append({
            'entity': match.group(),
            'start_idx': match.start(),
            'end_idx': match.end(),
            'label': 'color'
        })
    
    return return_list

def regex_ar_colors(text):
    # Extended pattern to capture masculine and feminine forms of colors in Arabic
    pattern = r"\b(?:أسود|سوداء|أبيض|بيضاء|أحمر|حمراء|أخضر|خضراء|أزرق|زرقاء|أصفر|صفراء|برتقالي|برتقاليّة|بنفسجي|بنفسجيّة|وردي|ورديّة|بني|بنيّة|رمادي|رماديّة|نيلي|نيليّة|زهري|زهريّة|كريمي|كريميّة|بحري|بحريّة|نحاسي|نحاسيّة|ذهبي|ذهبيّة|فضي|فضيّة|برونزي|برونزيّة|أرجواني|أرجوانيّة|كستنائي|كستنائيّة|عنابي|عنابيّة|فيروزي|فيروزيّة|زيتي|زيتيّة|كحلي|كحليّة|كاكي|كاكيّة|خردلي|خردليّة|تان)\s*(?:فاتح|غامق|زاهي|فاتح جداً|غامق جداً|ساطع|باهت|داكن|فائق|خفيف)?\b|\b(?:فاتح|غامق|زاهي|فاتح جداً|غامق جداً|ساطع|باهت|داكن|فائق|خفيف)?\s*(?:أسود|سوداء|أبيض|بيضاء|أحمر|حمراء|أخضر|خضراء|أزرق|زرقاء|أصفر|صفراء|برتقالي|برتقاليّة|بنفسجي|بنفسجيّة|وردي|ورديّة|بني|بنيّة|رمادي|رماديّة|نيلي|نيليّة|زهري|زهريّة|كريمي|كريميّة|بحري|بحريّة|نحاسي|نحاسيّة|ذهبي|ذهبيّة|فضي|فضيّة|برونزي|برونزيّة|أرجواني|أرجوانيّة|كستنائي|كستنائيّة|عنابي|عنابيّة|فيروزي|فيروزيّة|زيتي|زيتيّة|كحلي|كحليّة|كاكي|كاكيّة|خردلي|خردليّة|تان)\b"
    
    matches = re.finditer(pattern, text)
    return_list = []
    
    for match in matches:
        return_list.append({
            'entity': match.group(),
            'start_idx': match.start(),
            'end_idx': match.end(),
            'label': 'color'
        })
    
    return return_list

def regex_en_dates(text):
    pattern = r"\b(?:\d{1,2}(?:st|nd|rd|th)?\s(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{4}|\d{1,2}(?:-|/)\d{1,2}(?:-|/)\d{2,4}|\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{1,2}(?:st|nd|rd|th)?(?:,\s\d{4})?)\b"
    matches = re.finditer(pattern, text)
    return_list = []
    
    for match in matches:
        return_list.append({
            'entity': match.group(),
            'start_idx': match.start(),
            'end_idx': match.end(),
            'label': 'date'
        })
    
    return return_list

def regex_en_times(text):
    pattern = r"(?<!\d)(?:[01]?\d:\d{2}(?::\d{2})?\s?(?:AM|PM|am|pm)?)(?!\d)"
    matches = re.finditer(pattern, text)
    return_list = []
    
    for match in matches:
        return_list.append({
            'entity': match.group(),
            'start_idx': match.start(),
            'end_idx': match.end(),
            'label': 'time'
        })
    
    return return_list

def regex_ar_dates(text):
    pattern = (
        r"\b(?:[\u0660-\u0669]{1,2}\s(?:يناير|فبراير|مارس|أبريل|مايو|يونيو|يوليو|"
        r"أغسطس|سبتمبر|أكتوبر|نوفمبر|ديسمبر)\s[\u0660-\u0669]{4}|"
        r"[\u0660-\u0669]{1,2}(?:-|/)[\u0660-\u0669]{1,2}(?:-|/)[\u0660-\u0669]{2,4}|"
        r"(?:يناير|فبراير|مارس|أبريل|مايو|يونيو|يوليو|أغسطس|سبتمبر|أكتوبر|نوفمبر|"
        r"ديسمبر)\s[\u0660-\u0669]{1,2}(?:،\s[\u0660-\u0669]{4})?)\b"
    )
    matches = re.finditer(pattern, text)
    return_list = []
    
    for match in matches:
        return_list.append({
            'entity': match.group(),
            'start_idx': match.start(),
            'end_idx': match.end(),
            'label': 'date'
        })
    
    return return_list

def regex_ar_times(text):
    pattern = r"(?<![\u0660-\u0669])(?:[\u0660-\u0661]?\u0660:\u0660{2}(?::\u0660{2})?\s?(?:ص|م))(?![\u0660-\u0669])"
    matches = re.finditer(pattern, text)
    return_list = []
    
    for match in matches:
        return_list.append({
            'entity': match.group(),
            'start_idx': match.start(),
            'end_idx': match.end(),
            'label': 'time'
        })
    
    return return_list

def regex_en_currency(text):
    # Regex pattern for detecting English currency formats
    pattern = r"\b(?:\$\s?\d+(?:,\d{3})*(?:\.\d+)?|€\s?\d+(?:,\d{3})*(?:\.\d+)?|£\s?\d+(?:,\d{3})*(?:\.\d+)?|¥\s?\d+(?:,\d{3})*(?:\.\d+)?|USD\s?\d+(?:,\d{3})*(?:\.\d+)?|dollar(?:s)?\s?\d+(?:,\d{3})*(?:\.\d+)?|euro(?:s)?\s?\d+(?:,\d{3})*(?:\.\d+)?|pound(?:s)?\s?\d+(?:,\d{3})*(?:\.\d+)?|yen\s?\d+(?:,\d{3})*(?:\.\d+)?|rupee(?:s)?\s?\d+(?:,\d{3})*(?:\.\d+)?|₽\s?\d+(?:,\d{3})*(?:\.\d+)?|₹\s?\d+(?:,\d{3})*(?:\.\d+)?|rub(?:le|les)?\s?\d+(?:,\d{3})*(?:\.\d+)?)\b"
    matches = re.finditer(pattern, text, re.IGNORECASE)
    return_list = []
    
    for match in matches:
        return_list.append({
            'entity': match.group(),
            'start_idx': match.start(),
            'end_idx': match.end(),
            'label': 'currency'
        })
    
    return return_list

def regex_ar_currency(text):
    # Regex pattern for detecting Arabic currency formats
    pattern = r"\b(?:\d+(?:,\d{3})*(?:\.\d+)?\s?(?:دولار|دولارات|يورو|يوروهات|جنيه|جنيهات|ين|ينات|روبل|روبلات|روبية|روبيات)|(?:دولار|دولارات|يورو|يوروهات|جنيه|جنيهات|ين|ينات|روبل|روبلات|روبية|روبيات)\s?\d+(?:,\d{3})*(?:\.\d+)?)\b"
    matches = re.finditer(pattern, text)
    return_list = []
    
    for match in matches:
        return_list.append({
            'entity': match.group(),
            'start_idx': match.start(),
            'end_idx': match.end(),
            'label': 'currency'
        })
    
    return return_list

def regex_en_units(text):
    # Regex pattern for detecting English units of measurement with additional structures
    pattern = r"\b(?:kg|kilograms?|g(?!\b)|grams?|lb|pounds?|oz|ounces?|meters?|cm|centimeters?|mm|millimeters?|km|kilometers?|in(?:ches)?|ft|feet|mile?s?|liters?|ml|milliliters?|gallons?|quarts?|pints?|sq\s?m|square\s?meters?|sq\s?ft|square\s?feet?|square\s?foot|acres?|hectares?|(?:km|m|cm|mm|g|kg|liters?)\s?(?:/|per|p)\s?(?:h|hour|hr|day|week|month|year)s?)\b"
    matches = re.finditer(pattern, text, re.IGNORECASE)
    return_list = []
    
    for match in matches:
        return_list.append({
            'entity': match.group(),
            'start_idx': match.start(),
            'end_idx': match.end(),
            'label': 'unit'
        })
    
    return return_list

def regex_ar_units(text):
    # Regex pattern for detecting Arabic units of measurement (singular and plural)
    pattern = r"\b(?:كجم|كيلوغرام|غرام|رطل|أوقية|متر|سنتيمتر|ميليمتر|كيلومتر|كيلومترات|بوصة|قدم|ميل|أميال|لتر|مل|غالون|كوارت|باينت|متر مربع|قدم مربع|فدان|هكتار|كم|م|سم|مم|غ|كجم|لتر)\b"
    matches = re.finditer(pattern, text)
    return_list = []
    
    for match in matches:
        return_list.append({
            'entity': match.group(),
            'start_idx': match.start(),
            'end_idx': match.end(),
            'label': 'unit'
        })
    
    return return_list

def regex_ner(text:str)->List:
    all_matches = []
    
    # Collect matches from all regex functions
    all_matches.extend(regex_en_dates(text))
    all_matches.extend(regex_en_times(text))
    all_matches.extend(regex_ar_dates(text))
    all_matches.extend(regex_ar_times(text))
    
    all_matches.extend(regex_en_colors(text))
    all_matches.extend(regex_ar_colors(text))

    all_matches.extend(regex_en_currency(text))
    all_matches.extend(regex_ar_currency(text))

    all_matches.extend(regex_en_units(text))
    all_matches.extend(regex_ar_units(text))

    ## exclude empty lists
    all_matches = [match for match in all_matches if match]
    return all_matches
