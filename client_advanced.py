"""
Instagram Client - Anti-Ban Advanced Version
Integra todos los sistemas de camuflaje para uso con proxies móviles
"""

import os
import time
import random
import logging
from typing import Optional, Dict, List
from datetime import datetime

from client import InstagramClient
from device import DeviceGenerator
from anti_ban import (
    AccountWarming,
    AdvancedTimingPatterns,
    ProxyRotationManager,
    BehaviorRandomization,
    RiskScoreCalculator
)


class AdvancedInstagramClient(InstagramClient):
    """
    Cliente avanzado con anti-ban completo
    """

    def __init__(
        self,
        username: str,
        password: str,
        device: Optional[DeviceGenerator] = None,
        proxies: Optional[List[Dict]] = None,
        enable_warming: bool = True,
        enable_advanced_timing: bool = True,
        enable_behavior_randomization: bool = True
    ):
        """
        Initialize advanced client

        :param username: Instagram username
        :param password: Instagram password
        :param device: Device fingerprint (optional)
        :param proxies: List of proxy configs
        :param enable_warming: Enable account warming system
        :param enable_advanced_timing: Enable advanced timing patterns
        :param enable_behavior_randomization: Enable behavior randomization
        """

        # Generate unique account ID
        self.account_id = f"{username}_{hash(username) % 10000}"

        # Initialize proxy manager
        self.proxy_manager = None
        if proxies:
            self.proxy_manager = ProxyRotationManager(proxies)
            current_proxy = self.proxy_manager.get_proxy_for_account(self.account_id)
            proxy_url = current_proxy["url"]
        else:
            proxy_url = None

        # Initialize base client
        super().__init__(
            username=username,
            password=password,
            device=device,
            proxy=proxy_url,
            use_timing=enable_advanced_timing
        )

        # Anti-ban systems
        self.warming = AccountWarming(self.account_id) if enable_warming else None
        self.advanced_timing = AdvancedTimingPatterns() if enable_advanced_timing else None
        self.behavior_random = BehaviorRandomization() if enable_behavior_randomization else None

        # State tracking
        self.session_active = False
        self.last_action_time = None
        self.consecutive_errors = 0

        # Logging
        self.logger = logging.getLogger(f"AdvancedClient.{username}")

    def safe_login(self) -> bool:
        """
        Login con verificaciones de seguridad
        """
        # Verificar warmup si está habilitado
        if self.warming:
            can_login, reason, wait = self.warming.can_perform_action("login")
            if not can_login:
                self.logger.warning(f"Login blocked by warming: {reason}")
                if wait > 0:
                    self.logger.info(f"Wait {wait}s before retrying")
                return False

        # Rotar proxy si es necesario
        if self.proxy_manager and self.proxy_manager.should_rotate_proxy(self.account_id):
            self.logger.info("Rotating proxy...")
            new_proxy = self.proxy_manager.get_proxy_for_account(
                self.account_id,
                force_rotate=True
            )
            self.session.proxies = {
                "http": new_proxy["url"],
                "https": new_proxy["url"]
            }
            self.logger.info(f"New proxy: {new_proxy.get('country')}, {new_proxy.get('carrier')}")

        # Delay antes de login (simula tiempo de escribir credenciales)
        if self.advanced_timing:
            typing_delay = random.uniform(3, 8)
            self.logger.info(f"Simulating credential typing ({typing_delay:.1f}s)...")
            time.sleep(typing_delay)

        # Intentar login
        success = self.login()

        # Registrar acción
        if self.warming:
            self.warming.record_action("login", success)

        if not success:
            self.consecutive_errors += 1

            # Verificar si proxy está baneado
            if self.consecutive_errors >= 3 and self.proxy_manager:
                self.logger.error("Too many errors, marking proxy as banned")
                current_proxy = self.proxy_manager.get_proxy_for_account(self.account_id)
                self.proxy_manager.mark_proxy_as_banned(current_proxy["url"])

            return False

        self.consecutive_errors = 0
        self.session_active = True
        return True

    def safe_upload_photo(
        self,
        image_path: str,
        caption: str = "",
        location: Optional[Dict] = None,
        auto_optimize: bool = True
    ) -> Dict:
        """
        Upload foto con todas las medidas anti-ban
        """
        # Verificar warmup
        if self.warming:
            can_post, reason, wait = self.warming.can_perform_action("post")
            if not can_post:
                self.logger.warning(f"Post blocked by warming: {reason}")
                return {"status": "error", "message": reason}

        # Verificar si necesita break
        if self.advanced_timing:
            should_break, break_duration = self.advanced_timing.should_take_break()
            if should_break:
                self.logger.info(f"Taking natural break ({break_duration/60:.1f} min)...")
                time.sleep(break_duration)
                self.advanced_timing.reset_session()

        # Calcular risk score
        account_data = self._get_account_data()
        risk_score = RiskScoreCalculator.calculate_risk(account_data)
        recommendation = RiskScoreCalculator.get_recommendation(risk_score)

        self.logger.info(f"Risk Score: {risk_score:.2f} - {recommendation}")

        if risk_score > 0.7:
            self.logger.error("Risk score too high! Aborting post.")
            return {"status": "error", "message": "Risk score too high"}

        # Randomizar caption
        if auto_optimize and self.behavior_random:
            caption = self.behavior_random.randomize_caption(caption)
            self.logger.info(f"Randomized caption: {caption}")

        # Simular tiempo de edición de foto
        if self.behavior_random:
            edit_time = self.behavior_random.randomize_upload_time()
            self.logger.info(f"Simulating photo editing ({edit_time}s)...")
            time.sleep(edit_time)

        # Delay basado en patrón de timing avanzado
        if self.advanced_timing:
            delay = self.advanced_timing.get_session_based_delay("post")
            self.logger.info(f"Waiting {delay:.1f}s before post...")
            time.sleep(delay)

        # Upload
        self.logger.info(f"Uploading photo: {image_path}")
        result = self.upload_photo(image_path, caption, location)

        # Registrar acción
        success = result.get("status") == "ok"
        if self.warming:
            self.warming.record_action("post", success)

        if not success:
            self.consecutive_errors += 1
        else:
            self.consecutive_errors = 0
            self.last_action_time = datetime.now()

        return result

    def safe_like(self, media_id: str) -> Dict:
        """Like con verificaciones"""
        if self.warming:
            can_like, reason, wait = self.warming.can_perform_action("like")
            if not can_like:
                return {"status": "error", "message": reason}

        if self.advanced_timing:
            delay = self.advanced_timing.get_session_based_delay("like")
            time.sleep(delay)

        # Aquí iría la implementación de like
        # (necesitarías añadirla a la clase base)

        if self.warming:
            self.warming.record_action("like", True)

        return {"status": "ok"}

    def _get_account_data(self) -> Dict:
        """Obtener datos de cuenta para cálculo de risk"""
        # Aquí obtendrías datos reales de la DB
        # Por ahora retornamos mock data
        return {
            "created_at": "2024-01-01",
            "total_posts": 10,
            "total_likes": 100,
            "follows": 50,
            "followers": 40,
            "last_action": datetime.now().isoformat(),
            "recent_action_count": 5,
            "failed_actions": self.consecutive_errors
        }

    def execute_daily_activity_pattern(self):
        """
        Ejecuta patrón de actividad natural para el día
        """
        if not self.behavior_random:
            self.logger.warning("Behavior randomization not enabled")
            return

        pattern = self.behavior_random.generate_natural_activity_pattern()

        self.logger.info(f"Generated activity pattern for today:")
        for activity in pattern:
            self.logger.info(f"  {activity['time']}: {activity['action']} ({activity['duration']}min)")

        for activity in pattern:
            # Calcular tiempo hasta la actividad
            target_time = datetime.strptime(activity['time'], "%H:%M").time()
            now = datetime.now()
            target_datetime = now.replace(
                hour=target_time.hour,
                minute=target_time.minute,
                second=0
            )

            # Si ya pasó la hora, saltar
            if target_datetime < now:
                self.logger.info(f"Skipping past activity: {activity['action']} at {activity['time']}")
                continue

            # Esperar hasta la hora programada
            wait_seconds = (target_datetime - now).seconds
            self.logger.info(f"Waiting {wait_seconds/60:.1f}min until next activity...")
            time.sleep(wait_seconds)

            # Ejecutar actividad
            self.logger.info(f"Executing: {activity['action']}")

            if activity['action'] == "post":
                # Aquí ejecutarías el post real
                self.logger.info("Would post here")
            elif activity['action'] == "like":
                # Aquí ejecutarías likes
                self.logger.info("Would like here")
            elif activity['action'] == "browse":
                # Simular browsing
                time.sleep(activity['duration'] * 60)

    def health_check(self) -> Dict:
        """
        Verificar salud de la cuenta
        """
        account_data = self._get_account_data()
        risk_score = RiskScoreCalculator.calculate_risk(account_data)
        recommendation = RiskScoreCalculator.get_recommendation(risk_score)

        warmup_schedule = None
        if self.warming:
            warmup_schedule = self.warming.get_warmup_schedule()

        proxy_info = None
        if self.proxy_manager:
            current_proxy = self.proxy_manager.get_proxy_for_account(self.account_id)
            proxy_info = {
                "country": current_proxy.get("country"),
                "carrier": current_proxy.get("carrier"),
                "type": current_proxy.get("type")
            }

        return {
            "account_id": self.account_id,
            "username": self.username,
            "risk_score": risk_score,
            "recommendation": recommendation,
            "warmup_stage": warmup_schedule["stage"] if warmup_schedule else "N/A",
            "proxy": proxy_info,
            "consecutive_errors": self.consecutive_errors,
            "session_active": self.session_active
        }


# ========================================
# EJEMPLO DE USO
# ========================================

if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Configurar proxies móviles
    proxies = [
        {
            "url": "http://user:pass@mobile-proxy-1.com:8080",
            "type": "mobile",
            "country": "US",
            "city": "New York",
            "carrier": "T-Mobile",
            "timezone": "America/New_York"
        },
        {
            "url": "http://user:pass@mobile-proxy-2.com:8080",
            "type": "mobile",
            "country": "US",
            "city": "Los Angeles",
            "carrier": "Verizon",
            "timezone": "America/Los_Angeles"
        }
    ]

    # Crear cliente avanzado
    client = AdvancedInstagramClient(
        username="your_username",
        password="your_password",
        proxies=proxies,
        enable_warming=True,
        enable_advanced_timing=True,
        enable_behavior_randomization=True
    )

    # Health check
    health = client.health_check()
    print("\n=== Account Health ===")
    print(f"Risk Score: {health['risk_score']:.2f}")
    print(f"Recommendation: {health['recommendation']}")
    print(f"Warmup Stage: {health['warmup_stage']}")
    print(f"Proxy: {health['proxy']}")

    # Login seguro
    if client.safe_login():
        print("\n✓ Logged in successfully")

        # Upload con todas las protecciones
        result = client.safe_upload_photo(
            image_path="photo.jpg",
            caption="My awesome photo",
            auto_optimize=True
        )

        print(f"\nUpload result: {result}")

        # Ejecutar patrón de actividad natural
        # client.execute_daily_activity_pattern()
    else:
        print("\n✗ Login failed")
