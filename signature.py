"""
Request Signature Generator
Generates cryptographic signatures identical to Instagram iOS app
"""

import hmac
import hashlib
import json
import time
import random
import uuid
from typing import Dict, Any
from urllib.parse import quote


class SignatureGenerator:
    """
    Generates Instagram API request signatures
    Critical for request authentication
    """

    # Instagram's signature key (extracted from iOS binary)
    # Updated from hiflybo/Instagram_Private_Api_Ios (v397.1) - ACTUAL signature key
    SIG_KEY = "23966c53a485abc8a46056e59953606212796f430df44d03b1024a9403373fd7"
    SIG_KEY_VERSION = "4"

    def __init__(self):
        self.session_id = str(uuid.uuid4())

    @staticmethod
    def generate_signature(data: str) -> str:
        """
        Generate HMAC-SHA256 signature for request payload
        :param data: JSON payload as string
        :return: Hex signature
        """
        body = data.encode('utf-8')
        signature = hmac.new(
            SignatureGenerator.SIG_KEY.encode('utf-8'),
            body,
            hashlib.sha256
        ).hexdigest()

        return signature

    @staticmethod
    def sign_payload(payload: Dict[str, Any]) -> Dict[str, str]:
        """
        Sign a payload dictionary
        :param payload: Dictionary to sign
        :return: Dictionary with signed_body and ig_sig_key_version
        """
        # Convert payload to JSON (compact, sorted keys for consistency)
        json_data = json.dumps(payload, separators=(',', ':'), sort_keys=True)

        # Generate signature
        signature = SignatureGenerator.generate_signature(json_data)

        # Return signed body format that Instagram expects
        return {
            "signed_body": f"SIGNATURE.{json_data}",
            "ig_sig_key_version": SignatureGenerator.SIG_KEY_VERSION
        }

    @staticmethod
    def generate_uuid(uuid_type: str = 'v4') -> str:
        """
        Generate UUID in Instagram format
        :param uuid_type: Type of UUID to generate
        :return: UUID string
        """
        if uuid_type == 'v4':
            return str(uuid.uuid4())
        else:
            # For some endpoints, Instagram uses time-based UUIDs
            return str(uuid.uuid1())

    @staticmethod
    def generate_upload_id(timestamp: bool = True) -> str:
        """
        Generate upload ID for media uploads
        :param timestamp: Whether to use timestamp-based ID
        :return: Upload ID string
        """
        if timestamp:
            return str(int(time.time() * 1000))
        else:
            return str(random.randint(1000000000000000, 9999999999999999))

    @staticmethod
    def generate_client_context() -> str:
        """
        Generate client_context for GraphQL requests
        :return: Client context as JSON string
        """
        context = {
            "bloks_version": "7c3f94b1168c7de88c8b1e754f308f1a3c48ddb3e1a5c07cd03bb19e2a3b6f23",
            "styles_id": "instagram",
        }
        return json.dumps(context, separators=(',', ':'))

    @staticmethod
    def generate_device_id() -> str:
        """Generate device ID in Instagram iOS format"""
        return f"ios-{uuid.uuid4().hex[:16]}"

    @staticmethod
    def generate_phone_id() -> str:
        """Generate phone ID"""
        return str(uuid.uuid4())

    @staticmethod
    def generate_waterfall_id() -> str:
        """Generate waterfall ID for tracking"""
        return str(uuid.uuid4())

    @staticmethod
    def generate_guid() -> str:
        """Generate GUID"""
        return str(uuid.uuid4())


class RequestBuilder:
    """
    Builds requests with proper formatting and signatures
    """

    def __init__(self, device_id: str, uuid: str, phone_id: str):
        self.device_id = device_id
        self.uuid = uuid
        self.phone_id = phone_id
        self.sig_gen = SignatureGenerator()

    def build_login_payload(self, username: str, password: str) -> Dict:
        """
        Build login request payload
        :param username: Instagram username
        :param password: Instagram password
        :return: Complete payload ready to send
        """
        payload = {
            "jazoest": self._generate_jazoest(self.phone_id),
            "country_codes": '[{"country_code":"1","source":["default"]}]',
            "phone_id": self.phone_id,
            "enc_password": f"#PWD_INSTAGRAM:0:{int(time.time())}:{password}",
            "username": username,
            "adid": str(uuid.uuid4()),
            "guid": self.uuid,
            "device_id": self.device_id,
            "google_tokens": "[]",
            "login_attempt_count": "0",
        }

        return self.sig_gen.sign_payload(payload)

    def build_upload_photo_payload(
        self,
        upload_id: str,
        image_data: bytes,
        caption: str = "",
        location: Dict = None,
        usertags: list = None,
    ) -> Dict:
        """
        Build photo upload configuration payload
        :param upload_id: Upload ID
        :param image_data: Image bytes
        :param caption: Photo caption
        :param location: Location data
        :param usertags: User tags
        :return: Configuration payload
        """
        payload = {
            "upload_id": upload_id,
            "caption": caption,
            "usertags": json.dumps(usertags) if usertags else "[]",
            "custom_accessibility_caption": "",
            "retry_timeout": "0",
            "source_type": "4",  # 4 = camera
            "device": {
                "manufacturer": "Apple",
                "model": "iPhone",
                "android_version": None,
                "android_release": None
            },
            "edits": {
                "crop_original_size": [1080.0, 1080.0],
                "crop_center": [0.0, 0.0],
                "crop_zoom": 1.0
            },
            "extra": {
                "source_width": 1080,
                "source_height": 1080
            }
        }

        # Add location if provided
        if location:
            payload["location"] = json.dumps(location)
            payload["geotag_enabled"] = "1"
            payload["media_latitude"] = str(location.get("lat", "0.0"))
            payload["media_longitude"] = str(location.get("lng", "0.0"))
            payload["posting_latitude"] = str(location.get("lat", "0.0"))
            payload["posting_longitude"] = str(location.get("lng", "0.0"))

        # Add timestamps
        payload["date_time_original"] = time.strftime("%Y%m%dT%H%M%S.000Z", time.gmtime())
        payload["timezone_offset"] = str(random.choice([-28800, -25200, -21600, -18000]))

        return self.sig_gen.sign_payload(payload)

    def build_timeline_payload(self, max_id: str = None) -> Dict:
        """
        Build timeline request payload
        :param max_id: Pagination cursor
        :return: Timeline payload
        """
        payload = {
            "is_prefetch": "0",
            "feed_view_info": "[]",
            "seen_posts": "[]",
            "phone_id": self.phone_id,
            "battery_level": str(random.randint(20, 95)),
            "timezone_offset": str(random.choice([-28800, -25200, -21600, -18000])),
            "is_charging": str(random.randint(0, 1)),
            "will_sound_on": "1",
            "is_on_wifi": "true",
            "is_async_ads_in_headload_enabled": "0",
            "rti_delivery_backend": "0",
            "is_async_ads_double_request": "0",
            "is_async_ads_rti": "0",
        }

        if max_id:
            payload["max_id"] = max_id
            payload["reason"] = "pagination"

        return self.sig_gen.sign_payload(payload)

    @staticmethod
    def _generate_jazoest(phone_id: str) -> str:
        """
        Generate jazoest parameter from phone_id
        :param phone_id: Phone ID
        :return: Jazoest string
        """
        char_sum = sum(ord(c) for c in phone_id)
        return f"2{char_sum}"

    def build_media_configure_payload(self, upload_id: str, caption: str = "") -> Dict:
        """
        Build media configuration payload for finalizing upload
        :param upload_id: Upload ID
        :param caption: Media caption
        :return: Configuration payload
        """
        payload = {
            "upload_id": upload_id,
            "caption": caption,
            "source_type": "4",
            "camera_position": "back",
            "creation_logger_session_id": str(uuid.uuid4()),
            "device": {
                "manufacturer": "Apple",
                "model": "iPhone",
                "ios_version": "17.2",
                "ios_release": "17.2"
            },
            "edits": {
                "crop_original_size": [1080.0, 1080.0],
                "crop_center": [0.0, 0.0],
                "crop_zoom": 1.0
            },
            "extra": {
                "source_width": 1080,
                "source_height": 1080
            }
        }

        return self.sig_gen.sign_payload(payload)
