# Instagram iOS API - Implementación Stealth 🔒

API ultra-camuflada para Instagram que imita perfectamente la aplicación oficial de iOS. Nivel militar de sigilo y anti-detección.

## 🎯 Características

### Camuflaje de Nivel Experto

- **Device Fingerprinting**: Genera huellas digitales de dispositivos iPhone 15 Pro/Max indistinguibles de dispositivos reales
- **Request Signing**: Firmas criptográficas HMAC-SHA256 idénticas a la app oficial
- **EXIF Metadata**: Inyección de metadatos de cámara iPhone realistas (modelo, GPS, timestamps, configuración de cámara)
- **TLS Fingerprinting**: Configuración SSL/TLS que imita el stack de red de iOS
- **Human Timing**: Simulación de patrones de comportamiento humano (delays variables, horarios realistas)
- **Rate Limiting**: Límites inteligentes para evitar detección
- **Header Rotation**: Headers dinámicos que cambian como la app real
- **Session Management**: Gestión de sesiones persistentes para reutilización

## 📋 Requisitos

- Python 3.8+
- Cuenta de Instagram
- (Opcional) Proxy para mayor anonimato

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone <tu-repo>
cd instagram-ios-api
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita `.env` con tus credenciales:

```env
INSTAGRAM_USERNAME=tu_usuario
INSTAGRAM_PASSWORD=tu_contraseña

# Proxy (opcional)
PROXY_HTTP=http://user:pass@proxy:port
PROXY_HTTPS=https://user:pass@proxy:port

# Configuración avanzada
USE_PROXY_ROTATION=false
DELAY_MIN=2
DELAY_MAX=8
MAX_RETRIES=3
```

## 💻 Uso Básico

### Ejemplo Simple: Subir una Foto

```python
from client import InstagramClient

# Crear cliente
client = InstagramClient(
    username="tu_usuario",
    password="tu_contraseña",
    use_timing=True  # Activar simulación de comportamiento humano
)

# Login
if client.login():
    # Subir foto
    response = client.upload_photo(
        image_path="mi_foto.jpg",
        caption="¡Mi primera publicación! 📸"
    )

    print(response)

    # Guardar sesión para reutilizar
    client.save_session("session.json")
    client.logout()
```

### Post con Ubicación y GPS

```python
from client import InstagramClient

client = InstagramClient(username="tu_usuario", password="tu_contraseña")

if client.login():
    # Datos de ubicación
    location = {
        "name": "Torre Eiffel",
        "lat": 48.858844,
        "lng": 2.294351,
        "external_id": "104512749",
        "external_id_source": "facebook_places"
    }

    # Coordenadas GPS para EXIF
    gps_coords = (48.858844, 2.294351)

    response = client.upload_photo(
        image_path="paris.jpg",
        caption="📍 París, Francia",
        location=location,
        gps_coords=gps_coords
    )

    client.logout()
```

### Usar Device Fingerprint Personalizado

```python
from device import DeviceGenerator
from client import InstagramClient

# Crear dispositivo específico con seed (reproducible)
device = DeviceGenerator(seed="mi-seed-unico")

# Ver información del dispositivo
print(f"Modelo: {device.device_name}")
print(f"iOS: {device.ios_version}")
print(f"UUID: {device.uuid}")

# Guardar device para reutilizar
device.save_to_file("mi_device.json")

# Usar device en cliente
client = InstagramClient(
    username="usuario",
    password="contraseña",
    device=device
)
```

### Cargar Sesión Guardada (Más Rápido)

```python
from client import InstagramClient

# Cargar sesión existente (sin hacer login de nuevo)
client = InstagramClient.load_session(
    filename="session.json",
    password="tu_contraseña"
)

# Ya está listo para usar
response = client.upload_photo("foto.jpg", "Usando sesión guardada ⚡")
```

### Usar con Proxy

```python
from client import InstagramClient

client = InstagramClient(
    username="usuario",
    password="contraseña",
    proxy="http://user:pass@proxy-server:8080"
)

if client.login():
    print("Conectado a través del proxy!")
```

## 🎨 Características Avanzadas

### 1. Programar Posts en Horarios Realistas

```python
from client import InstagramClient

client = InstagramClient(username="usuario", password="contraseña")

# Generar horario para 5 posts distribuidos en 12 horas
# Automáticamente evita horarios sospechosos (madrugada, etc.)
schedule = client.scheduler.schedule_posts(
    num_posts=5,
    spread_hours=12.0
)

for i, post_time in enumerate(schedule):
    print(f"Post {i+1}: {post_time}")
```

### 2. Verificar Rate Limits

```python
stats = client.rate_limiter.get_stats()

print(f"Requests en última hora: {stats['requests_last_hour']}")
print(f"Posts en últimas 24h: {stats['posts_last_24h']}")
print(f"Requests restantes: {stats['requests_remaining']}")
```

### 3. Procesar Imágenes con EXIF

```python
from media import MediaProcessor

processor = MediaProcessor(device_model="iPhone 15 Pro Max")

# Añadir metadata de iPhone a imagen
processor.add_iphone_exif(
    image_path="foto.jpg",
    output_path="foto_con_exif.jpg",
    gps_coords=(40.7128, -74.0060),  # NYC
    capture_time=None  # Usa tiempo reciente aleatorio
)
```

## 🔐 Características de Seguridad

### Device Fingerprinting

El sistema genera huellas digitales de dispositivos iOS completamente realistas:

- **UUIDs únicos**: Genera identificadores únicos reproducibles
- **Modelos actuales**: iPhone 15 Pro, iPhone 15 Pro Max, iPhone 14 Pro
- **Versiones iOS**: 17.2.1, 17.2, 17.1.2, etc.
- **Configuración realista**: Resolución de pantalla, densidad, procesador

### EXIF Metadata

Cada foto subida incluye metadata EXIF auténtica de iPhone:

- **Modelo de cámara**: iPhone 15 Pro back triple camera
- **Configuración**: Aperture, ISO, velocidad de obturación realistas
- **GPS**: Coordenadas, altitud, dirección
- **Timestamps**: Fecha/hora de captura con subsegundos
- **Lens information**: Especificaciones de lente de iPhone

### Request Signing

Todas las requests son firmadas criptográficamente:

- **HMAC-SHA256**: Firma igual que la app oficial
- **Signature key**: Extraída del binario de Instagram iOS
- **Payload formatting**: Formato JSON exacto que Instagram espera

### Human Behavior Simulation

El sistema imita comportamiento humano natural:

- **Typing delays**: Simula tiempo de escritura de captions
- **Action timing**: Delays variables entre acciones usando distribución Gamma
- **Smart scheduling**: Evita posts a las 3 AM, prefiere horarios prime (18:00-22:00)
- **Random variations**: Tiempos no uniformes, más naturales

## 📁 Estructura del Proyecto

```
instagram-ios-api/
├── client.py           # Cliente principal de la API
├── device.py          # Generación de device fingerprints
├── signature.py       # Firma criptográfica de requests
├── media.py           # Procesamiento de imágenes con EXIF
├── timing.py          # Simulación de comportamiento humano
├── constants.py       # Constantes de la API de Instagram
├── example.py         # Ejemplos de uso
├── requirements.txt   # Dependencias
├── .env.example       # Template de configuración
└── README.md          # Este archivo
```

## ⚙️ Módulos

### `client.py`
Cliente principal que integra todos los componentes:
- Login/logout
- Upload de fotos
- Gestión de sesiones
- Timeline feed
- User info

### `device.py`
Generación de device fingerprints:
- `DeviceGenerator`: Crea dispositivos iOS realistas
- `DeviceFingerprint`: Genera headers y metadata del dispositivo

### `signature.py`
Firma de requests:
- `SignatureGenerator`: Genera firmas HMAC-SHA256
- `RequestBuilder`: Construye payloads firmados

### `media.py`
Procesamiento de media:
- `MediaProcessor`: Añade EXIF metadata de iPhone
- Redimensionamiento para Instagram
- Generación de GPS IFD

### `timing.py`
Simulación de comportamiento humano:
- `HumanTiming`: Delays variables y realistas
- `ActivityScheduler`: Horarios de actividad naturales
- `RateLimiter`: Control de rate limiting

## 🎯 Nivel de Camuflaje

Este proyecto implementa **camuflaje de nivel experto** con:

### ✅ Nivel 1: Básico
- User-Agent correcto
- Headers básicos

### ✅ Nivel 2: Intermedio
- Device fingerprinting
- Request signing
- Session management

### ✅ Nivel 3: Avanzado
- EXIF metadata injection
- TLS fingerprinting
- Human timing patterns

### ✅ Nivel 4: Experto (IMPLEMENTADO)
- Gamma-distributed timing
- Smart scheduling (avoid 3 AM posts)
- GPS coordinates in EXIF
- Realistic camera settings
- Bandwidth simulation headers
- Pigeon session IDs
- Client context generation
- Battery level simulation
- Network type rotation

### ⚡ Nivel 5: Militar (FUTURO)
- ML-based behavior prediction
- Image similarity avoidance
- Network fingerprint rotation
- Advanced proxy chaining

## ⚠️ Consideraciones

### Legalidad y Ética

Este proyecto es para **fines educativos y de investigación**. El uso de esta herramienta debe cumplir con:

- Términos de servicio de Instagram
- Leyes locales sobre automatización
- Política de uso aceptable de tu jurisdicción

**No usar para:**
- Spam
- Harassment
- Violación de privacidad
- Actividades ilegales

### Límites Recomendados

Para evitar detección, respeta estos límites:

- **Posts**: Máximo 10 por día
- **Requests**: Máximo 60 por hora
- **Login**: Usar sesiones guardadas, no hacer login constantemente
- **Horarios**: Usar `ActivityScheduler` para horarios naturales

### Proxies

Se recomienda usar proxies residenciales para:
- Mayor anonimato
- Evitar bloqueos de IP
- Simular ubicaciones diferentes

## 🐛 Debugging

Activar logging detallado:

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## 📊 Ejemplos Completos

Ejecuta `example.py` para ver todos los ejemplos:

```bash
python example.py
```

Incluye:
1. Upload básico
2. Post con ubicación
3. Device personalizado
4. Cargar device guardado
5. Reutilizar sesión
6. Usar con proxy
7. Rate limiter stats
8. Posts programados
9. Eliminar post

## 🔧 Troubleshooting

### Error: "Challenge Required"

Instagram puede solicitar verificación. Soluciones:
- Verificar cuenta manualmente en la app oficial
- Usar proxy diferente
- Esperar 24-48 horas antes de reintentar
- Usar sesión guardada de login previo

### Error: "Login Failed"

- Verificar credenciales en `.env`
- Comprobar que la cuenta no esté bloqueada
- Intentar login manual en app oficial primero
- Usar 2FA si está activado

### Upload Failed

- Verificar que imagen existe
- Comprobar formato (JPG/PNG)
- Verificar tamaño (< 8MB recomendado)
- Revisar rate limits

## 🚀 Mejoras Futuras

- [ ] Soporte para videos
- [ ] Stories
- [ ] Reels
- [ ] Multi-account management
- [ ] Database logging
- [ ] Web dashboard
- [ ] Improved TLS fingerprinting usando curl_cffi
- [ ] ML-based caption generation
- [ ] Automatic hashtag optimization

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## ⭐ Soporte

Si este proyecto te ayuda, considera darle una estrella ⭐

## 📞 Contacto

Para preguntas o soporte, abre un issue en GitHub.

---

**Disclaimer**: Este proyecto es solo para fines educativos. El autor no se hace responsable del mal uso de esta herramienta.
