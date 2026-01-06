"""
Advanced Device Fingerprinting Module
Generates realistic iOS device fingerprints that are indistinguishable from real devices
"""

import uuid
import random
import hashlib
import hmac
import json
from typing import Dict, Optional
from constants import DEVICE_MODELS, IOS_VERSIONS, APP_VERSIONS, DEVICE_SETTINGS_PRESETS


class DeviceGenerator:
    """
    Generates and manages realistic iOS device fingerprints
    Uses actual device patterns from real iPhones
    """

    def __init__(self, seed: Optional[str] = None):
        """
        Initialize device generator
        :param seed: Optional seed for reproducible device generation
        """
        self.seed = seed
        if seed:
            random.seed(seed)

        self.device_id = None
        self.phone_id = None
        self.uuid = None
        self.advertising_id = None
        self.device_model = None
        self.device_name = None
        self.ios_version = None
        self.app_version = None
        self.device_settings = None

        self._generate_device()

    def _generate_device(self):
        """Generate complete device fingerprint"""
        # Select device model
        self.device_model, self.device_name = random.choice(DEVICE_MODELS)

        # Select iOS version
        self.ios_version = random.choice(IOS_VERSIONS)

        # Select app version
        self.app_version = random.choice(APP_VERSIONS)

        # Generate UUIDs - iOS format
        self.uuid = str(uuid.uuid4()).upper()
        self.phone_id = str(uuid.uuid4()).upper()
        self.advertising_id = str(uuid.uuid4()).upper()

        # Generate device ID (Instagram's internal device identifier)
        # Format: android-<16 hex chars>
        # Even though it says "android", iOS clients also use this format
        self.device_id = f"ios-{uuid.uuid4().hex[:16]}"

        # Select device settings preset
        preset_name = self._get_preset_name()
        self.device_settings = DEVICE_SETTINGS_PRESETS.get(
            preset_name,
            DEVICE_SETTINGS_PRESETS["iPhone15Pro"]
        )

    def _get_preset_name(self) -> str:
        """Map device model to preset name"""
        if "iPhone 15 Pro Max" in self.device_name:
            return "iPhone15ProMax"
        elif "iPhone 15 Pro" in self.device_name:
            return "iPhone15Pro"
        elif "iPhone 14 Pro" in self.device_name:
            return "iPhone14Pro"
        else:
            return "iPhone15Pro"

    def get_user_agent(self) -> str:
        """Generate realistic User-Agent string"""
        ios_ver_formatted = self.ios_version.replace('.', '_')

        return (
            f"Instagram {self.app_version} "
            f"(iPhone; iOS {self.ios_version}; {ios_ver_formatted}; "
            f"Apple; {self.device_model}; {self.device_name}; en_US; en-US; "
            f"scale={self.device_settings['screen_density']}; "
            f"{self.device_settings['screen_resolution']}; "
            f"{self.app_version.split('.')[0]})"
        )

    def get_device_dict(self) -> Dict:
        """Get complete device information as dictionary"""
        return {
            "device_id": self.device_id,
            "phone_id": self.phone_id,
            "uuid": self.uuid,
            "advertising_id": self.advertising_id,
            "device_model": self.device_model,
            "device_name": self.device_name,
            "ios_version": self.ios_version,
            "app_version": self.app_version,
            "user_agent": self.get_user_agent(),
            "settings": self.device_settings
        }

    def generate_device_string(self) -> str:
        """
        Generate device string for API requests
        Format matches Instagram iOS app exactly
        """
        device_dict = {
            "manufacturer": self.device_settings["manufacturer"],
            "model": self.device_settings["model"],
            "ios_version": self.ios_version,
            "ios_release": self.ios_version,
        }
        return json.dumps(device_dict, separators=(',', ':'))

    def get_battery_level(self) -> int:
        """Generate realistic battery level (20-95%)"""
        return random.randint(20, 95)

    def get_is_charging(self) -> bool:
        """Randomly determine if device is charging"""
        return random.choice([True, False])

    def get_timezone_offset(self) -> str:
        """Generate timezone offset (typically -5 to -8 for US)"""
        offsets = ["-28800", "-25200", "-21600", "-18000"]  # PST, MST, CST, EST
        return random.choice(offsets)

    def get_network_type(self) -> str:
        """Get network type (WiFi more common than cellular for posting)"""
        return random.choices(
            ["WIFI", "MOBILE(LTE)"],
            weights=[0.7, 0.3],
            k=1
        )[0]

    def save_to_file(self, filename: str):
        """Save device fingerprint to file for reuse"""
        import json
        with open(filename, 'w') as f:
            json.dump(self.get_device_dict(), f, indent=2)

    @staticmethod
    def load_from_file(filename: str) -> 'DeviceGenerator':
        """Load device fingerprint from file"""
        import json
        with open(filename, 'r') as f:
            data = json.load(f)

        device = DeviceGenerator()
        device.device_id = data['device_id']
        device.phone_id = data['phone_id']
        device.uuid = data['uuid']
        device.advertising_id = data['advertising_id']
        device.device_model = data['device_model']
        device.device_name = data['device_name']
        device.ios_version = data['ios_version']
        device.app_version = data['app_version']
        device.device_settings = data['settings']

        return device


class DeviceFingerprint:
    """
    Advanced device fingerprinting that mimics iOS device characteristics
    """

    def __init__(self, device: DeviceGenerator):
        self.device = device

    def generate_clientcontext(self) -> str:
        """
        Generate client_context JSON
        This is critical for Instagram to accept the request as legitimate
        """
        context = {
            "bloks_version": "7c3f94b1168c7de88c8b1e754f308f1a3c48ddb3e1a5c07cd03bb19e2a3b6f23",
            "styles_id": "instagram",
            "app_id": "567067343352427",
            "app_version": self.device.app_version,
            "build_num": self.device.app_version.split('.')[0],
            "device_id": self.device.uuid,
            "family_device_id": self.device.phone_id,
            "session_id": str(uuid.uuid4()),
            "machine_id": self.device.device_id,
        }
        return json.dumps(context, separators=(',', ':'))

    def generate_jazoest(self, phone_id: str) -> str:
        """
        Generate jazoest parameter
        Instagram uses this for request validation
        """
        # Sum of phone_id character codes
        char_sum = sum(ord(c) for c in phone_id)
        return f"2{char_sum}"

    def generate_device_headers(self, additional_headers: Optional[Dict] = None) -> Dict:
        """
        Generate complete set of headers that mimic iOS Instagram app
        """
        headers = {
            "User-Agent": self.device.get_user_agent(),
            "X-Pigeon-Session-Id": str(uuid.uuid4()),
            "X-Pigeon-Rawclienttime": str(random.uniform(1700000000.0, 1800000000.0)),
            "X-IG-Connection-Type": self.device.get_network_type(),
            "X-IG-Capabilities": "3brTv10=",
            "X-IG-App-ID": "567067343352427",
            "X-IG-Device-ID": self.device.uuid,
            "X-IG-Bandwidth-Speed-KBPS": str(random.randint(2000, 8000)),
            "X-IG-Bandwidth-TotalBytes-B": str(random.randint(5000000, 15000000)),
            "X-IG-Bandwidth-TotalTime-MS": str(random.randint(200, 800)),
            "X-IG-EU-DC-ENABLED": "true",
            "X-IG-Extended-CDN-Thumbnail-Cache-Busting-Value": str(random.randint(1000, 9999)),
            "X-IG-WWW-Claim": "0",
            "X-Bloks-Version-Id": "7c3f94b1168c7de88c8b1e754f308f1a3c48ddb3e1a5c07cd03bb19e2a3b6f23",
            "X-IG-Device-Locale": "en_US",
            "X-IG-Mapped-Locale": "en_US",
            "X-IG-Connection-Speed": f"{random.randint(1000, 3000)}kbps",
            "X-IG-ABR-Connection-Speed-KBPS": str(random.randint(2000, 5000)),
            "X-FB-HTTP-Engine": "Liger",
            "X-FB-Client-IP": "True",
            "X-FB-Server-Cluster": "True",
            "Accept-Language": "en-US",
            "Accept-Encoding": "gzip, deflate",
            "Accept": "*/*",
            "Connection": "keep-alive",
        }

        if additional_headers:
            headers.update(additional_headers)

        return headers
