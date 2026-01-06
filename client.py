"""
Instagram iOS API Client
Ultra-stealthy API client that mimics official Instagram iOS app
"""

import os
import json
import time
import random
import requests
from typing import Optional, Dict, Tuple
from urllib.parse import urlencode
import logging

from device import DeviceGenerator, DeviceFingerprint
from signature import SignatureGenerator, RequestBuilder
from media import MediaProcessor
from timing import HumanTiming, ActivityScheduler, RateLimiter
from constants import API_URL, ENDPOINTS, TLS_CONFIG


class InstagramClient:
    """
    Main Instagram API client with military-grade stealth
    """

    def __init__(
        self,
        username: str,
        password: str,
        device: Optional[DeviceGenerator] = None,
        proxy: Optional[str] = None,
        use_timing: bool = True
    ):
        """
        Initialize Instagram client
        :param username: Instagram username
        :param password: Instagram password
        :param device: Optional pre-configured device
        :param proxy: Optional proxy URL
        :param use_timing: Whether to use human timing simulation
        """
        self.username = username
        self.password = password

        # Device fingerprinting
        self.device = device or DeviceGenerator()
        self.fingerprint = DeviceFingerprint(self.device)

        # Request signing
        self.request_builder = RequestBuilder(
            self.device.device_id,
            self.device.uuid,
            self.device.phone_id
        )

        # Media processing
        self.media_processor = MediaProcessor(self.device.device_name)

        # Timing and rate limiting
        self.use_timing = use_timing
        self.timing = HumanTiming() if use_timing else None
        self.scheduler = ActivityScheduler()
        self.rate_limiter = RateLimiter()

        # Session management
        self.session = self._create_session(proxy)
        self.is_logged_in = False
        self.user_id = None
        self.rank_token = None

        # Logging
        self.logger = logging.getLogger(__name__)

    def _create_session(self, proxy: Optional[str] = None) -> requests.Session:
        """
        Create requests session with iOS TLS fingerprint
        :param proxy: Optional proxy URL
        :return: Configured session
        """
        session = requests.Session()

        # Set proxies if provided
        if proxy:
            session.proxies = {
                'http': proxy,
                'https': proxy
            }

        # Configure TLS to mimic iOS
        # Note: Full TLS fingerprinting requires curl_cffi or similar
        # This is basic configuration
        adapter = requests.adapters.HTTPAdapter(
            max_retries=3,
            pool_connections=10,
            pool_maxsize=10
        )
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        return session

    def _send_request(
        self,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        method: str = "POST",
        extra_headers: Optional[Dict] = None
    ) -> Dict:
        """
        Send API request with full stealth
        :param endpoint: API endpoint
        :param data: Request data
        :param params: URL parameters
        :param method: HTTP method
        :param extra_headers: Additional headers
        :return: Response JSON
        """
        # Rate limiting
        self.rate_limiter.wait_if_needed("request")

        # Human timing
        if self.use_timing and self.timing:
            self.timing.wait_before_action("general")

        # Build URL
        url = f"{API_URL}{endpoint}"

        # Get headers
        headers = self.fingerprint.generate_device_headers(extra_headers)

        # Add session-specific headers if logged in
        if self.is_logged_in:
            headers.update({
                "X-IG-WWW-Claim": self.session.cookies.get("csrftoken", "0"),
            })

        try:
            # Send request
            if method == "POST":
                response = self.session.post(
                    url,
                    data=data,
                    params=params,
                    headers=headers,
                    timeout=30
                )
            else:
                response = self.session.get(
                    url,
                    params=params,
                    headers=headers,
                    timeout=30
                )

            # Parse response
            try:
                response_json = response.json()
            except:
                response_json = {
                    "status": "fail",
                    "message": response.text
                }

            # Check for errors
            if response.status_code != 200:
                self.logger.error(f"Request failed: {response.status_code} - {response_json}")

            return response_json

        except Exception as e:
            self.logger.error(f"Request exception: {e}")
            return {"status": "fail", "message": str(e)}

    def login(self) -> bool:
        """
        Login to Instagram
        :return: True if successful
        """
        self.logger.info(f"Logging in as {self.username}")

        # Human timing for login
        if self.use_timing and self.timing:
            self.timing.wait_before_action("login")

        # Build login payload
        payload = self.request_builder.build_login_payload(
            self.username,
            self.password
        )

        # Send login request
        response = self._send_request(
            ENDPOINTS["LOGIN"],
            data=payload
        )

        # Check response
        if response.get("status") == "ok" or response.get("logged_in_user"):
            self.is_logged_in = True

            # Extract user info
            user = response.get("logged_in_user", {})
            self.user_id = user.get("pk")
            self.rank_token = f"{self.user_id}_{self.device.uuid}"

            self.logger.info(f"Login successful! User ID: {self.user_id}")
            return True
        else:
            self.logger.error(f"Login failed: {response.get('message', 'Unknown error')}")
            return False

    def logout(self) -> bool:
        """
        Logout from Instagram
        :return: True if successful
        """
        if not self.is_logged_in:
            return True

        response = self._send_request(ENDPOINTS["LOGOUT"])

        if response.get("status") == "ok":
            self.is_logged_in = False
            self.logger.info("Logged out successfully")
            return True

        return False

    def upload_photo(
        self,
        image_path: str,
        caption: str = "",
        location: Optional[Dict] = None,
        usertags: Optional[list] = None,
        gps_coords: Optional[Tuple[float, float]] = None
    ) -> Dict:
        """
        Upload photo to Instagram
        :param image_path: Path to image file
        :param caption: Photo caption
        :param location: Location dict with 'name', 'lat', 'lng', 'external_id'
        :param usertags: List of user tags
        :param gps_coords: GPS coordinates for EXIF (lat, lon)
        :return: Response dictionary
        """
        if not self.is_logged_in:
            return {"status": "error", "message": "Not logged in"}

        self.logger.info(f"Uploading photo: {image_path}")

        # Rate limiting for posts
        self.rate_limiter.wait_if_needed("post")

        # Human timing
        if self.use_timing and self.timing:
            self.timing.wait_before_action("post")

        # Generate upload ID
        upload_id = SignatureGenerator.generate_upload_id()

        # Prepare image with EXIF
        self.logger.info("Processing image and adding EXIF metadata...")
        image_bytes = self.media_processor.prepare_for_upload(
            image_path,
            device_model=self.device.device_name,
            gps_coords=gps_coords or (location.get("lat"), location.get("lng")) if location else None
        )

        # Upload photo
        upload_response = self._upload_photo_file(upload_id, image_bytes)

        if upload_response.get("status") != "ok":
            return upload_response

        # Configure photo (finalize upload)
        self.logger.info("Configuring photo...")

        # Simulate typing caption
        if caption and self.use_timing and self.timing:
            typing_delay = self.timing.typing_delay(caption)
            self.logger.info(f"Simulating caption typing ({typing_delay:.1f}s)...")
            time.sleep(typing_delay)

        # Build configure payload
        configure_payload = self.request_builder.build_upload_photo_payload(
            upload_id=upload_id,
            image_data=image_bytes,
            caption=caption,
            location=location,
            usertags=usertags
        )

        # Send configure request
        configure_response = self._send_request(
            ENDPOINTS["CONFIGURE_PHOTO"],
            data=configure_payload
        )

        if configure_response.get("status") == "ok":
            media = configure_response.get("media", {})
            self.logger.info(f"Photo uploaded successfully! Media ID: {media.get('id')}")

        return configure_response

    def _upload_photo_file(self, upload_id: str, image_bytes: bytes) -> Dict:
        """
        Upload photo file to Instagram
        :param upload_id: Upload ID
        :param image_bytes: Image bytes
        :return: Response dict
        """
        # Build upload URL
        url = f"{API_URL}{ENDPOINTS['UPLOAD_PHOTO']}"

        # Build headers
        headers = self.fingerprint.generate_device_headers({
            "X-Entity-Type": "image/jpeg",
            "Offset": "0",
            "X-Instagram-Rupload-Params": json.dumps({
                "media_type": "1",
                "upload_id": upload_id,
                "upload_media_height": "1080",
                "upload_media_width": "1080",
            }, separators=(',', ':')),
        })

        # Remove Content-Type as it will be set by requests
        headers.pop("Content-Type", None)

        # Upload
        response = self.session.post(
            url,
            data=image_bytes,
            headers=headers,
            timeout=60
        )

        try:
            return response.json()
        except:
            return {"status": "fail", "message": response.text}

    def get_timeline(self, max_id: Optional[str] = None) -> Dict:
        """
        Get timeline feed
        :param max_id: Pagination cursor
        :return: Timeline data
        """
        if not self.is_logged_in:
            return {"status": "error", "message": "Not logged in"}

        payload = self.request_builder.build_timeline_payload(max_id)

        return self._send_request(
            ENDPOINTS["TIMELINE"],
            data=payload
        )

    def get_user_info(self, user_id: Optional[str] = None) -> Dict:
        """
        Get user information
        :param user_id: User ID (defaults to self)
        :return: User info
        """
        if not self.is_logged_in:
            return {"status": "error", "message": "Not logged in"}

        uid = user_id or self.user_id
        endpoint = ENDPOINTS["USER_INFO"].format(user_id=uid)

        return self._send_request(endpoint, method="GET")

    def delete_media(self, media_id: str, media_type: str = "PHOTO") -> Dict:
        """
        Delete media
        :param media_id: Media ID to delete
        :param media_type: Media type (PHOTO or VIDEO)
        :return: Response dict
        """
        if not self.is_logged_in:
            return {"status": "error", "message": "Not logged in"}

        endpoint = ENDPOINTS["DELETE_MEDIA"].format(
            media_id=media_id,
            media_type=media_type
        )

        payload = self.request_builder.sig_gen.sign_payload({
            "media_id": media_id
        })

        return self._send_request(endpoint, data=payload)

    def save_session(self, filename: str):
        """
        Save session to file for reuse
        :param filename: Output filename
        """
        session_data = {
            "username": self.username,
            "cookies": self.session.cookies.get_dict(),
            "device": self.device.get_device_dict(),
            "user_id": self.user_id,
            "rank_token": self.rank_token,
        }

        with open(filename, 'w') as f:
            json.dump(session_data, f, indent=2)

        self.logger.info(f"Session saved to {filename}")

    @classmethod
    def load_session(cls, filename: str, password: str) -> 'InstagramClient':
        """
        Load session from file
        :param filename: Session filename
        :param password: Account password
        :return: InstagramClient instance
        """
        with open(filename, 'r') as f:
            session_data = json.load(f)

        # Recreate device
        device = DeviceGenerator()
        device.device_id = session_data["device"]["device_id"]
        device.phone_id = session_data["device"]["phone_id"]
        device.uuid = session_data["device"]["uuid"]
        device.advertising_id = session_data["device"]["advertising_id"]
        device.device_model = session_data["device"]["device_model"]
        device.device_name = session_data["device"]["device_name"]
        device.ios_version = session_data["device"]["ios_version"]
        device.app_version = session_data["device"]["app_version"]
        device.device_settings = session_data["device"]["settings"]

        # Create client
        client = cls(
            username=session_data["username"],
            password=password,
            device=device
        )

        # Restore session
        for key, value in session_data["cookies"].items():
            client.session.cookies.set(key, value)

        client.is_logged_in = True
        client.user_id = session_data.get("user_id")
        client.rank_token = session_data.get("rank_token")

        return client
