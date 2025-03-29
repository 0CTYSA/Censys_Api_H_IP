# 🔍 Censys IP Lookup Tool v2.0

![Python](https://img.shields.io/badge/python-3.6%2B-blue)
![API](https://img.shields.io/badge/Censys-API%20v2-orange)

Herramienta CLI para consulta avanzada de información de IPs usando Censys API v2 con soporte para paginación.

## 🌟 Novedades (v2.0)

- ✅ **Nuevo endpoint** `/hosts/{ip}/names` implementado
- 🔄 **Paginación automática** para resultados completos
- 📊 **Dos tipos de consulta** en un solo comando:
  - Información básica del host
  - Todos los nombres DNS asociados
- 📁 **Salida estructurada** en múltiples archivos JSON

## 📦 Instalación rápida

```bash
git clone https://github.com/0CTYSA/Censys_Api_H_IP.git
cd Censys_Api_H_IP
pip install requests
```

## 🛠 Configuración

Edita `censys_t.py` con tus credenciales:

```python
API_ID = "tu-api-id"          # Reemplaza esto
API_SECRET = "tu-api-secret"  # Reemplaza esto
```

## 🖥 Uso básico

```bash
python censys_query.py

=== Censys API v2 ===
Ingrese la IP: 1.1.1.1

[1/2] Obteniendo información del host...
✔ ASN: 13335 (CLOUDFLARENET)
✔ Puertos abiertos: 3
✔ Guardado en 1.1.1.1_censys_info.json

[2/2] Buscando nombres asociados...
✔ Total nombres encontrados: 47
✔ Ejemplos: one.one.one.one, cloudflare.com...
✔ Guardado en 1.1.1.1_censys_nombres.json
```

## 📌 Características clave

| Función         | Descripción                                  | Endpoint               |
| --------------- | -------------------------------------------- | ---------------------- |
| **Host Lookup** | Información básica del IP                    | `/v2/hosts/{ip}`       |
| **DNS Names**   | Todos los nombres asociados (paginado)       | `/v2/hosts/{ip}/names` |
| **Paginación**  | Obtiene todos los resultados automáticamente | Parámetros `cursor`    |

## 📂 Estructura de salida

```json
// Archivo _info.json
{
  "ip": "1.1.1.1",
  "asn": "13335",
  "organization": "CLOUDFLARENET",
  "ports": [80, 443, 53]
}

// Archivo _nombres.json
["one.one.one.one", "cloudflare.com", "..."]
```

## ⚠️ Límites importantes

- **Tasa de peticiones**: Máx. 30 consultas/minuto
- **Paginación**: Hasta 1,000 registros por página
- **Créditos**: Cada consulta consume créditos de API

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE) para detalles.
