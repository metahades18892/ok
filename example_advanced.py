#!/usr/bin/env python3
"""
Ejemplo Completo: Instagram API con Anti-Ban Total
Para uso con proxies móviles
"""

import os
import sys
import time
import logging
from datetime import datetime
from dotenv import load_dotenv

from client_advanced import AdvancedInstagramClient
from device import DeviceGenerator
from anti_ban import (
    AccountWarming,
    AdvancedTimingPatterns,
    ProxyRotationManager,
    BehaviorRandomization,
    RiskScoreCalculator
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('instagram_bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Load environment
load_dotenv()


def setup_mobile_proxies():
    """
    Configurar proxies móviles
    IMPORTANTE: Usa SOLO proxies móviles (4G/5G)
    """
    proxies = [
        {
            "url": os.getenv("MOBILE_PROXY_1", "http://user:pass@proxy1:port"),
            "type": "mobile",
            "country": "US",
            "city": "New York",
            "carrier": "T-Mobile",
            "timezone": "America/New_York",
            "coordinates": (40.7128, -74.0060)  # NYC
        },
        {
            "url": os.getenv("MOBILE_PROXY_2", "http://user:pass@proxy2:port"),
            "type": "mobile",
            "country": "US",
            "city": "Los Angeles",
            "carrier": "Verizon",
            "timezone": "America/Los_Angeles",
            "coordinates": (34.0522, -118.2437)  # LA
        },
        {
            "url": os.getenv("MOBILE_PROXY_3", "http://user:pass@proxy3:port"),
            "type": "mobile",
            "country": "US",
            "city": "Miami",
            "carrier": "AT&T",
            "timezone": "America/New_York",
            "coordinates": (25.7617, -80.1918)  # Miami
        }
    ]

    return proxies


def example_single_post_with_full_protection():
    """
    Ejemplo 1: Hacer UN post con TODAS las protecciones
    """
    logger.info("="*60)
    logger.info("EJEMPLO 1: Single Post con Protección Total")
    logger.info("="*60)

    # Setup proxies
    proxies = setup_mobile_proxies()

    # Crear cliente avanzado
    client = AdvancedInstagramClient(
        username=os.getenv("INSTAGRAM_USERNAME"),
        password=os.getenv("INSTAGRAM_PASSWORD"),
        proxies=proxies,
        enable_warming=True,
        enable_advanced_timing=True,
        enable_behavior_randomization=True
    )

    # Health check ANTES
    logger.info("\n--- Pre-Post Health Check ---")
    health = client.health_check()
    logger.info(f"Risk Score: {health['risk_score']:.2f}")
    logger.info(f"Recommendation: {health['recommendation']}")
    logger.info(f"Warmup Stage: {health['warmup_stage']}")
    logger.info(f"Proxy: {health['proxy']}")

    # Verificar si es seguro proceder
    if health['risk_score'] > 0.7:
        logger.error("❌ Risk score too high! Aborting.")
        return

    # Login seguro
    logger.info("\n--- Attempting Safe Login ---")
    if not client.safe_login():
        logger.error("❌ Login failed!")
        return

    logger.info("✅ Login successful!")

    # Browsing antes de postear (comportamiento natural)
    logger.info("\n--- Natural Browsing Before Post ---")
    browse_duration = random.randint(120, 300)
    logger.info(f"Browsing feed for {browse_duration}s...")
    # Aquí harías browsing real
    time.sleep(browse_duration)

    # Preparar post
    image_path = "photo.jpg"
    caption = "Beautiful day 🌞"

    # Upload con protección
    logger.info("\n--- Uploading Photo ---")
    result = client.safe_upload_photo(
        image_path=image_path,
        caption=caption,
        auto_optimize=True  # Randomiza caption, añade EXIF, etc.
    )

    # Resultado
    if result.get("status") == "ok":
        logger.info("✅ Photo uploaded successfully!")
        media = result.get("media", {})
        logger.info(f"Media ID: {media.get('id')}")
    else:
        logger.error(f"❌ Upload failed: {result.get('message')}")

    # Health check DESPUÉS
    logger.info("\n--- Post-Post Health Check ---")
    health = client.health_check()
    logger.info(f"Risk Score: {health['risk_score']:.2f}")
    logger.info(f"Recommendation: {health['recommendation']}")

    # Logout
    client.logout()


def example_multi_account_campaign():
    """
    Ejemplo 2: Campaña con múltiples cuentas
    Distribuye posts entre varias cuentas para reducir riesgo
    """
    logger.info("="*60)
    logger.info("EJEMPLO 2: Multi-Account Campaign")
    logger.info("="*60)

    # Configuración de cuentas
    accounts = [
        {
            "username": os.getenv("INSTAGRAM_USER_1"),
            "password": os.getenv("INSTAGRAM_PASS_1"),
            "posts_today": 0,
            "max_posts": 5
        },
        {
            "username": os.getenv("INSTAGRAM_USER_2"),
            "password": os.getenv("INSTAGRAM_PASS_2"),
            "posts_today": 0,
            "max_posts": 5
        },
        {
            "username": os.getenv("INSTAGRAM_USER_3"),
            "password": os.getenv("INSTAGRAM_PASS_3"),
            "posts_today": 0,
            "max_posts": 5
        }
    ]

    proxies = setup_mobile_proxies()

    # Lista de posts a hacer
    posts = [
        {"image": "photo1.jpg", "caption": "Amazing view! 🏔️"},
        {"image": "photo2.jpg", "caption": "Loving this place ❤️"},
        {"image": "photo3.jpg", "caption": "Perfect weather today ☀️"},
        {"image": "photo4.jpg", "caption": "Great vibes! ✨"},
        {"image": "photo5.jpg", "caption": "Beautiful moment 📸"},
    ]

    # Distribuir posts entre cuentas
    for post in posts:
        # Seleccionar cuenta con menos posts
        account = min(accounts, key=lambda a: a["posts_today"])

        if account["posts_today"] >= account["max_posts"]:
            logger.warning(f"⚠️ All accounts reached daily limit")
            break

        logger.info(f"\n--- Posting with {account['username']} ---")

        # Crear cliente para esta cuenta
        client = AdvancedInstagramClient(
            username=account["username"],
            password=account["password"],
            proxies=proxies,
            enable_warming=True,
            enable_advanced_timing=True,
            enable_behavior_randomization=True
        )

        # Login
        if not client.safe_login():
            logger.error(f"❌ Login failed for {account['username']}")
            continue

        # Upload
        result = client.safe_upload_photo(
            image_path=post["image"],
            caption=post["caption"],
            auto_optimize=True
        )

        if result.get("status") == "ok":
            logger.info(f"✅ Posted with {account['username']}")
            account["posts_today"] += 1
        else:
            logger.error(f"❌ Failed to post with {account['username']}")

        # Logout
        client.logout()

        # Delay entre cuentas
        delay = random.uniform(300, 900)  # 5-15 min
        logger.info(f"Waiting {delay/60:.1f} min before next account...")
        time.sleep(delay)

    # Resumen
    logger.info("\n=== Campaign Summary ===")
    for account in accounts:
        logger.info(f"{account['username']}: {account['posts_today']} posts")


def example_daily_activity_pattern():
    """
    Ejemplo 3: Ejecutar patrón de actividad natural para todo el día
    """
    logger.info("="*60)
    logger.info("EJEMPLO 3: Daily Activity Pattern")
    logger.info("="*60)

    proxies = setup_mobile_proxies()

    client = AdvancedInstagramClient(
        username=os.getenv("INSTAGRAM_USERNAME"),
        password=os.getenv("INSTAGRAM_PASSWORD"),
        proxies=proxies,
        enable_warming=True,
        enable_advanced_timing=True,
        enable_behavior_randomization=True
    )

    # Generar patrón de actividad
    pattern = client.behavior_random.generate_natural_activity_pattern()

    logger.info("\n--- Generated Daily Pattern ---")
    for activity in pattern:
        logger.info(f"{activity['time']}: {activity['action']} ({activity['duration']}min)")

    # Ejecutar patrón
    logger.info("\n--- Executing Pattern ---")
    client.execute_daily_activity_pattern()


def example_warming_new_account():
    """
    Ejemplo 4: Warming de cuenta nueva (primeros 14 días)
    """
    logger.info("="*60)
    logger.info("EJEMPLO 4: Account Warming (New Account)")
    logger.info("="*60)

    account_id = "new_account_123"
    warming = AccountWarming(account_id)

    # Ver schedule de warming
    schedule = warming.get_warmup_schedule()

    logger.info(f"\nCurrent Warmup Stage: {schedule['stage']}")
    logger.info(f"Allowed Actions: {schedule['allowed_actions']}")
    logger.info(f"Max Posts/Day: {schedule.get('max_posts_per_day', 'N/A')}")
    logger.info(f"Max Likes/Day: {schedule.get('max_likes_per_day', 'N/A')}")
    logger.info(f"Max Follows/Day: {schedule.get('max_follows_per_day', 'N/A')}")

    # Simular actividades según stage
    if schedule['stage'] == 1:
        # Días 1-3: Solo browsing
        logger.info("\n--- Stage 1: Browse Only ---")
        logger.info("Activities: Browse, search, view profiles")
        logger.info("NO posting, very limited likes")

    elif schedule['stage'] == 2:
        # Días 4-7: Engagement ligero
        logger.info("\n--- Stage 2: Light Engagement ---")
        logger.info("Activities: Browse, likes (20/day), follows (10/day)")
        logger.info("Still NO posting")

    elif schedule['stage'] == 3:
        # Días 8-14: Primeros posts
        logger.info("\n--- Stage 3: First Posts ---")
        logger.info("Activities: Browse, likes (50/day), posts (2/day)")

    elif schedule['stage'] == 4:
        # Día 15+: Normal
        logger.info("\n--- Stage 4: Normal Activity ---")
        logger.info("Activities: All actions with normal limits")


def example_risk_monitoring():
    """
    Ejemplo 5: Monitoreo continuo de risk score
    """
    logger.info("="*60)
    logger.info("EJEMPLO 5: Risk Score Monitoring")
    logger.info("="*60)

    # Simular datos de cuenta
    account_scenarios = [
        {
            "name": "Safe Account",
            "data": {
                "created_at": "2023-01-01",
                "total_posts": 50,
                "total_likes": 500,
                "follows": 100,
                "followers": 120,
                "last_action": datetime.now().isoformat(),
                "recent_action_count": 5,
                "failed_actions": 0
            }
        },
        {
            "name": "Risky Account",
            "data": {
                "created_at": datetime.now().isoformat(),  # Cuenta nueva
                "total_posts": 20,  # Muchos posts para cuenta nueva
                "total_likes": 50,
                "follows": 200,  # Muchos follows
                "followers": 5,  # Pocos followers
                "last_action": datetime.now().isoformat(),
                "recent_action_count": 25,  # Mucha actividad reciente
                "failed_actions": 3  # Errores
            }
        }
    ]

    for scenario in account_scenarios:
        logger.info(f"\n--- {scenario['name']} ---")

        risk = RiskScoreCalculator.calculate_risk(scenario['data'])
        recommendation = RiskScoreCalculator.get_recommendation(risk)

        logger.info(f"Risk Score: {risk:.2f}/1.0")
        logger.info(f"Recommendation: {recommendation}")

        if risk < 0.3:
            logger.info("✅ SAFE - Continue normal activity")
        elif risk < 0.5:
            logger.info("⚠️ CAUTION - Reduce activity")
        elif risk < 0.7:
            logger.info("🔶 WARNING - Take break")
        else:
            logger.info("🚨 CRITICAL - Stop all activity!")


if __name__ == "__main__":
    import random

    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   Instagram API - Anti-Ban Advanced Examples                 ║
║   Con Proxies Móviles y Protección Total                     ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """)

    print("\nEjemplos disponibles:")
    print("1. Single post con protección total")
    print("2. Multi-account campaign")
    print("3. Daily activity pattern")
    print("4. Account warming (cuenta nueva)")
    print("5. Risk score monitoring")
    print("0. Salir")

    while True:
        try:
            choice = input("\nSelecciona ejemplo (0-5): ")

            if choice == "0":
                break
            elif choice == "1":
                example_single_post_with_full_protection()
            elif choice == "2":
                example_multi_account_campaign()
            elif choice == "3":
                example_daily_activity_pattern()
            elif choice == "4":
                example_warming_new_account()
            elif choice == "5":
                example_risk_monitoring()
            else:
                print("Opción inválida")

        except KeyboardInterrupt:
            print("\n\nInterrumpido por usuario")
            break
        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)

    print("\n¡Hasta luego!")
