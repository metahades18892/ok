"""
Media Processing Module
Handles image/video processing with realistic EXIF metadata injection
Makes uploaded media indistinguishable from real iPhone photos
"""

import io
import os
import random
import time
from datetime import datetime, timedelta
from typing import Tuple, Optional, Dict
from PIL import Image, ImageOps
import piexif
from piexif import GPSIFD, ImageIFD, ExifIFD


class MediaProcessor:
    """
    Processes media files to add realistic iPhone metadata
    """

    # iPhone camera models that match our device fingerprints
    IPHONE_MODELS = [
        "iPhone 15 Pro",
        "iPhone 15 Pro Max",
        "iPhone 14 Pro",
        "iPhone 14 Pro Max",
        "iPhone 13 Pro",
        "iPhone 13 Pro Max",
    ]

    # Realistic iPhone camera settings
    CAMERA_SETTINGS = {
        "iPhone 15 Pro": {
            "Make": "Apple",
            "Model": "iPhone 15 Pro",
            "LensMake": "Apple",
            "LensModel": "iPhone 15 Pro back triple camera 6.86mm f/1.78",
            "FocalLength": (686, 100),  # 6.86mm
            "FNumber": (178, 100),  # f/1.78
            "ISOSpeedRatings": [50, 64, 80, 100, 125, 160, 200, 250, 320, 400],
            "ExposureTime": [(1, 120), (1, 60), (1, 30), (1, 15)],
        },
        "iPhone 15 Pro Max": {
            "Make": "Apple",
            "Model": "iPhone 15 Pro Max",
            "LensMake": "Apple",
            "LensModel": "iPhone 15 Pro Max back triple camera 6.86mm f/1.78",
            "FocalLength": (686, 100),
            "FNumber": (178, 100),
            "ISOSpeedRatings": [50, 64, 80, 100, 125, 160, 200, 250, 320, 400],
            "ExposureTime": [(1, 120), (1, 60), (1, 30), (1, 15)],
        },
        "iPhone 14 Pro": {
            "Make": "Apple",
            "Model": "iPhone 14 Pro",
            "LensMake": "Apple",
            "LensModel": "iPhone 14 Pro back triple camera 6.86mm f/1.78",
            "FocalLength": (686, 100),
            "FNumber": (178, 100),
            "ISOSpeedRatings": [32, 40, 50, 64, 80, 100, 125, 160, 200, 250],
            "ExposureTime": [(1, 100), (1, 50), (1, 25), (1, 12)],
        }
    }

    def __init__(self, device_model: str = "iPhone 15 Pro"):
        """
        Initialize media processor
        :param device_model: iPhone model to simulate
        """
        self.device_model = device_model
        self.camera_settings = self.CAMERA_SETTINGS.get(
            device_model,
            self.CAMERA_SETTINGS["iPhone 15 Pro"]
        )

    def add_iphone_exif(
        self,
        image_path: str,
        output_path: Optional[str] = None,
        gps_coords: Optional[Tuple[float, float]] = None,
        capture_time: Optional[datetime] = None
    ) -> str:
        """
        Add realistic iPhone EXIF data to image
        :param image_path: Path to input image
        :param output_path: Path to save output (if None, overwrites input)
        :param gps_coords: Optional GPS coordinates (latitude, longitude)
        :param capture_time: Optional capture time (defaults to recent random time)
        :return: Path to output file
        """
        if output_path is None:
            output_path = image_path

        # Open image
        img = Image.open(image_path)

        # Auto-rotate based on EXIF orientation
        img = ImageOps.exif_transpose(img)

        # Generate EXIF data
        exif_dict = self._generate_exif_dict(
            img.size,
            gps_coords,
            capture_time
        )

        # Convert to bytes
        exif_bytes = piexif.dump(exif_dict)

        # Save with EXIF
        img.save(output_path, exif=exif_bytes, quality=95, optimize=True)

        return output_path

    def _generate_exif_dict(
        self,
        image_size: Tuple[int, int],
        gps_coords: Optional[Tuple[float, float]],
        capture_time: Optional[datetime]
    ) -> Dict:
        """
        Generate complete EXIF dictionary
        :param image_size: Image dimensions (width, height)
        :param gps_coords: GPS coordinates
        :param capture_time: Capture time
        :return: EXIF dictionary
        """
        if capture_time is None:
            # Random time in last 24 hours
            hours_ago = random.uniform(0.5, 24)
            capture_time = datetime.now() - timedelta(hours=hours_ago)

        # Format datetime strings
        datetime_str = capture_time.strftime("%Y:%m:%d %H:%M:%S")

        # Build EXIF dict
        exif_dict = {
            "0th": {},
            "Exif": {},
            "GPS": {},
            "1st": {},
            "thumbnail": None,
        }

        # 0th IFD (Image)
        exif_dict["0th"] = {
            ImageIFD.Make: self.camera_settings["Make"].encode('utf-8'),
            ImageIFD.Model: self.camera_settings["Model"].encode('utf-8'),
            ImageIFD.Orientation: 1,
            ImageIFD.XResolution: (72, 1),
            ImageIFD.YResolution: (72, 1),
            ImageIFD.ResolutionUnit: 2,
            ImageIFD.Software: b"17.2.1",  # iOS version
            ImageIFD.DateTime: datetime_str.encode('utf-8'),
            ImageIFD.YCbCrPositioning: 1,
        }

        # Exif IFD
        exif_dict["Exif"] = {
            ExifIFD.ExposureTime: random.choice(self.camera_settings["ExposureTime"]),
            ExifIFD.FNumber: self.camera_settings["FNumber"],
            ExifIFD.ExposureProgram: 2,  # Normal program
            ExifIFD.ISOSpeedRatings: random.choice(self.camera_settings["ISOSpeedRatings"]),
            ExifIFD.ExifVersion: b"0232",
            ExifIFD.DateTimeOriginal: datetime_str.encode('utf-8'),
            ExifIFD.DateTimeDigitized: datetime_str.encode('utf-8'),
            ExifIFD.ComponentsConfiguration: b"\x01\x02\x03\x00",
            ExifIFD.ShutterSpeedValue: (random.randint(400, 800), 100),
            ExifIFD.ApertureValue: (170, 100),
            ExifIFD.BrightnessValue: (random.randint(200, 600), 100),
            ExifIFD.ExposureBiasValue: (0, 1),
            ExifIFD.MeteringMode: 5,  # Pattern
            ExifIFD.Flash: random.choice([16, 24, 32]),  # Flash settings
            ExifIFD.FocalLength: self.camera_settings["FocalLength"],
            ExifIFD.SubjectArea: (
                image_size[0] // 2,
                image_size[1] // 2,
                random.randint(800, 1200),
                random.randint(800, 1200)
            ),
            ExifIFD.SubSecTimeOriginal: str(random.randint(100, 999)).encode('utf-8'),
            ExifIFD.SubSecTimeDigitized: str(random.randint(100, 999)).encode('utf-8'),
            ExifIFD.ColorSpace: 65535,  # Uncalibrated
            ExifIFD.PixelXDimension: image_size[0],
            ExifIFD.PixelYDimension: image_size[1],
            ExifIFD.SensingMethod: 2,  # One-chip color area sensor
            ExifIFD.SceneType: b"\x01",
            ExifIFD.ExposureMode: 0,  # Auto exposure
            ExifIFD.WhiteBalance: 0,  # Auto white balance
            ExifIFD.FocalLengthIn35mmFilm: 26,
            ExifIFD.SceneCaptureType: 0,  # Standard
            ExifIFD.LensSpecification: ((417, 100), (900, 100), (178, 100), (28, 10)),
            ExifIFD.LensMake: self.camera_settings["LensMake"].encode('utf-8'),
            ExifIFD.LensModel: self.camera_settings["LensModel"].encode('utf-8'),
        }

        # GPS data if provided
        if gps_coords:
            lat, lon = gps_coords
            exif_dict["GPS"] = self._generate_gps_ifd(lat, lon, capture_time)

        return exif_dict

    def _generate_gps_ifd(
        self,
        latitude: float,
        longitude: float,
        timestamp: datetime
    ) -> Dict:
        """
        Generate GPS IFD data
        :param latitude: Latitude in decimal degrees
        :param longitude: Longitude in decimal degrees
        :param timestamp: Timestamp for GPS
        :return: GPS IFD dictionary
        """
        # Convert decimal degrees to degrees, minutes, seconds
        lat_deg = self._to_deg(latitude, ["S", "N"])
        lon_deg = self._to_deg(longitude, ["W", "E"])

        # GPS timestamp
        gps_time = (
            (timestamp.hour, 1),
            (timestamp.minute, 1),
            (timestamp.second, 1)
        )

        gps_ifd = {
            GPSIFD.GPSVersionID: (2, 3, 0, 0),
            GPSIFD.GPSLatitudeRef: lat_deg[0].encode('utf-8'),
            GPSIFD.GPSLatitude: lat_deg[1],
            GPSIFD.GPSLongitudeRef: lon_deg[0].encode('utf-8'),
            GPSIFD.GPSLongitude: lon_deg[1],
            GPSIFD.GPSAltitudeRef: 0,
            GPSIFD.GPSAltitude: (random.randint(10, 500), 1),
            GPSIFD.GPSTimeStamp: gps_time,
            GPSIFD.GPSSpeedRef: b"K",
            GPSIFD.GPSSpeed: (0, 1),
            GPSIFD.GPSImgDirectionRef: b"T",
            GPSIFD.GPSImgDirection: (random.randint(0, 359), 1),
            GPSIFD.GPSDestBearingRef: b"T",
            GPSIFD.GPSDestBearing: (random.randint(0, 359), 1),
            GPSIFD.GPSDateStamp: timestamp.strftime("%Y:%m:%d").encode('utf-8'),
            GPSIFD.GPSHPositioningError: (random.randint(5, 15), 1),
        }

        return gps_ifd

    @staticmethod
    def _to_deg(value: float, loc: list) -> Tuple[str, Tuple]:
        """
        Convert decimal degrees to degrees, minutes, seconds
        :param value: Decimal degrees
        :param loc: Location references (e.g., ["S", "N"] for latitude)
        :return: Tuple of (reference, (degrees, minutes, seconds))
        """
        if value < 0:
            ref = loc[0]
        else:
            ref = loc[1]

        value = abs(value)
        deg = int(value)
        min_val = int((value - deg) * 60)
        sec = int(((value - deg) * 60 - min_val) * 60 * 100)

        return ref, ((deg, 1), (min_val, 1), (sec, 100))

    def resize_for_instagram(
        self,
        image_path: str,
        output_path: Optional[str] = None,
        max_size: int = 1080
    ) -> str:
        """
        Resize image to Instagram's preferred dimensions
        :param image_path: Input image path
        :param output_path: Output path (if None, overwrites input)
        :param max_size: Maximum dimension size
        :return: Output path
        """
        if output_path is None:
            output_path = image_path

        img = Image.open(image_path)

        # Calculate new size maintaining aspect ratio
        width, height = img.size

        if width > height:
            # Landscape
            new_width = max_size
            new_height = int((max_size / width) * height)
        else:
            # Portrait or square
            new_height = max_size
            new_width = int((max_size / height) * width)

        # Resize with high-quality antialiasing
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Save
        img.save(output_path, quality=95, optimize=True)

        return output_path

    def prepare_for_upload(
        self,
        image_path: str,
        device_model: Optional[str] = None,
        gps_coords: Optional[Tuple[float, float]] = None
    ) -> bytes:
        """
        Prepare image for upload with all metadata
        :param image_path: Path to image
        :param device_model: Device model override
        :param gps_coords: GPS coordinates
        :return: Image bytes ready for upload
        """
        # Use temporary file for processing
        temp_path = f"/tmp/ig_upload_{int(time.time())}.jpg"

        try:
            # Resize
            self.resize_for_instagram(image_path, temp_path)

            # Add EXIF
            if device_model:
                original_model = self.device_model
                self.device_model = device_model
                self.camera_settings = self.CAMERA_SETTINGS.get(
                    device_model,
                    self.CAMERA_SETTINGS["iPhone 15 Pro"]
                )

            self.add_iphone_exif(temp_path, temp_path, gps_coords)

            if device_model:
                self.device_model = original_model

            # Read bytes
            with open(temp_path, 'rb') as f:
                image_bytes = f.read()

            return image_bytes

        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)
