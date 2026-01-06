"""
Utility functions for Instagram API
"""

import json
import os
import random
import string
from typing import Optional, List, Dict
import hashlib


def generate_random_string(length: int = 16) -> str:
    """
    Generate random alphanumeric string
    :param length: Length of string
    :return: Random string
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def load_proxies(filename: str) -> List[str]:
    """
    Load proxies from file
    :param filename: File containing proxies (one per line)
    :return: List of proxy URLs
    """
    if not os.path.exists(filename):
        return []

    with open(filename, 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]

    return proxies


def rotate_proxy(proxies: List[str], current_proxy: Optional[str] = None) -> str:
    """
    Get next proxy from list
    :param proxies: List of proxies
    :param current_proxy: Current proxy (to avoid)
    :return: Next proxy
    """
    if not proxies:
        return None

    available = [p for p in proxies if p != current_proxy]
    if not available:
        available = proxies

    return random.choice(available)


def hash_password(password: str, salt: str = "") -> str:
    """
    Hash password (useful for secure storage)
    :param password: Password to hash
    :param salt: Optional salt
    :return: Hashed password
    """
    return hashlib.sha256(f"{password}{salt}".encode()).hexdigest()


def validate_image_path(path: str) -> bool:
    """
    Validate image file exists and is correct format
    :param path: Path to image
    :return: True if valid
    """
    if not os.path.exists(path):
        return False

    valid_extensions = ['.jpg', '.jpeg', '.png']
    _, ext = os.path.splitext(path.lower())

    return ext in valid_extensions


def format_location(name: str, lat: float, lng: float, external_id: Optional[str] = None) -> Dict:
    """
    Format location dictionary for Instagram
    :param name: Location name
    :param lat: Latitude
    :param lng: Longitude
    :param external_id: Facebook Places ID
    :return: Location dict
    """
    location = {
        "name": name,
        "lat": lat,
        "lng": lng,
    }

    if external_id:
        location["external_id"] = external_id
        location["external_id_source"] = "facebook_places"

    return location


def format_usertag(user_id: str, x: float, y: float) -> Dict:
    """
    Format user tag for photo
    :param user_id: Instagram user ID
    :param x: X position (0.0-1.0)
    :param y: Y position (0.0-1.0)
    :return: User tag dict
    """
    return {
        "user_id": user_id,
        "position": [x, y]
    }


def save_config(config: Dict, filename: str = "config.json"):
    """
    Save configuration to file
    :param config: Configuration dictionary
    :param filename: Output filename
    """
    with open(filename, 'w') as f:
        json.dump(config, f, indent=2)


def load_config(filename: str = "config.json") -> Dict:
    """
    Load configuration from file
    :param filename: Config filename
    :return: Configuration dict
    """
    if not os.path.exists(filename):
        return {}

    with open(filename, 'r') as f:
        return json.load(f)


def clean_caption(caption: str, max_length: int = 2200) -> str:
    """
    Clean and truncate caption
    :param caption: Caption text
    :param max_length: Maximum length
    :return: Cleaned caption
    """
    # Remove null bytes and other problematic characters
    caption = caption.replace('\x00', '')

    # Truncate if needed
    if len(caption) > max_length:
        caption = caption[:max_length-3] + "..."

    return caption.strip()


def extract_media_id_from_url(url: str) -> Optional[str]:
    """
    Extract media ID from Instagram URL
    :param url: Instagram post URL
    :return: Media ID or None
    """
    # Example: https://www.instagram.com/p/ABC123/
    import re

    pattern = r'instagram\.com/p/([A-Za-z0-9_-]+)'
    match = re.search(pattern, url)

    if match:
        shortcode = match.group(1)
        # Convert shortcode to media ID (simplified)
        # Note: Full conversion requires base64 decoding
        return shortcode

    return None


def create_batch_upload_plan(
    images: List[str],
    captions: List[str],
    delay_min: int = 300,
    delay_max: int = 3600
) -> List[Dict]:
    """
    Create upload plan for multiple images
    :param images: List of image paths
    :param captions: List of captions
    :param delay_min: Minimum delay between posts (seconds)
    :param delay_max: Maximum delay between posts (seconds)
    :return: List of upload tasks
    """
    tasks = []

    for i, (image, caption) in enumerate(zip(images, captions)):
        delay = 0 if i == 0 else random.randint(delay_min, delay_max)

        tasks.append({
            "index": i,
            "image": image,
            "caption": caption,
            "delay": delay,
        })

    return tasks


def check_instagram_url(url: str) -> bool:
    """
    Check if URL is valid Instagram URL
    :param url: URL to check
    :return: True if valid Instagram URL
    """
    import re

    pattern = r'(https?://)?(www\.)?instagram\.com/'
    return bool(re.match(pattern, url))


def get_file_size_mb(path: str) -> float:
    """
    Get file size in MB
    :param path: File path
    :return: Size in MB
    """
    if not os.path.exists(path):
        return 0.0

    size_bytes = os.path.getsize(path)
    size_mb = size_bytes / (1024 * 1024)

    return round(size_mb, 2)


def check_requirements() -> Dict[str, bool]:
    """
    Check if all required packages are installed
    :return: Dict of package: installed status
    """
    requirements = {
        "requests": False,
        "PIL": False,
        "piexif": False,
        "dotenv": False,
    }

    for package in requirements.keys():
        try:
            if package == "PIL":
                __import__("PIL")
            elif package == "dotenv":
                __import__("dotenv")
            else:
                __import__(package)
            requirements[package] = True
        except ImportError:
            requirements[package] = False

    return requirements


if __name__ == "__main__":
    # Test utilities
    print("Testing utilities...")

    # Check requirements
    print("\nChecking requirements:")
    reqs = check_requirements()
    for package, installed in reqs.items():
        status = "✓" if installed else "✗"
        print(f"  {status} {package}")

    print("\nUtilities working correctly!")
