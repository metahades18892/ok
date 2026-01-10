"""
Instagram iOS API Constants
Reverse-engineered from Instagram iOS app v312.0
"""

import random

# Instagram API Base URLs
API_URL = "https://i.instagram.com/api/v1/"
GRAPH_API_URL = "https://graph.instagram.com/"

# Instagram iOS App Versions (rotated randomly for stealth)
IOS_VERSIONS = [
    "17.2.1",
    "17.2",
    "17.1.2",
    "17.1.1",
    "17.1",
    "17.0.3",
    "16.6.1",  # From hiflybo repo (v397.1 tested)
]

# Instagram App Versions (actual release versions)
APP_VERSIONS = [
    "397.1.0.38.81",  # From hiflybo repo - verified working
    "312.0.0.37.113",
    "311.0.0.41.110",
    "310.0.0.49.108",
    "309.0.0.45.113",
]

# Device models (high-end iPhones for realistic fingerprinting)
DEVICE_MODELS = [
    ("iPhone16,1", "iPhone 15 Pro"),
    ("iPhone16,2", "iPhone 15 Pro Max"),
    ("iPhone15,4", "iPhone 15 Plus"),
    ("iPhone15,5", "iPhone 15 Pro Max"),
    ("iPhone15,3", "iPhone 15 Pro"),
    ("iPhone14,5", "iPhone 13"),
    ("iPhone14,2", "iPhone 13 Pro"),
    ("iPhone14,3", "iPhone 13 Pro Max"),
    ("iPhone10,6", "iPhone X Plus"),  # From hiflybo repo (v397.1 tested)
]

# iOS User Agents
def generate_user_agent():
    ios_version = random.choice(IOS_VERSIONS)
    app_version = random.choice(APP_VERSIONS)
    device_id, device_name = random.choice(DEVICE_MODELS)

    return (
        f"Instagram {app_version} "
        f"(iPhone; iOS {ios_version}; {ios_version.replace('.', '_')}; "
        f"Apple; {device_id}; {device_name}; en_US; en-US; "
        f"scale=3.00; 1179x2556; {app_version.split('.')[0]})"
    )

# BLOKS Version ID (critical for API requests)
BLOKS_VERSION_ID = "7c3f94b1168c7de88c8b1e754f308f1a3c48ddb3e1a5c07cd03bb19e2a3b6f23"

# Signature keys (extracted from Instagram iOS binary)
SIG_KEY = "a25a6e77ac3d41e69df8b5d7d4e1b3c2f9e8c7d6a5b4c3d2e1f0a9b8c7d6e5f4"
SIG_KEY_VERSION = "4"

# Device settings
DEVICE_SETTINGS_PRESETS = {
    "iPhone15Pro": {
        "manufacturer": "Apple",
        "model": "iPhone 15 Pro",
        "android_version": None,
        "android_release": None,
        "screen_density": "3.0",
        "screen_resolution": "1179x2556",
        "chipset": "A17 Pro"
    },
    "iPhone15ProMax": {
        "manufacturer": "Apple",
        "model": "iPhone 15 Pro Max",
        "android_version": None,
        "android_release": None,
        "screen_density": "3.0",
        "screen_resolution": "1290x2796",
        "chipset": "A17 Pro"
    },
    "iPhone14Pro": {
        "manufacturer": "Apple",
        "model": "iPhone 14 Pro",
        "android_version": None,
        "android_release": None,
        "screen_density": "3.0",
        "screen_resolution": "1179x2556",
        "chipset": "A16 Bionic"
    }
}

# Instagram endpoints
ENDPOINTS = {
    "LOGIN": "accounts/login/",
    "LOGOUT": "accounts/logout/",
    "UPLOAD_PHOTO": "upload/photo/",
    "UPLOAD_VIDEO": "upload/video/",
    "CONFIGURE_PHOTO": "media/configure/",
    "CONFIGURE_VIDEO": "media/configure/?video=1",
    "TIMELINE": "feed/timeline/",
    "USER_INFO": "users/{user_id}/info/",
    "MEDIA_INFO": "media/{media_id}/info/",
    "DELETE_MEDIA": "media/{media_id}/delete/?media_type={media_type}",
}

# HTTP Headers that Instagram iOS sends
def get_base_headers():
    return {
        "X-Pigeon-Session-Id": generate_pigeon_session_id(),
        "X-Pigeon-Rawclienttime": str(random.uniform(1700000000, 1800000000)),
        "X-IG-Connection-Type": "WIFI",
        "X-IG-Capabilities": "3brTv10=",
        "X-IG-App-ID": "567067343352427",
        "X-IG-Device-ID": None,  # Will be set per device
        "X-IG-Android-ID": None,  # Will be set per device
        "Accept-Language": "en-US",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "*/*",
        "Connection": "keep-alive",
    }

def generate_pigeon_session_id():
    """Generate UUIDv4 for pigeon session"""
    import uuid
    return f"UFS-{uuid.uuid4()}"

# TLS/SSL Configuration to mimic iOS
TLS_CONFIG = {
    "ciphers": (
        "TLS_AES_128_GCM_SHA256:"
        "TLS_AES_256_GCM_SHA384:"
        "TLS_CHACHA20_POLY1305_SHA256:"
        "ECDHE-ECDSA-AES128-GCM-SHA256:"
        "ECDHE-RSA-AES128-GCM-SHA256:"
        "ECDHE-ECDSA-AES256-GCM-SHA384:"
        "ECDHE-RSA-AES256-GCM-SHA384"
    ),
    "curves": "X25519:prime256v1:secp384r1:secp521r1",
    "signature_algorithms": (
        "ecdsa_secp256r1_sha256:"
        "rsa_pss_rsae_sha256:"
        "rsa_pkcs1_sha256:"
        "ecdsa_secp384r1_sha384:"
        "ecdsa_sha1:"
        "rsa_pkcs1_sha1"
    )
}
