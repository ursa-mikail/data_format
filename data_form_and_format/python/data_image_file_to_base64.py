import base64
import requests

def fetch_image_and_convert_to_base64(image_url):
    """
    Fetch an image from a repo URL and convert it to a Base64 string.
    
    Args:
        image_url (str): The URL of the image on the repo.
        
    Returns:
        str: Base64-encoded string of the image.
    """
    response = requests.get(image_url)
    if response.status_code == 200:
        image_data = response.content
        return base64.b64encode(image_data).decode('utf-8')
    else:
        raise ValueError(f"Failed to fetch the image. HTTP Status Code: {response.status_code}")

def base64_to_image(base64_string, output_file_path):
    """
    Convert a Base64 string back to an image and save it to a file.
    
    Args:
        base64_string (str): Base64-encoded string of the image.
        output_file_path (str): Path where the image file will be saved.
    """
    image_data = base64.b64decode(base64_string)
    with open(output_file_path, 'wb') as f:
        f.write(image_data)

# Example Usage:
image_url = 'https://raw.githubusercontent.com/ursa-mikail/site_announcement/refs/heads/main/js/aes.js' # path_to_image

try:
    # Convert GitHub image to Base64
    base64_text = fetch_image_and_convert_to_base64(image_url)
    print("Base64 String:")
    print(base64_text)

    # Convert Base64 back to image
    output_path = "output_image.js"
    base64_to_image(base64_text, output_path)
    print(f"Image saved to {output_path}")
except Exception as e:
    print(f"Error: {e}")


"""
Base64 String:
LyoKQ3J5cH...AuX2NyZWF0ZUhlbHBlcihkKX0pKCk7Cg==
Image saved to output_image.js
"""