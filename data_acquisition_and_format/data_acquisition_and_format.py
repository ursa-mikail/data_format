#!pip install langdetect
'''
Text extraction (removal of html tags and images, including document format stripping) -> language identification -> removal of duplicates -> removal of blacklist contents and abusive emotives -> removal of non-informative content -> ready for tokenization
''''


import requests
from bs4 import BeautifulSoup
import langdetect
import re
from collections import OrderedDict

def fetch_url_content(url):
    """Fetches the HTML content of a given URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

def remove_html_tags(text):
    """Removes HTML tags and decodes HTML entities."""
    soup = BeautifulSoup(text, "html.parser")
    for img in soup.find_all("img"):
        img.decompose()  # Remove images
    return soup.get_text()

def identify_language(text):
    """Identifies the language of the text."""
    try:
        return langdetect.detect(text)
    except langdetect.lang_detect_exception.LangDetectException:
        return None

def remove_duplicates(text_list):
    """Removes duplicate entries while preserving order."""
    return list(OrderedDict.fromkeys(text_list))

def remove_blacklisted_content(text, blacklist):
    """Removes blacklisted words or abusive content from text."""
    for word in blacklist:
        text = re.sub(rf"\b{re.escape(word)}\b", "", text, flags=re.IGNORECASE)
    return text

def remove_non_informative(text):
    """Removes non-informative content such as short or meaningless text."""
    return text if len(text.split()) > 3 else ""  # Adjust threshold as needed

def preprocess_url(url, blacklist):
    """Runs the full pipeline to prepare text from a URL for tokenization."""
    html_content = fetch_url_content(url)
    if not html_content:
        return None, None

    text = remove_html_tags(html_content)
    lang = identify_language(text)
    text = remove_blacklisted_content(text, blacklist)
    text = remove_non_informative(text)

    return text, lang

# Example usage
url = "https://www.youtube.com/watch?v=d7Eqv2ibXyw"
blacklist_words = ["test", "example"]

clean_text, language = preprocess_url(url, blacklist_words)
print("Processed Text:", clean_text[:500])  # Print first 500 characters
print("Detected Language:", language)

import langcodes

def map_language_code(lang_code):
    """Maps a language code to its full human-readable name."""
    try:
        return langcodes.Language.get(lang_code).display_name()
    except ValueError:
        return "Unknown Language"

# Example usage
lang_code = "nl"
print("Detected Language:", map_language_code(language))  # Output: "Dutch"

from langdetect import detect_langs

def detect_multiple_languages(text):
    """Detects multiple languages in the given text."""
    try:
        lang_probs = detect_langs(text)  # Returns a list of languages with probabilities
        return [(str(lang.lang), lang.prob) for lang in lang_probs]
    except Exception:
        return [("Unknown", 1.0)]

# Example usage
'''
text = """2025：一個影響世界的漩渦形成...
         YouTube PersAuteursrechtContactCreatorsAdverterenOntwikkelaars"""

detected_languages = detect_multiple_languages(text)
human_readable_languages = [(langcodes.Language.get(lang).display_name(), prob) for lang, prob in detected_languages]

print("Detected Languages:", human_readable_languages)
'''

detected_languages = detect_multiple_languages(clean_text)
human_readable_languages = [(langcodes.Language.get(lang).display_name(), prob) for lang, prob in detected_languages]

print("Detected Languages:", human_readable_languages)

detected_languages = detect_multiple_languages(clean_text[:100])
human_readable_languages = [(langcodes.Language.get(lang).display_name(), prob) for lang, prob in detected_languages]

print("Detected Languages:", human_readable_languages)

"""
Processed Text: 2025：馬斯克的6天才意外曝光，一個影響世界的漩渦形成，下一步，是走向星辰大海的「AI文明」，還是娛樂至死的「美麗新世界」？也許，我們都在見證著這場巨變的開始……|自說自話的總裁 - YouTubeOverPersAuteursrechtContactCreatorsAdverterenOntwikkelaarsVoorwaardenPrivacyBeleid en veiligheidZo werkt YouTubeNieuwe functies testen© 2025 Google LLC YouTube, een bedrijf van Google
Detected Language: nl
Detected Language: Dutch
Detected Languages: [('Dutch', 0.999992619259496)]
Detected Languages: [('Chinese (Taiwan)', 0.8571416780977749), ('Korean', 0.14285830048401382)]
"""
