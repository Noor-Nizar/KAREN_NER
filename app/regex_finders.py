import re

def regex_en_colors(text):
    pattern = r"\b(?:very\s|extremely\s|slightly\s|light\s|dark\s|bright\s|pale\s|deep\s|vivid\s|dull\s|rich\s|soft\s|warm\s|cool\s|muted\s|neon\s|pastel\s)?(?:black|white|red|green|blue|yellow|orange|purple|pink|brown|gray|grey|violet|indigo|cyan|magenta|beige|maroon|navy|teal|olive|turquoise|gold|silver|bronze|lavender|peach|coral|amber|aqua|cream|charcoal|khaki|mustard|tan)\b"
    matches = re.finditer(pattern, text)
    color_dict = {}
    
    for match in matches:
        color_dict[match.group()] = {
            'start_idx': match.start(),
            'end_idx': match.end(),
            'entity': 'Color'
        }
    
    return color_dict


def regex_ar_colors(text):
    pattern = r"\b(?:فاتح\s|غامق\s|زاهي\s|فاتح جداً\s|غامق جداً\s|ساطع\s|باهت\s|داكن\s|فائق\s|خفيف\s)?(?:أسود|أبيض|أحمر|أخضر|أزرق|أصفر|برتقالي|بنفسجي|وردي|بني|رمادي|رمادى|بنفسجي|نيلي|سماوي|زهري|كريمي|بحري|نحاسي|ذهبي|فضي|برونزي|أرجواني|كستنائي|عنابي|نيلي|فيروزي|زيتي|كريمي|كحلي|كاكي|خردلي|تان)\b"
    matches = re.finditer(pattern, text)
    color_dict = {}
    
    for match in matches:
        color_dict[match.group()] = {
            'start_idx': match.start(),
            'end_idx': match.end(),
            'entity': 'Color'
        }
    
    return color_dict

def regex_en_dates(text):
    pattern = r"\b(?:\d{1,2}(?:st|nd|rd|th)?\s(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{4}|\d{1,2}(?:-|/)\d{1,2}(?:-|/)\d{2,4}|\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{1,2}(?:st|nd|rd|th)?(?:,\s\d{4})?)\b"
    matches = re.finditer(pattern, text)
    date_dict = {}
    
    for match in matches:
        date_dict[match.group()] = {
            'start_idx': match.start(),
            'end_idx': match.end(),
            'entity': 'Date'
        }
    
    return date_dict

def regex_en_times(text):
    pattern = r"(?<!\d)(?:[01]?\d:\d{2}(?::\d{2})?\s?(?:AM|PM|am|pm)?)(?!\d)"
    matches = re.finditer(pattern, text)
    time_dict = {}
    
    for match in matches:
        time_dict[match.group()] = {
            'start_idx': match.start(),
            'end_idx': match.end(),
            'entity': 'Time'
        }
    
    return time_dict



def regex_ar_dates(text):
    pattern = r"\b(?:\d{1,2}\s(?:يناير|فبراير|مارس|أبريل|مايو|يونيو|يوليو|أغسطس|سبتمبر|أكتوبر|نوفمبر|ديسمبر)\s\d{4}|\d{1,2}(?:-|/)\d{1,2}(?:-|/)\d{2,4}|\b(?:يناير|فبراير|مارس|أبريل|مايو|يونيو|يوليو|أغسطس|سبتمبر|أكتوبر|نوفمبر|ديسمبر)\s\d{1,2}(?:،\s\d{4})?)\b"
    matches = re.finditer(pattern, text)
    date_dict = {}
    
    for match in matches:
        date_dict[match.group()] = {
            'start_idx': match.start(),
            'end_idx': match.end(),
            'entity': 'Date'
        }
    
    return date_dict

def regex_ar_times(text):
    pattern = r"(?<!\d)(?:[01]?\d:\d{2}(?::\d{2})?\s?(?:ص|م))(?!\d)"
    matches = re.finditer(pattern, text)
    time_dict = {}
    
    for match in matches:
        time_dict[match.group()] = {
            'start_idx': match.start(),
            'end_idx': match.end(),
            'entity': 'Time'
        }
    
    return time_dict

def regex_en_currency(text):
    # Regex pattern for detecting English currency formats
    pattern = r"\b(?:\$\s?\d+(?:,\d{3})*(?:\.\d+)?|€\s?\d+(?:,\d{3})*(?:\.\d+)?|£\s?\d+(?:,\d{3})*(?:\.\d+)?|¥\s?\d+(?:,\d{3})*(?:\.\d+)?|USD\s?\d+(?:,\d{3})*(?:\.\d+)?|dollar(?:s)?\s?\d+(?:,\d{3})*(?:\.\d+)?|euro(?:s)?\s?\d+(?:,\d{3})*(?:\.\d+)?|pound(?:s)?\s?\d+(?:,\d{3})*(?:\.\d+)?|yen\s?\d+(?:,\d{3})*(?:\.\d+)?|rupee(?:s)?\s?\d+(?:,\d{3})*(?:\.\d+)?|₽\s?\d+(?:,\d{3})*(?:\.\d+)?|₹\s?\d+(?:,\d{3})*(?:\.\d+)?|rub(?:le|les)?\s?\d+(?:,\d{3})*(?:\.\d+)?)\b"
    matches = re.finditer(pattern, text, re.IGNORECASE)
    currency_dict = {}

    for match in matches:
        currency_dict[match.group()] = {
            'start_idx': match.start(),
            'end_idx': match.end(),
            'entity': 'Currency'
        }
    
    return currency_dict

def regex_ar_currency(text):
    # Regex pattern for detecting Arabic currency formats
    pattern = r"\b(?:\d+(?:,\d{3})*(?:\.\d+)?\s?(?:دولار|دولارات|يورو|يوروهات|جنيه|جنيهات|ين|ينات|روبل|روبلات|روبية|روبيات)|(?:دولار|دولارات|يورو|يوروهات|جنيه|جنيهات|ين|ينات|روبل|روبلات|روبية|روبيات)\s?\d+(?:,\d{3})*(?:\.\d+)?)\b"
    matches = re.finditer(pattern, text)
    currency_dict = {}

    for match in matches:
        currency_dict[match.group()] = {
            'start_idx': match.start(),
            'end_idx': match.end(),
            'entity': 'Currency'
        }
    
    return currency_dict

def regex_en_units(text):
    # Regex pattern for detecting English units of measurement with additional structures
    pattern = r"\b(?:kg|kilograms?|g(?!\b)|grams?|lb|pounds?|oz|ounces?|meters?|cm|centimeters?|mm|millimeters?|km|kilometers?|in(?:ches)?|ft|feet|mile?s?|liters?|ml|milliliters?|gallons?|quarts?|pints?|sq\s?m|square\s?meters?|sq\s?ft|square\s?feet?|square\s?foot|acres?|hectares?|(?:km|m|cm|mm|g|kg|liters?)\s?(?:/|per|p)\s?(?:h|hour|hr|day|week|month|year)s?)\b"
    matches = re.finditer(pattern, text, re.IGNORECASE)
    units_dict = {}

    for match in matches:
        units_dict[match.group()] = {
            'start_idx': match.start(),
            'end_idx': match.end(),
            'entity': 'Unit'
        }
    
    return units_dict

def regex_ar_units(text):
    # Regex pattern for detecting Arabic units of measurement with additional structures
    pattern = r"\b(?:كجم|كيلوغرام|غرام|رطل|أوقية|متر|سنتيمتر|ميليمتر|كيلومتر|بوصة|قدم|ميل|لتر|مل|غالون|كوارت|باينت|متر مربع|قدم مربع|فدان|هكتار|(?:كم|م|سم|مم|غ|كجم|لتر)\s?(?:\/|في|لكل)\s?(?:س|ساعة|يوم|أسبوع|شهر|سنة)s?)\b"
    matches = re.finditer(pattern, text)
    units_dict = {}

    for match in matches:
        units_dict[match.group()] = {
            'start_idx': match.start(),
            'end_idx': match.end(),
            'entity': 'Unit'
        }
    
    return units_dict



def regex_ner(text):
    all_matches = {}
    
    # Collect matches from all regex functions
    all_matches.update(regex_en_dates(text))
    all_matches.update(regex_en_times(text))
    all_matches.update(regex_ar_dates(text))
    all_matches.update(regex_ar_times(text))
    
    all_matches.update(regex_en_colors(text))
    all_matches.update(regex_ar_colors(text))

    all_matches.update(regex_en_currency(text))
    all_matches.update(regex_ar_currency(text))

    all_matches.update(regex_en_units(text))
    all_matches.update(regex_ar_units(text))

    return all_matches

