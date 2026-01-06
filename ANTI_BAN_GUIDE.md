# Guía Definitiva Anti-Ban para Proxies Móviles

## 🎯 Objetivo

Usar Instagram de forma automatizada con proxies móviles **SIN ser baneado**.

---

## 📊 Factores que Causan Bans

### 1. **Cuenta Nueva + Actividad Agresiva** ⚠️⚠️⚠️
- Cuenta creada hoy → 10 posts hoy = BAN INSTANT

### 2. **Patrones Detectables** ⚠️⚠️
- Posts exactamente cada 2 horas
- Siempre a las mismas horas
- Captions idénticos
- Timing robótico

### 3. **Proxy/IP Issues** ⚠️⚠️
- Cambiar IP constantemente durante sesión
- Usar datacenter proxies (en vez de móviles)
- IP baneada previamente

### 4. **Límites Excedidos** ⚠️
- Más de 10 posts/día (cuenta nueva)
- Más de 200 likes/día
- Más de 60 follows/día

### 5. **Comportamiento No-Humano** ⚠️
- No hay browsing, solo posts
- Sin engagement (likes, comments)
- Velocidad de acciones constante

---

## ✅ Sistema Anti-Ban de 10 Capas

### Capa 1: Account Warming (CRÍTICO)

```python
from anti_ban import AccountWarming

warming = AccountWarming("account_id_123")
schedule = warming.get_warmup_schedule()

"""
DÍA 1-3: SOLO MIRAR
- Browse feed
- Ver perfiles
- Buscar hashtags
- 0 posts, 0-5 likes

DÍA 4-7: ENGAGEMENT LIGERO
- Browse
- 10-20 likes/día
- 5-10 follows/día
- 0 posts aún

DÍA 8-14: PRIMEROS POSTS
- 1-2 posts/día
- 30-50 likes/día
- 10-20 follows/día
- Algunos comments

DÍA 15+: ACTIVIDAD NORMAL
- 5-10 posts/día (máximo)
- 100-200 likes/día
- 30-50 follows/día
- Browsing regular
"""

# Verificar antes de cada acción
can_post, reason, wait = warming.can_perform_action("post")
if can_post:
    client.upload_photo(...)
else:
    print(f"Blocked: {reason}. Wait {wait}s")
```

### Capa 2: Advanced Timing

```python
from anti_ban import AdvancedTimingPatterns

timing = AdvancedTimingPatterns()

# Delay que aumenta con fatiga
for i in range(10):
    delay = timing.get_session_based_delay("post")
    print(f"Post {i}: wait {delay:.1f}s")
    time.sleep(delay)

    # Primer post: 45s
    # Post 5: 78s
    # Post 10: 120s + posible break

# Breaks automáticos
should_break, duration = timing.should_take_break()
if should_break:
    print(f"Taking {duration/60:.0f} min break")
    time.sleep(duration)
    timing.reset_session()
```

### Capa 3: Proxy Móvil Correcto

```python
from anti_ban import ProxyRotationManager

# USAR SOLO PROXIES MÓVILES (4G/5G)
mobile_proxies = [
    {
        "url": "http://user:pass@proxy1.com:8080",
        "type": "mobile",  # ← IMPORTANTE
        "country": "US",
        "carrier": "T-Mobile",  # Carrier real
        "timezone": "America/New_York"
    },
    {
        "url": "http://user:pass@proxy2.com:8080",
        "type": "mobile",
        "country": "US",
        "carrier": "Verizon",
        "timezone": "America/Los_Angeles"
    }
]

manager = ProxyRotationManager(mobile_proxies)

# Sticky session: misma cuenta = mismo proxy (30-60 min)
proxy = manager.get_proxy_for_account("account_123")

# Rotar solo cuando sea necesario
if manager.should_rotate_proxy("account_123"):
    new_proxy = manager.get_proxy_for_account("account_123", force_rotate=True)
```

**⚠️ NUNCA uses:**
- Datacenter proxies (detectable al instante)
- Free proxies
- Proxies compartidos con bans
- Proxies que cambian IP cada request

**✅ USA:**
- Proxies móviles 4G/5G residenciales
- Sticky sessions (30-60 min mismo IP)
- Rotation después de X tiempo, NO después de X requests

### Capa 4: Behavior Randomization

```python
from anti_ban import BehaviorRandomization

random_behavior = BehaviorRandomization()

# Randomizar captions (evitar duplicados)
caption1 = random_behavior.randomize_caption("Beautiful sunset")
# → "Beautiful sunset ✨"
caption2 = random_behavior.randomize_caption("Beautiful sunset")
# → "✨ Beautiful sunset"
caption3 = random_behavior.randomize_caption("Beautiful sunset")
# → "Beautiful sunset\u200B" (zero-width space)

# Timing variable
edit_time = random_behavior.randomize_upload_time()
time.sleep(edit_time)  # 5-30 segundos

# Filtros aleatorios
if random_behavior.should_add_filter():
    apply_filter_to_photo()

# Patrón de actividad natural
pattern = random_behavior.generate_natural_activity_pattern()
"""
Resultado:
  08:30 - browse (5 min)
  13:15 - like (8 min)
  19:45 - post (3 min)
  22:30 - browse (6 min)
"""
```

### Capa 5: Risk Score Monitoring

```python
from anti_ban import RiskScoreCalculator

account_data = {
    "created_at": "2024-01-01",
    "total_posts": 25,
    "total_likes": 150,
    "follows": 80,
    "followers": 15,  # ← Problema: muchos follows, pocos followers
    "last_action": datetime.now().isoformat(),
    "recent_action_count": 15,  # ← Problema: 15 acciones en 1 hora
    "failed_actions": 2
}

risk = RiskScoreCalculator.calculate_risk(account_data)
recommendation = RiskScoreCalculator.get_recommendation(risk)

print(f"Risk Score: {risk:.2f}")
print(f"Action: {recommendation}")

"""
Risk Score: 0.65
Action: WARNING - Take 24h break

Si risk > 0.7: STOP TODO
Si risk > 0.5: Reducir actividad
Si risk < 0.3: Safe, continuar
"""
```

### Capa 6: EXIF Metadata Correcto

```python
from media import MediaProcessor

processor = MediaProcessor(device_model="iPhone 15 Pro")

# CRÍTICO: GPS debe match con proxy location
if proxy_location == "New York":
    gps_coords = (40.7128, -74.0060)  # NYC coordinates
elif proxy_location == "Los Angeles":
    gps_coords = (34.0522, -118.2437)  # LA coordinates

# Añadir EXIF con GPS del proxy
processor.add_iphone_exif(
    image_path="photo.jpg",
    gps_coords=gps_coords,  # ← DEBE MATCH PROXY
    capture_time=datetime.now() - timedelta(hours=random.randint(1, 6))
)
```

**⚠️ ERROR COMÚN:**
```python
# Proxy en New York
# GPS en Tokyo
# → Instagram detecta inconsistencia = FLAGGED
```

### Capa 7: Session Management

```python
# NO hagas login/logout constantemente
# Usa sesiones persistentes

client.login()
client.save_session("session.json")  # ← Guardar

# Próxima vez (minutos/horas después):
client = InstagramClient.load_session("session.json", password)
# No hace login de nuevo = menos sospechoso
```

### Capa 8: Natural Activity Mix

```python
# NO: Solo posts, nada más
for i in range(10):
    client.upload_photo(...)  # ← DETECTABLE

# SÍ: Mix de actividades
client.get_timeline()  # Browse
time.sleep(random.uniform(30, 120))

client.like_media(media_id)  # Like
time.sleep(random.uniform(20, 60))

client.upload_photo(...)  # Post
time.sleep(random.uniform(300, 900))

client.get_timeline()  # Browse más
time.sleep(random.uniform(40, 100))

client.comment_media(...)  # Comment
```

### Capa 9: Timezone Consistency

```python
# Si proxy está en timezone America/New_York
# NO postees a las 3 AM hora de New York
# SÍ postea en horario normal (8 AM - 11 PM)

from timing import ActivityScheduler

scheduler = ActivityScheduler()
scheduler.timezone_offset = -5  # EST

if scheduler.is_good_time_to_post():
    client.upload_photo(...)
else:
    next_time = scheduler.get_next_good_time()
    print(f"Wait until {next_time}")
```

### Capa 10: Multiple Accounts Strategy

```python
# NO: 1 account, 100 posts/día
# SÍ: 10 accounts, 10 posts cada uno

accounts = [
    {"username": "user1", "password": "pass1", "proxy": proxy1},
    {"username": "user2", "password": "pass2", "proxy": proxy2},
    # ...
]

# Distribuir carga
for account in accounts:
    client = AdvancedInstagramClient(
        username=account["username"],
        password=account["password"],
        proxies=[account["proxy"]]
    )

    if client.safe_login():
        # Solo 5-10 posts por cuenta
        for i in range(random.randint(5, 10)):
            client.safe_upload_photo(...)
            time.sleep(random.uniform(1800, 3600))  # 30-60 min entre posts
```

---

## 🚫 Errores FATALES que Causan Ban Inmediato

### 1. Cuenta Nueva + Posts Inmediatos
```python
# ❌ FATAL
account_created_today()
upload_10_photos()  # BAN EN 1 HORA

# ✅ CORRECTO
account_created_today()
wait_3_days()
browse_and_like_only()
wait_5_more_days()
first_post()
```

### 2. Timing Robótico
```python
# ❌ FATAL
while True:
    upload_photo()
    time.sleep(3600)  # Exactamente cada hora

# ✅ CORRECTO
while True:
    upload_photo()
    delay = random.uniform(1800, 7200)  # 30min - 2h variable
    time.sleep(delay)
```

### 3. Datacenter Proxies
```python
# ❌ FATAL
proxy = "http://datacenter-proxy.com:8080"  # Detectado al instante

# ✅ CORRECTO
proxy = "http://mobile-4g-proxy.com:8080"  # Indistinguible de usuario real
```

### 4. No Matching GPS/Timezone
```python
# ❌ FATAL
proxy_location = "New York" (UTC-5)
photo_gps = "Tokyo" (UTC+9)
post_time = "3:00 AM New York time"
# → Instagram: "WTF?"

# ✅ CORRECTO
proxy_location = "New York"
photo_gps = NEW_YORK_COORDS
post_time = "7:00 PM New York time"  # Prime time
```

### 5. Sin Browsing/Engagement
```python
# ❌ FATAL
login()
upload_photo_1()
upload_photo_2()
upload_photo_3()
logout()
# → 0 browsing, 0 likes, solo posts = BOT OBVIO

# ✅ CORRECTO
login()
browse_feed(duration=5min)
like_some_posts(5-10)
browse_profiles(3-5)
upload_photo()
like_more_posts(10-15)
comment_on_post()
browse_feed(3min)
logout()
```

---

## 📈 Límites Seguros por Día

### Cuenta Nueva (0-7 días):
- Posts: **0-2/día**
- Likes: **10-30/día**
- Follows: **5-15/día**
- Comments: **0-5/día**

### Cuenta Warmed (7-30 días):
- Posts: **2-5/día**
- Likes: **30-100/día**
- Follows: **15-30/día**
- Comments: **5-20/día**

### Cuenta Aged (30+ días):
- Posts: **5-10/día**
- Likes: **100-300/día**
- Follows: **30-60/día**
- Comments: **20-50/día**

**⚠️ NUNCA excedas estos límites, incluso en cuenta vieja.**

---

## 🔧 Setup Recomendado para Proxies Móviles

### Proveedores Recomendados:

1. **Smartproxy** - Mobile proxies
   - $50/GB
   - 4G/5G real
   - Sticky sessions

2. **Soax** - Residential mobile
   - $99/8GB
   - Multi-carrier
   - Good for Instagram

3. **Proxy-Cheap** - Budget option
   - $30/5GB
   - Decent quality

### Configuración Óptima:

```python
mobile_proxy_config = {
    "url": "http://user:pass@gate.smartproxy.com:10001",
    "type": "mobile",
    "rotation": "sticky",  # ← IMPORTANTE
    "session_duration": 1800,  # 30 min
    "country": "US",
    "carrier": "T-Mobile",

    # Advanced
    "request_timeout": 30,
    "max_retries": 3,
    "verify_ssl": True
}
```

---

## 📊 Monitoreo de Cuentas

```python
# Revisar health diariamente
health = client.health_check()

if health['risk_score'] > 0.7:
    # STOP TODO
    send_alert("CRITICAL: Account at risk!")
    pause_all_activity(account_id)

elif health['risk_score'] > 0.5:
    # Reducir actividad
    reduce_posting_frequency(account_id)

elif health['risk_score'] < 0.3:
    # Safe, continuar
    continue_normal_activity()
```

---

## ✅ Checklist Pre-Post

Antes de cada post, verificar:

- [ ] Cuenta tiene más de 7 días
- [ ] No excedió límite diario de posts
- [ ] Último post fue hace >30 min
- [ ] Risk score < 0.5
- [ ] Proxy es móvil (no datacenter)
- [ ] GPS coords match proxy location
- [ ] Hora es razonable (8 AM - 11 PM del timezone del proxy)
- [ ] Caption está randomizado
- [ ] Ya hizo browsing/likes antes de postear
- [ ] No hay errores recientes (3+ fails)

Si TODO ✅ → Safe to post
Si ANY ❌ → WAIT

---

## 🎯 Estrategia Final

```python
# DÍA 1-7: WARMING
for day in range(1, 8):
    browse_feed(10-20 min)
    like_posts(5-15)
    view_profiles(3-8)
    # 0 posts

# DÍA 8-14: PRIMEROS POSTS
for day in range(8, 15):
    browse_feed(10 min)
    like_posts(20-30)
    post_1_photo()
    wait(30-60 min)
    browse_more(5 min)
    like_more(10-15)

# DÍA 15+: NORMAL (pero conservador)
for day in range(15, 365):
    morning_session():
        browse(10 min)
        like(30)

    afternoon_session():
        browse(5 min)
        post(1-2 photos)
        like(50)
        follow(10-15)

    evening_session():
        browse(15 min)
        post(1 photo)
        comment(5-10)
        like(40)
```

**NUNCA aceleres este proceso. Paciencia = Cuentas que duran.**

---

## 🚨 Señales de Warning

Si ves esto, PARA INMEDIATAMENTE:

1. **"Challenge Required"** - Instagram sospecha
2. **403 Forbidden** repetidos - IP flaggeada
3. **Rate limit errors** - Excediste límites
4. **"Try again later"** - Temporalmente bloqueado
5. **Login requiere verificación** - Cuenta under review

**Acción:** STOP 24-48 horas. Cambiar proxy. Reducir actividad.
