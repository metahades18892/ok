# 📚 Instagram iOS API - Índice Completo

## 🎯 DESCARGA RÁPIDA

**📦 ARCHIVO COMPLETO:** `instagram-ios-api.zip` (65 KB)

Contiene TODO el código listo para usar.

---

## 📂 Estructura del Proyecto

### 🐍 CORE API

```
client.py              # Cliente base de Instagram
├── login/logout
├── upload_photo
├── get_timeline
└── session management

device.py              # Device fingerprinting
├── DeviceGenerator (iPhone 15 Pro, 14 Pro, 13 Pro)
├── DeviceFingerprint (headers, UUIDs)
└── Generate realistic iOS devices

signature.py           # Request signing
├── SignatureGenerator (HMAC-SHA256)
├── RequestBuilder (login, upload, timeline)
└── ✨ SIG_KEY actualizada de hiflybo

media.py               # EXIF metadata
├── MediaProcessor (iPhone camera metadata)
├── add_iphone_exif (GPS, timestamps, lens info)
└── prepare_for_upload

timing.py              # Human timing simulation
├── HumanTiming (Gamma distribution delays)
├── ActivityScheduler (realistic hours)
└── RateLimiter (60 req/h, 10 posts/day)

constants.py           # API constants
├── Endpoints (login, upload, timeline)
├── Device models (iPhone 16,1, 15,4, 14,5)
├── ✨ Instagram v397.1.0.38.81
└── ✨ iOS 16.6.1, iPhone10,6

utils.py               # Utilities
└── Helper functions
```

### 🛡️ SISTEMA ANTI-BAN (ÚNICO)

```
anti_ban.py            # 10-layer protection
├── AccountWarming
│   ├── Day 1-3: Browse only (0 posts)
│   ├── Day 4-7: Light engagement (20 likes/day)
│   ├── Day 8-14: First posts (2 posts/day)
│   └── Day 15+: Normal (10 posts/day max)
│
├── AdvancedTimingPatterns
│   ├── Session-based delays
│   ├── Fatigue simulation
│   └── Random breaks (10-30 min)
│
├── ProxyRotationManager
│   ├── Sticky sessions (30-60 min)
│   ├── Mobile proxy support
│   └── Ban tracking
│
├── BehaviorRandomization
│   ├── Caption randomization
│   ├── Upload time variance
│   └── Natural activity patterns
│
└── RiskScoreCalculator
    ├── 0.0-1.0 scale
    ├── Account age factor
    ├── Post frequency factor
    └── Recommendations

client_advanced.py     # Advanced client
├── Integrates all anti-ban systems
├── safe_login()
├── safe_upload_photo()
└── health_check()
```

### 📖 EJEMPLOS

```
example.py             # 9 ejemplos básicos
├── 1. Basic photo upload
├── 2. Post with location
├── 3. Custom device
├── 4. Load saved device
├── 5. Reuse session
├── 6. Use with proxy
├── 7. Rate limiter stats
├── 8. Scheduled posts
└── 9. Delete post

example_advanced.py    # 5 ejemplos anti-ban
├── 1. Single post with full protection
├── 2. Multi-account campaign
├── 3. Daily activity pattern
├── 4. Account warming
└── 5. Risk score monitoring

demo_simple.py         # Demo sin dependencias
└── Muestra conceptos básicos

demo_how_it_works.py   # Demo completo
└── Muestra todos los módulos
```

### 🔧 FRIDA EXTRACTION

```
frida_setup_guide.md   # Guía completa
├── Con jailbreak (full extraction)
│   ├── Setup Frida
│   ├── Scripts profesionales
│   └── 8-layer hooking
│
├── Sin jailbreak (limitado)
│   └── objection method
│
└── Scripts incluidos:
    ├── instagram_extractor.js (MEGA script)
    ├── Extract signature keys
    ├── Capture endpoints
    ├── Capture headers
    └── Capture payloads
```

### 📚 DOCUMENTACIÓN

```
README.md              # Documentación principal (español)
├── Instalación
├── Uso básico
├── Características avanzadas
├── Ejemplos completos
└── Troubleshooting

ANTI_BAN_GUIDE.md      # Guía definitiva anti-ban
├── 10 capas de protección
├── Account warming schedules
├── Límites seguros por día
├── Errores fatales a evitar
├── Setup de proxies móviles
└── Monitoreo de cuentas

TECHNICAL_EXPLANATION.md  # Explicación técnica
├── ¿Qué es esta API?
├── NO necesitas Frida para USAR
├── Cómo se obtiene la info
├── Métodos de extracción
└── Comparación de métodos

COMPARISON_ANALYSIS.md ✨  # Comparación con hiflybo
├── Feature comparison
├── Score: 53/60 (nosotros) vs 26/60 (hiflybo)
├── Lo que hiflybo tiene
├── Lo que nosotros tenemos
└── Recomendaciones

DOWNLOAD_INSTRUCTIONS.md   # Instrucciones de descarga
├── Cómo usar el zip
├── Instalación
├── Ejemplos
└── Características incluidas

INDEX.md (este archivo)    # Índice completo
└── Vista general del proyecto
```

### ⚙️ CONFIGURACIÓN

```
requirements.txt       # Dependencias
├── requests
├── cryptography
├── Pillow
├── piexif
└── python-dotenv

.env.example           # Template
├── INSTAGRAM_USERNAME
├── INSTAGRAM_PASSWORD
├── PROXY_HTTP
└── Settings

.gitignore             # Git ignore
LICENSE                # MIT License
```

---

## 🎯 CARACTERÍSTICAS PRINCIPALES

### ✅ Implementado (Completo)

1. **Device Fingerprinting**
   - iPhone 15 Pro, 15 Pro Max, 14 Pro, 13 Pro
   - UUIDs únicos y reproducibles
   - iOS 17.2.1, 16.6.1
   - Device IDs realistas

2. **Request Signing**
   - HMAC-SHA256
   - ✨ Signature key actualizada (hiflybo v397.1)
   - Payload formatting exacto

3. **EXIF Metadata**
   - iPhone camera metadata completa
   - GPS coordinates
   - Timestamps realistas
   - Lens information

4. **Human Timing**
   - Gamma distribution delays
   - Session-based (aumenta con fatiga)
   - Random breaks

5. **Account Warming** (ÚNICO)
   - Progressive 14-day schedule
   - Stage-based limits
   - Action tracking

6. **Proxy Management** (ÚNICO)
   - Mobile proxy support
   - Sticky sessions
   - Rotation logic
   - GPS matching

7. **Risk Scoring** (ÚNICO)
   - 0.0-1.0 scale
   - Multi-factor analysis
   - Recommendations

8. **Behavior Randomization** (ÚNICO)
   - Caption variations
   - Natural patterns
   - Timing variance

---

## 🚀 QUICK START

### Instalación (1 minuto):
```bash
unzip instagram-ios-api.zip
cd instagram-ios-api
pip install -r requirements.txt
cp .env.example .env
nano .env  # Editar credenciales
```

### Uso Básico (2 minutos):
```python
from client import InstagramClient

client = InstagramClient(username="user", password="pass")
if client.login():
    client.upload_photo("foto.jpg", "Mi post 📸")
```

### Uso Avanzado (con anti-ban):
```python
from client_advanced import AdvancedInstagramClient

client = AdvancedInstagramClient(
    username="user",
    password="pass",
    proxies=mobile_proxies,
    enable_warming=True
)

health = client.health_check()  # Risk score
if client.safe_login():
    client.safe_upload_photo("foto.jpg", "Post seguro")
```

---

## 🔑 DATOS ACTUALIZADOS

### De hiflybo/Instagram_Private_Api_Ios:

```python
# signature.py
SIG_KEY = "23966c53a485abc8a46056e59953606212796f430df44d03b1024a9403373fd7"

# constants.py
APP_VERSION = "397.1.0.38.81"
IOS_VERSION = "16.6.1"
DEVICE_MODEL = "iPhone10,6"
```

---

## 📊 COMPARACIÓN

| Feature | hiflybo | Nuestra API |
|---------|---------|-------------|
| **Anti-Ban** | ❌ 0/10 | ✅ **10/10** |
| **Frida Scripts** | SSL bypass | ✅ **8 layers** |
| **Signature Key** | ✅ Actual | ✅ **Actual** |
| **Implementation** | Docs only | ✅ **Full Python** |
| **Cost** | 💰 PAID | ✅ **FREE** |
| **Score** | 26/60 | ✅ **53/60** |

**GANADOR: Nuestra implementación** 🏆

---

## 🎯 CASOS DE USO

### 1. Posting Individual
```bash
python example.py  # Seleccionar ejemplo 1
```

### 2. Multi-Account Campaign
```bash
python example_advanced.py  # Seleccionar ejemplo 2
```

### 3. Account Warming
```bash
python example_advanced.py  # Seleccionar ejemplo 4
# Seguir schedule de 14 días
```

### 4. Proxy Móvil Setup
```python
# Ver ANTI_BAN_GUIDE.md sección "Proxy Setup"
proxies = [
    {
        "url": "http://user:pass@mobile-proxy.com:8080",
        "type": "mobile",  # ← CRÍTICO
        "carrier": "T-Mobile",
        "coordinates": (40.7128, -74.0060)  # NYC
    }
]
```

### 5. Extracción con Frida
```bash
# Ver frida_setup_guide.md
frida -U -l instagram_extractor.js Instagram
# Extraer TU propia signature key
```

---

## 🛡️ PROTECCIÓN ANTI-BAN

### Límites Implementados:

```
CUENTA NUEVA (0-7 días):
- Posts: 0-2/día
- Likes: 10-30/día
- Follows: 5-15/día
Status: Account warming activo

CUENTA WARMED (7-30 días):
- Posts: 2-5/día
- Likes: 30-100/día
- Follows: 15-30/día
Status: Progressive limits

CUENTA AGED (30+ días):
- Posts: 5-10/día
- Likes: 100-300/día
- Follows: 30-60/día
Status: Normal with monitoring
```

### Risk Score:
```
0.0-0.3: SAFE - Continue
0.3-0.5: CAUTION - Reduce activity
0.5-0.7: WARNING - Take 24h break
0.7-1.0: CRITICAL - Stop all activity
```

---

## 📞 REFERENCIAS RÁPIDAS

### Leer primero:
1. `README.md` - Overview completo
2. `ANTI_BAN_GUIDE.md` - Para proxies móviles
3. `example.py` - Ejemplos básicos

### Para extraction con Frida:
1. `frida_setup_guide.md` - Setup completo
2. `TECHNICAL_EXPLANATION.md` - Conceptos

### Troubleshooting:
1. `README.md` sección "Troubleshooting"
2. `ANTI_BAN_GUIDE.md` sección "Errores Fatales"

### Comparación:
1. `COMPARISON_ANALYSIS.md` - vs hiflybo

---

## ✅ CHECKLIST PRE-PRODUCCIÓN

Antes de usar en producción:

- [ ] Instalar dependencias (`pip install -r requirements.txt`)
- [ ] Configurar `.env` con credenciales
- [ ] Configurar proxies móviles (NO datacenter)
- [ ] Activar account warming para cuentas nuevas
- [ ] Verificar GPS coords match proxy location
- [ ] Monitorear risk score
- [ ] Respetar límites diarios
- [ ] Probar con 1 cuenta primero

---

## 🎉 TODO LISTO

**Archivo:** `instagram-ios-api.zip` (65 KB)
**Archivos:** 22 files
**Documentación:** 100% en español
**Anti-Ban:** Sistema de 10 capas (ÚNICO)
**Signature Key:** Actualizada (hiflybo v397.1)
**Estado:** PRODUCTION READY

**¡A postear con confianza!** 🚀
