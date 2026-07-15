# 📦 Backend - Sistema de Gestión de Inventario y Ventas

> **Caso de Éxito Real:** Backend de grado empresarial diseñado, desarrollado e implementado durante mis prácticas profesionales para automatizar el control de stock, registro de transacciones y alertas automáticas de una empresa real. Actualmente se encuentra **desplegado en producción (Vercel)** y es utilizado activamente en el día a día de la compañía.

Este proyecto expone una API REST robusta desarrollada con **FastAPI** que sirve como motor para una aplicación de inventariado. Su diseño se rige bajo los principios de la **Arquitectura Hexagonal (Ports & Adapters)**, logrando un desacoplamiento total entre la lógica de negocio, las bases de datos y los servicios externos.

---

## 🌟 ¿Por qué Arquitectura Hexagonal? (Decisión de Diseño)

A diferencia de los típicos proyectos escolares estructurados en capas acopladas, decidí implementar **Arquitectura Hexagonal** para separar la lógica del dominio de la infraestructura (la base de datos, el envío de correos, etc.). 

Esto aportó dos beneficios críticos al proyecto:
1. **Testabilidad sin fricción:** Me permitió implementar tests unitarios de los casos de uso de manera sumamente sencilla y limpia, utilizando *mocks* para simular la persistencia y los servicios externos.
2. **Seguridad y Confianza al iterar:** Me proporcionó una enorme tranquilidad y seguridad al momento de modificar o añadir código para implementar nuevas funcionalidades, sabiendo que las reglas de negocio estaban totalmente blindadas y validadas por la suite de pruebas.

---

## 🚀 Características Principales

*   **Autenticación y Seguridad:** Implementación de seguridad robusta basada en tokens **JWT (JSON Web Tokens)** para proteger los endpoints y asegurar que solo el personal autorizado acceda al sistema.
*   **Feature Flags (Habilitación Dinámica):**
    *   `ENABLE_REGISTER`: Permite activar o desactivar el registro público de nuevos vendedores desde las variables de entorno para evitar accesos no deseados una vez configurado el equipo inicial.
    *   `SEND_REAL_EMAILS`: Permite testear o desarrollar el sistema de forma segura. Si está desactivado, el backend simula el flujo sin realizar llamadas SMTP reales; si está activado, despacha los correos utilizando el servidor SMTP de Gmail de producción.
*   **Notificaciones por Correo en Tiempo Real:** Envío automático de reportes al correo de administración/gerencia cada vez que se registra una venta, y alertas inmediatas cuando un producto baja de su stock mínimo de seguridad.
*   **Seguridad y CORS Configurable:** El backend protege sus endpoints limitando el origen de las peticiones. Recibe la URL del frontend como variable de entorno, configurando de forma dinámica el CORS para que solo admita peticiones legítimas desde la interfaz de usuario.
*   **Soporte Multientorno Inteligente (PostgreSQL & SQLite):** 
    *   **Producción (PostgreSQL en Supabase):** Conexión unificada de alta velocidad a través de un string de conexión de Supabase.
    *   **Desarrollo/Local (SQLite):** Configuración automática "Zero-Setup" especificando una ruta local. Al arrancar en local, los repositorios SQLite (implementados bajo el patrón Singleton para optimizar recursos y conexiones) detectan si las tablas no existen y las construyen automáticamente sobre la marcha.
*   **Auditoría y Trazabilidad:** Historial de acciones críticas por vendedor (creación de producto, entradas de mercancía, ventas, etc.), permitiendo un control transparente de las operaciones diarias.
*   **Suite de Pruebas Automatizadas:** Cobertura de tests unitarios y de integración para garantizar el correcto funcionamiento de todos los casos de uso principales.

---

## 🛠️ Stack Tecnológico

*   **Lenguaje:** Python 3.10+
*   **Framework API:** FastAPI
*   **Validación de Datos:** Pydantic V2 (Validación estricta y tipado estático de variables de entorno)
*   **Arquitectura:** Hexagonal (Ports & Adapters)
*   **Bases de Datos:** PostgreSQL (Supabase en Producción) / SQLite (Entorno Local)
*   **Testing:** Pytest
*   **Despliegue:** Vercel (Serverless)

---

## ⚙️ Configuración y Variables de Entorno

El sistema cuenta con un sistema estricto de validación de configuración en tiempo de ejecución utilizando **Pydantic**. 

Crea un archivo `.env` en la raíz del proyecto basándote en esta [plantilla de configuración](./.env.example)

---

## 💻 Instalación y Ejecución en Local

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/tu-repo-backend.git
cd tu-repo-backend
```

### 2. Crear y activar el entorno virtual
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/macOS:
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Lanzar el servidor en modo desarrollo
```bash
uvicorn main:app --reload
```
*El backend se levantará en `http://127.0.0.1:8000`. Puedes acceder a la documentación interactiva de la API en `/docs`.*

---

## 🧪 Ejecución de Tests

Para validar la integridad del sistema y verificar que todos los casos de uso funcionan perfectamente bajo los estándares de la arquitectura hexagonal, ejecuta:

```bash
pytest
```