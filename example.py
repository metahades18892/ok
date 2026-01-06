#!/usr/bin/env python3
"""
Instagram iOS API - Usage Examples
Demonstrates various features of the stealth API
"""

import os
import logging
from dotenv import load_dotenv
from client import InstagramClient
from device import DeviceGenerator

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def example_basic_post():
    """
    Example 1: Basic photo upload
    """
    print("\n" + "="*50)
    print("EXAMPLE 1: Basic Photo Upload")
    print("="*50 + "\n")

    # Create client
    client = InstagramClient(
        username=os.getenv("INSTAGRAM_USERNAME"),
        password=os.getenv("INSTAGRAM_PASSWORD"),
        use_timing=True  # Enable human timing simulation
    )

    # Login
    if client.login():
        # Upload photo
        response = client.upload_photo(
            image_path="path/to/your/photo.jpg",
            caption="Posted with stealth API! 📸"
        )

        print(f"Upload response: {response}")

        # Save session for reuse
        client.save_session("session.json")

        # Logout
        client.logout()
    else:
        print("Login failed!")


def example_post_with_location():
    """
    Example 2: Post with location and GPS data
    """
    print("\n" + "="*50)
    print("EXAMPLE 2: Post with Location")
    print("="*50 + "\n")

    client = InstagramClient(
        username=os.getenv("INSTAGRAM_USERNAME"),
        password=os.getenv("INSTAGRAM_PASSWORD")
    )

    if client.login():
        # Location data
        location = {
            "name": "Times Square",
            "lat": 40.758896,
            "lng": -73.985130,
            "external_id": "212988663",  # Instagram location ID
            "external_id_source": "facebook_places"
        }

        # GPS coordinates for EXIF (should match location)
        gps_coords = (40.758896, -73.985130)

        response = client.upload_photo(
            image_path="path/to/photo.jpg",
            caption="📍 Times Square, NYC",
            location=location,
            gps_coords=gps_coords
        )

        print(f"Upload response: {response}")
        client.logout()


def example_custom_device():
    """
    Example 3: Use custom device fingerprint
    """
    print("\n" + "="*50)
    print("EXAMPLE 3: Custom Device Fingerprint")
    print("="*50 + "\n")

    # Create specific device
    device = DeviceGenerator(seed="my-unique-seed")

    # Print device info
    print("Device Information:")
    print(f"  Model: {device.device_name}")
    print(f"  iOS: {device.ios_version}")
    print(f"  Device ID: {device.device_id}")
    print(f"  UUID: {device.uuid}")

    # Save device for reuse
    device.save_to_file("my_device.json")
    print("\nDevice saved to my_device.json")

    # Create client with custom device
    client = InstagramClient(
        username=os.getenv("INSTAGRAM_USERNAME"),
        password=os.getenv("INSTAGRAM_PASSWORD"),
        device=device
    )

    if client.login():
        print("\nLogged in successfully with custom device!")
        client.logout()


def example_load_device():
    """
    Example 4: Load saved device
    """
    print("\n" + "="*50)
    print("EXAMPLE 4: Load Saved Device")
    print("="*50 + "\n")

    # Load device from file
    device = DeviceGenerator.load_from_file("my_device.json")
    print(f"Loaded device: {device.device_name}")

    client = InstagramClient(
        username=os.getenv("INSTAGRAM_USERNAME"),
        password=os.getenv("INSTAGRAM_PASSWORD"),
        device=device
    )

    if client.login():
        print("Logged in with saved device!")
        client.logout()


def example_load_session():
    """
    Example 5: Reuse saved session (faster)
    """
    print("\n" + "="*50)
    print("EXAMPLE 5: Reuse Saved Session")
    print("="*50 + "\n")

    # Load saved session (no login needed if valid)
    client = InstagramClient.load_session(
        filename="session.json",
        password=os.getenv("INSTAGRAM_PASSWORD")
    )

    print(f"Loaded session for user: {client.username}")
    print(f"User ID: {client.user_id}")

    # Get user info
    user_info = client.get_user_info()
    print(f"User info: {user_info}")

    # Upload photo
    response = client.upload_photo(
        image_path="path/to/photo.jpg",
        caption="Using saved session! ⚡"
    )

    print(f"Upload response: {response}")


def example_with_proxy():
    """
    Example 6: Use with proxy
    """
    print("\n" + "="*50)
    print("EXAMPLE 6: Use with Proxy")
    print("="*50 + "\n")

    # Create client with proxy
    client = InstagramClient(
        username=os.getenv("INSTAGRAM_USERNAME"),
        password=os.getenv("INSTAGRAM_PASSWORD"),
        proxy="http://user:pass@proxy-server:8080",  # Your proxy
        use_timing=True
    )

    if client.login():
        print("Logged in through proxy!")

        # Get timeline
        timeline = client.get_timeline()
        print(f"Timeline: {timeline.get('status')}")

        client.logout()


def example_rate_limiter():
    """
    Example 7: Check rate limiter stats
    """
    print("\n" + "="*50)
    print("EXAMPLE 7: Rate Limiter Statistics")
    print("="*50 + "\n")

    client = InstagramClient(
        username=os.getenv("INSTAGRAM_USERNAME"),
        password=os.getenv("INSTAGRAM_PASSWORD")
    )

    if client.login():
        # Make some requests
        client.get_timeline()
        client.get_user_info()

        # Check rate limiter stats
        stats = client.rate_limiter.get_stats()
        print("\nRate Limiter Stats:")
        print(f"  Requests in last hour: {stats['requests_last_hour']}")
        print(f"  Requests remaining: {stats['requests_remaining']}")
        print(f"  Posts in last 24h: {stats['posts_last_24h']}")
        print(f"  Posts remaining: {stats['posts_remaining']}")

        client.logout()


def example_scheduled_posts():
    """
    Example 8: Schedule posts for realistic times
    """
    print("\n" + "="*50)
    print("EXAMPLE 8: Scheduled Posts")
    print("="*50 + "\n")

    client = InstagramClient(
        username=os.getenv("INSTAGRAM_USERNAME"),
        password=os.getenv("INSTAGRAM_PASSWORD")
    )

    # Generate schedule for 3 posts over 6 hours
    schedule = client.scheduler.schedule_posts(
        num_posts=3,
        spread_hours=6.0
    )

    print("Planned post schedule:")
    for i, post_time in enumerate(schedule, 1):
        print(f"  Post {i}: {post_time.strftime('%Y-%m-%d %H:%M:%S')}")

    print("\nSchedule will avoid unrealistic posting times (late night, etc.)")


def example_delete_post():
    """
    Example 9: Delete a post
    """
    print("\n" + "="*50)
    print("EXAMPLE 9: Delete Post")
    print("="*50 + "\n")

    client = InstagramClient(
        username=os.getenv("INSTAGRAM_USERNAME"),
        password=os.getenv("INSTAGRAM_PASSWORD")
    )

    if client.login():
        # Delete a post by media ID
        media_id = "1234567890123456789"  # Replace with actual media ID
        response = client.delete_media(media_id)

        print(f"Delete response: {response}")
        client.logout()


if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║        Instagram iOS API - Stealth Implementation         ║
    ║                                                            ║
    ║  Military-grade stealth features:                          ║
    ║  ✓ Device fingerprinting (iPhone 15 Pro/Max)              ║
    ║  ✓ Request signature generation                           ║
    ║  ✓ EXIF metadata injection                                ║
    ║  ✓ Human timing simulation                                ║
    ║  ✓ Rate limiting                                          ║
    ║  ✓ TLS fingerprinting                                     ║
    ║  ✓ Session management                                     ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
    """)

    print("\nAvailable examples:")
    print("1. Basic photo upload")
    print("2. Post with location and GPS")
    print("3. Custom device fingerprint")
    print("4. Load saved device")
    print("5. Reuse saved session")
    print("6. Use with proxy")
    print("7. Rate limiter statistics")
    print("8. Scheduled posts")
    print("9. Delete post")

    print("\n" + "="*60)
    print("IMPORTANT: Update .env file with your credentials!")
    print("="*60)

    # Uncomment the example you want to run:
    # example_basic_post()
    # example_post_with_location()
    # example_custom_device()
    # example_load_device()
    # example_load_session()
    # example_with_proxy()
    # example_rate_limiter()
    # example_scheduled_posts()
    # example_delete_post()
