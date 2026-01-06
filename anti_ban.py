"""
Anti-Ban System - Military Grade
Sistema avanzado para evitar detección y ban de cuentas
Diseñado para uso con proxies móviles (4G/5G)
"""

import random
import time
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import sqlite3


class AccountWarming:
    """
    Sistema de warming para cuentas nuevas
    Las cuentas nuevas necesitan "envejecerse" antes de postear agresivamente
    """

    def __init__(self, account_id: str, db_path: str = "accounts.db"):
        self.account_id = account_id
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Inicializar base de datos de cuentas"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        c.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id TEXT PRIMARY KEY,
                created_at TIMESTAMP,
                last_action TIMESTAMP,
                total_posts INTEGER DEFAULT 0,
                total_likes INTEGER DEFAULT 0,
                total_comments INTEGER DEFAULT 0,
                total_follows INTEGER DEFAULT 0,
                warmup_stage INTEGER DEFAULT 0,
                is_warmed BOOLEAN DEFAULT 0,
                risk_score REAL DEFAULT 0.0
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id TEXT,
                action_type TEXT,
                timestamp TIMESTAMP,
                success BOOLEAN,
                FOREIGN KEY (account_id) REFERENCES accounts (id)
            )
        ''')

        conn.commit()
        conn.close()

    def get_warmup_schedule(self) -> Dict:
        """
        Schedule progresivo de warming
        Día 1-3: Solo lectura
        Día 4-7: Likes y follows limitados
        Día 8-14: Primeros posts
        Día 15+: Actividad normal
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        c.execute('SELECT created_at, warmup_stage FROM accounts WHERE id = ?',
                  (self.account_id,))
        result = c.fetchone()
        conn.close()

        if not result:
            # Nueva cuenta
            return {
                "stage": 0,
                "allowed_actions": ["browse", "search"],
                "max_posts_per_day": 0,
                "max_likes_per_day": 0,
                "max_follows_per_day": 0,
                "delay_between_actions": (30, 120),  # segundos
            }

        created_at = datetime.fromisoformat(result[0])
        days_old = (datetime.now() - created_at).days
        stage = result[1]

        # Día 1-3: Solo navegar
        if days_old < 3:
            return {
                "stage": 1,
                "allowed_actions": ["browse", "search", "view_profile"],
                "max_posts_per_day": 0,
                "max_likes_per_day": 5,  # Muy limitado
                "max_follows_per_day": 0,
                "delay_between_actions": (60, 180),
            }

        # Día 4-7: Engagement ligero
        elif days_old < 7:
            return {
                "stage": 2,
                "allowed_actions": ["browse", "search", "view_profile", "like", "follow"],
                "max_posts_per_day": 0,
                "max_likes_per_day": 20,
                "max_follows_per_day": 10,
                "delay_between_actions": (45, 150),
            }

        # Día 8-14: Primeros posts
        elif days_old < 14:
            return {
                "stage": 3,
                "allowed_actions": ["browse", "like", "follow", "post", "comment"],
                "max_posts_per_day": 2,
                "max_likes_per_day": 50,
                "max_follows_per_day": 20,
                "max_comments_per_day": 10,
                "delay_between_actions": (30, 120),
            }

        # Día 15+: Actividad normal (pero conservadora)
        else:
            return {
                "stage": 4,
                "allowed_actions": ["all"],
                "max_posts_per_day": 10,
                "max_likes_per_day": 200,
                "max_follows_per_day": 50,
                "max_comments_per_day": 50,
                "delay_between_actions": (20, 90),
            }

    def can_perform_action(self, action_type: str) -> tuple:
        """
        Verifica si se puede realizar una acción
        Returns: (can_perform: bool, reason: str, wait_time: int)
        """
        schedule = self.get_warmup_schedule()

        # Verificar si acción permitida
        if action_type not in schedule["allowed_actions"] and "all" not in schedule["allowed_actions"]:
            return (False, f"Action not allowed in stage {schedule['stage']}", 0)

        # Verificar límites diarios
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        c.execute('''
            SELECT COUNT(*) FROM actions
            WHERE account_id = ? AND action_type = ? AND timestamp >= ?
        ''', (self.account_id, action_type, today))

        count_today = c.fetchone()[0]
        conn.close()

        limit_key = f"max_{action_type}s_per_day"
        if limit_key in schedule:
            if count_today >= schedule[limit_key]:
                return (False, f"Daily limit reached for {action_type}", 3600)

        return (True, "OK", 0)

    def record_action(self, action_type: str, success: bool = True):
        """Registrar acción realizada"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        c.execute('''
            INSERT INTO actions (account_id, action_type, timestamp, success)
            VALUES (?, ?, ?, ?)
        ''', (self.account_id, action_type, datetime.now(), success))

        # Actualizar contador en accounts
        if success:
            count_field = f"total_{action_type}s"
            c.execute(f'''
                UPDATE accounts
                SET {count_field} = {count_field} + 1,
                    last_action = ?
                WHERE id = ?
            ''', (datetime.now(), self.account_id))

        conn.commit()
        conn.close()


class AdvancedTimingPatterns:
    """
    Patrones de timing ultra-realistas
    Más allá de distribución Gamma
    """

    def __init__(self):
        self.session_start = datetime.now()
        self.action_count = 0
        self.fatigue_factor = 0.0

    def get_session_based_delay(self, action_type: str) -> float:
        """
        Delay que aumenta con fatiga de usuario
        Los humanos se cansan después de mucho tiempo en la app
        """
        self.action_count += 1

        # Duración de sesión en minutos
        session_duration = (datetime.now() - self.session_start).seconds / 60

        # Base delay
        base_delays = {
            "like": (1.5, 4.0),
            "comment": (5.0, 15.0),
            "post": (30.0, 120.0),
            "follow": (2.0, 8.0),
            "browse": (0.5, 2.0),
        }

        min_delay, max_delay = base_delays.get(action_type, (2.0, 10.0))

        # Factor de fatiga (aumenta con tiempo y acciones)
        self.fatigue_factor = min(
            1.5,
            1.0 + (session_duration / 60) * 0.3 + (self.action_count / 100) * 0.2
        )

        # Delay ajustado por fatiga
        delay = random.uniform(min_delay, max_delay) * self.fatigue_factor

        # Pausas largas aleatorias (como cuando alguien se distrae)
        if random.random() < 0.05:  # 5% chance
            distraction_time = random.uniform(30, 180)
            delay += distraction_time

        return delay

    def should_take_break(self) -> tuple:
        """
        Determina si se debe tomar un break largo
        Returns: (should_break: bool, break_duration: int)
        """
        session_duration = (datetime.now() - self.session_start).seconds / 60

        # Break después de 20-40 minutos de uso continuo
        if session_duration > random.uniform(20, 40):
            break_duration = random.uniform(10, 30) * 60  # 10-30 minutos
            return (True, int(break_duration))

        # Break aleatorio por "notificación" o "llamada"
        if random.random() < 0.02:  # 2% chance
            break_duration = random.uniform(2, 10) * 60  # 2-10 minutos
            return (True, int(break_duration))

        return (False, 0)

    def reset_session(self):
        """Reset después de break"""
        self.session_start = datetime.now()
        self.action_count = 0
        self.fatigue_factor = 0.0


class ProxyRotationManager:
    """
    Gestión inteligente de rotación de proxies móviles
    """

    def __init__(self, proxies: List[Dict]):
        """
        proxies: Lista de dicts con formato:
        {
            "url": "http://user:pass@proxy:port",
            "type": "mobile|residential|datacenter",
            "country": "US",
            "city": "New York",
            "carrier": "T-Mobile",
            "timezone": "America/New_York"
        }
        """
        self.proxies = proxies
        self.current_proxy = None
        self.proxy_sessions = {}  # Track sessions per proxy
        self.proxy_bans = set()

    def get_proxy_for_account(self, account_id: str, force_rotate: bool = False) -> Dict:
        """
        Obtener proxy para cuenta específica
        Sticky session: misma cuenta = mismo proxy (por un tiempo)
        """
        # Verificar si ya tiene proxy asignado
        if account_id in self.proxy_sessions and not force_rotate:
            session = self.proxy_sessions[account_id]

            # Verificar si la sesión aún es válida (< 30 minutos)
            if (datetime.now() - session["assigned_at"]).seconds < 1800:
                # Verificar que proxy no esté baneado
                if session["proxy"]["url"] not in self.proxy_bans:
                    return session["proxy"]

        # Seleccionar nuevo proxy
        available_proxies = [
            p for p in self.proxies
            if p["url"] not in self.proxy_bans
        ]

        if not available_proxies:
            # Resetear bans si todos están baneados
            self.proxy_bans.clear()
            available_proxies = self.proxies

        # Preferir mobile proxies
        mobile_proxies = [p for p in available_proxies if p["type"] == "mobile"]

        if mobile_proxies:
            proxy = random.choice(mobile_proxies)
        else:
            proxy = random.choice(available_proxies)

        # Asignar sesión
        self.proxy_sessions[account_id] = {
            "proxy": proxy,
            "assigned_at": datetime.now()
        }

        return proxy

    def mark_proxy_as_banned(self, proxy_url: str):
        """Marcar proxy como baneado"""
        self.proxy_bans.add(proxy_url)

    def should_rotate_proxy(self, account_id: str) -> bool:
        """
        Determina si se debe rotar proxy
        Rotar después de X acciones o Y tiempo
        """
        if account_id not in self.proxy_sessions:
            return True

        session = self.proxy_sessions[account_id]
        time_elapsed = (datetime.now() - session["assigned_at"]).seconds

        # Rotar después de 30-60 minutos
        if time_elapsed > random.uniform(1800, 3600):
            return True

        return False


class BehaviorRandomization:
    """
    Randomización de comportamiento para evitar patrones
    """

    @staticmethod
    def randomize_caption(base_caption: str) -> str:
        """
        Añadir variación a captions para evitar detección de duplicados
        """
        variations = [
            lambda c: c,  # Sin cambios
            lambda c: c + " ✨",
            lambda c: c + " 🔥",
            lambda c: c + " 💯",
            lambda c: "✨ " + c,
            lambda c: c + "\n.",  # Punto invisible
            lambda c: c + "\u200B",  # Zero-width space
        ]

        return random.choice(variations)(base_caption)

    @staticmethod
    def randomize_upload_time() -> int:
        """
        Tiempo aleatorio para esperar antes de upload
        Simula tiempo de edición de foto
        """
        return random.randint(5, 30)  # 5-30 segundos

    @staticmethod
    def should_add_filter() -> bool:
        """Decide si añadir filtro a la foto"""
        return random.random() < 0.3  # 30% de fotos con filtro

    @staticmethod
    def generate_natural_activity_pattern() -> List[Dict]:
        """
        Genera patrón de actividad natural para el día
        No todas las acciones son posts
        """
        activities = []

        # Actividad matutina (8-10 AM)
        if random.random() < 0.7:
            activities.append({
                "time": f"{random.randint(8, 10):02d}:{random.randint(0, 59):02d}",
                "action": "browse",
                "duration": random.randint(3, 10)  # minutos
            })

        # Actividad de almuerzo (12-2 PM)
        if random.random() < 0.6:
            activities.append({
                "time": f"{random.randint(12, 14):02d}:{random.randint(0, 59):02d}",
                "action": random.choice(["browse", "like", "comment"]),
                "duration": random.randint(5, 15)
            })

        # Post en horario prime (6-10 PM)
        if random.random() < 0.8:
            activities.append({
                "time": f"{random.randint(18, 22):02d}:{random.randint(0, 59):02d}",
                "action": "post",
                "duration": random.randint(2, 5)
            })

        # Actividad nocturna ligera (10 PM - 12 AM)
        if random.random() < 0.4:
            activities.append({
                "time": f"{random.randint(22, 23):02d}:{random.randint(0, 59):02d}",
                "action": random.choice(["browse", "like"]),
                "duration": random.randint(2, 8)
            })

        return sorted(activities, key=lambda x: x["time"])


class RiskScoreCalculator:
    """
    Calcula score de riesgo de ban para una cuenta
    """

    @staticmethod
    def calculate_risk(account_data: Dict) -> float:
        """
        Calcula risk score 0.0 (seguro) a 1.0 (ban inminente)
        """
        risk = 0.0

        # Factor 1: Edad de cuenta
        account_age_days = (datetime.now() - datetime.fromisoformat(account_data["created_at"])).days

        if account_age_days < 7:
            risk += 0.3  # Cuenta muy nueva
        elif account_age_days < 30:
            risk += 0.15

        # Factor 2: Ratio de posts
        posts_per_day = account_data["total_posts"] / max(account_age_days, 1)

        if posts_per_day > 10:
            risk += 0.25  # Demasiados posts
        elif posts_per_day > 5:
            risk += 0.1

        # Factor 3: Ratio follows/followers
        # (muchos follows sin followers = sospechoso)
        if account_data.get("follows", 0) > 100 and account_data.get("followers", 0) < 10:
            risk += 0.2

        # Factor 4: Actividad reciente
        if account_data.get("last_action"):
            last_action = datetime.fromisoformat(account_data["last_action"])
            hours_since_last = (datetime.now() - last_action).seconds / 3600

            if hours_since_last < 1 and account_data.get("recent_action_count", 0) > 20:
                risk += 0.15  # Demasiada actividad en poco tiempo

        # Factor 5: Tasa de fallos
        if account_data.get("failed_actions", 0) > 5:
            risk += 0.2

        return min(risk, 1.0)

    @staticmethod
    def get_recommendation(risk_score: float) -> str:
        """Recomienda acción basado en risk score"""
        if risk_score < 0.3:
            return "SAFE - Continue normal activity"
        elif risk_score < 0.5:
            return "CAUTION - Reduce activity frequency"
        elif risk_score < 0.7:
            return "WARNING - Take 24h break"
        else:
            return "CRITICAL - Stop all activity, account at risk"
