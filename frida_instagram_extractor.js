/**
 * FRIDA SCRIPT - INSTAGRAM iOS API EXTRACTOR
 * Extrae: signature keys, headers, endpoints, device info, payloads
 */

console.log("[+] Instagram iOS API Extractor iniciado");
console.log("[+] Buscando módulos de Instagram...\n");

// ========================================
// 1. INTERCEPTAR SIGNATURE KEYS (HMAC)
// ========================================
var CCHmac = Module.findExportByName("libcommonCrypto.dylib", "CCHmac");
if (CCHmac) {
    console.log("[✓] CCHmac encontrado en: " + CCHmac);

    Interceptor.attach(CCHmac, {
        onEnter: function(args) {
            // CCHmac(CCHmacAlgorithm algorithm, const void *key, size_t keyLength, const void *data, size_t dataLength, void *macOut)
            var algorithm = args[0].toInt32();
            var keyPtr = args[1];
            var keyLen = args[2].toInt32();
            var dataPtr = args[3];
            var dataLen = args[4].toInt32();

            // Solo capturar HMAC-SHA256 (algorithm = 2) con keys de tamaño razonable
            if (algorithm === 2 && keyLen >= 32 && keyLen <= 256) {
                try {
                    var key = Memory.readUtf8String(keyPtr, keyLen);
                    var data = Memory.readUtf8String(dataPtr, Math.min(dataLen, 500));

                    console.log("\n" + "=".repeat(80));
                    console.log("🔑 [SIGNATURE KEY DETECTED]");
                    console.log("=".repeat(80));
                    console.log("Algorithm: HMAC-SHA256");
                    console.log("Key Length: " + keyLen);
                    console.log("Key: " + key);
                    console.log("Data (first 500 chars): " + data);
                    console.log("=".repeat(80) + "\n");
                } catch (e) {
                    // Si falla UTF8, intentar como hex
                    try {
                        var keyHex = Memory.readByteArray(keyPtr, keyLen);
                        var keyHexStr = Array.from(new Uint8Array(keyHex))
                            .map(b => ('0' + b.toString(16)).slice(-2))
                            .join('');

                        console.log("\n" + "=".repeat(80));
                        console.log("🔑 [SIGNATURE KEY DETECTED - HEX]");
                        console.log("=".repeat(80));
                        console.log("Key (HEX): " + keyHexStr);
                        console.log("=".repeat(80) + "\n");
                    } catch (e2) {
                        // Ignorar
                    }
                }
            }
        }
    });
} else {
    console.log("[✗] CCHmac NO encontrado");
}

// ========================================
// 2. INTERCEPTAR REQUESTS HTTP
// ========================================
var NSURLSession = ObjC.classes.NSURLSession;
if (NSURLSession) {
    console.log("[✓] NSURLSession encontrado\n");

    // Interceptar dataTaskWithRequest
    Interceptor.attach(ObjC.classes.NSURLSession['- dataTaskWithRequest:completionHandler:'].implementation, {
        onEnter: function(args) {
            try {
                var request = new ObjC.Object(args[2]);
                var url = request.URL().absoluteString().toString();
                var method = request.HTTPMethod().toString();
                var headers = request.allHTTPHeaderFields();

                // Solo capturar requests de Instagram API
                if (url.includes("instagram.com") || url.includes("i.instagram.com")) {
                    console.log("\n" + "=".repeat(80));
                    console.log("🌐 [HTTP REQUEST DETECTED]");
                    console.log("=".repeat(80));
                    console.log("Method: " + method);
                    console.log("URL: " + url);
                    console.log("\n📋 Headers:");

                    if (headers) {
                        var headersDict = new ObjC.Object(headers);
                        var allKeys = headersDict.allKeys();
                        var count = allKeys.count();

                        for (var i = 0; i < count; i++) {
                            var key = allKeys.objectAtIndex_(i).toString();
                            var value = headersDict.objectForKey_(key).toString();
                            console.log("  " + key + ": " + value);
                        }
                    }

                    // Intentar leer el body
                    var body = request.HTTPBody();
                    if (body) {
                        try {
                            var bodyStr = ObjC.classes.NSString.alloc().initWithData_encoding_(body, 4).toString();
                            console.log("\n📦 Body:");
                            console.log(bodyStr);
                        } catch (e) {
                            console.log("\n📦 Body: (binary data)");
                        }
                    }

                    console.log("=".repeat(80) + "\n");
                }
            } catch (e) {
                console.log("[!] Error interceptando request: " + e);
            }
        }
    });
} else {
    console.log("[✗] NSURLSession NO encontrado");
}

// ========================================
// 3. INTERCEPTAR USER-AGENT
// ========================================
try {
    var userAgentClass = ObjC.classes.NSUserDefaults;
    if (userAgentClass) {
        console.log("[✓] Buscando User-Agent...");

        Interceptor.attach(ObjC.classes.NSUserDefaults['- objectForKey:'].implementation, {
            onEnter: function(args) {
                var key = new ObjC.Object(args[2]).toString();
                if (key.toLowerCase().includes("useragent") || key.toLowerCase().includes("user-agent")) {
                    this.captureUA = true;
                }
            },
            onLeave: function(retval) {
                if (this.captureUA && retval != 0) {
                    var ua = new ObjC.Object(retval).toString();
                    console.log("\n" + "=".repeat(80));
                    console.log("📱 [USER-AGENT DETECTED]");
                    console.log("=".repeat(80));
                    console.log(ua);
                    console.log("=".repeat(80) + "\n");
                }
            }
        });
    }
} catch (e) {
    console.log("[!] Error en User-Agent hook: " + e);
}

// ========================================
// 4. INTERCEPTAR DEVICE ID / UUID
// ========================================
try {
    var NSUUID = ObjC.classes.NSUUID;
    if (NSUUID) {
        console.log("[✓] Monitoreando UUIDs / Device IDs...");

        Interceptor.attach(ObjC.classes.NSUUID['- UUIDString'].implementation, {
            onLeave: function(retval) {
                if (retval != 0) {
                    var uuid = new ObjC.Object(retval).toString();
                    console.log("\n🆔 [UUID/Device ID]: " + uuid);
                }
            }
        });
    }
} catch (e) {
    console.log("[!] Error en UUID hook: " + e);
}

// ========================================
// 5. INTERCEPTAR STRINGS DE CONFIGURACIÓN
// ========================================
console.log("[✓] Monitoreando strings de configuración...\n");

// Interceptar NSString stringWithFormat para capturar device info
try {
    Interceptor.attach(ObjC.classes.NSString['+ stringWithFormat:'].implementation, {
        onEnter: function(args) {
            try {
                var format = new ObjC.Object(args[2]).toString();
                if (format.includes("iPhone") || format.includes("iOS") || format.includes("sig_key")) {
                    this.interesting = true;
                    this.format = format;
                }
            } catch (e) {}
        },
        onLeave: function(retval) {
            if (this.interesting && retval != 0) {
                try {
                    var result = new ObjC.Object(retval).toString();
                    console.log("\n📝 [String Config]: " + result);
                } catch (e) {}
            }
        }
    });
} catch (e) {
    console.log("[!] Error en string hook: " + e);
}

console.log("\n" + "=".repeat(80));
console.log("✅ TODOS LOS HOOKS ACTIVADOS");
console.log("=".repeat(80));
console.log("👉 Ahora usa Instagram en tu iPhone para generar requests");
console.log("👉 Los datos se mostrarán aquí en tiempo real");
console.log("=".repeat(80) + "\n");
