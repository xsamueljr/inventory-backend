# Objetivo

Este proyecto sigue una arquitectura hexagonal. Antes de realizar cualquier cambio debes entender cómo está organizado el código y mantener la consistencia con el resto del proyecto.

La prioridad es mantener el diseño existente, no introducir nuevas abstracciones.

---

# Arquitectura

Cada módulo sigue esta estructura:

module/
    application/
    domain/
    infrastructure/

Los módulos actuales son, entre otros:
- auth
- products
- users
- activity
- emails

---

# Capas

## Domain

Contiene únicamente lógica de dominio.

Aquí viven:
- entidades
- interfaces de repositorio
- excepciones de dominio

Nunca debe depender de infraestructura.

---

## Application

Contiene casos de uso.

Los casos de uso únicamente dependen de interfaces del dominio.

No deben conocer FastAPI, SQL ni Supabase.

---

## Infrastructure

Aquí viven:

- implementaciones de repositorios
- routers FastAPI
- DTOs HTTP
- dependencias
- adaptadores

Nunca colocar lógica de negocio aquí.

---

# Repositorios

Cada repositorio tiene:

- interfaz en domain
- implementación en memoria
- implementación SQLite
- implementación Supabase

Mantener siempre las tres implementaciones cuando se añadan métodos nuevos.

No romper la interfaz existente.

---

# Base de datos

Se usa PostgreSQL (Supabase) mediante psycopg escribiendo SQL manualmente.

SQLite sigue existiendo para desarrollo local.

No existe sistema de migraciones.

No introducir ORMs nuevos.

---

# FastAPI

Los routers únicamente llaman a casos de uso.

Los routers no contienen lógica de negocio.

Las dependencias se inyectan usando el sistema de dependencias de FastAPI.

---

# Excepciones

Existe un Global Exception Handler.

No capturar excepciones en cada router salvo que exista una necesidad real.

Los casos de uso deben lanzar excepciones de dominio.

---

# Estilo

Mantener el estilo ya existente.

No:

- introducir patrones nuevos
- cambiar nombres de clases
- reorganizar carpetas
- mover módulos
- modificar APIs existentes sin necesidad

Seguir siempre el patrón que ya exista en el proyecto.

---

# Calidad

Antes de finalizar:

- eliminar imports sin usar
- evitar código duplicado
- comprobar que no se rompen interfaces existentes
- mantener nombres consistentes
- reutilizar código existente siempre que sea posible

No hacer refactors no relacionados con la tarea.

Si detectas mejoras fuera del alcance, deja un comentario TODO en lugar de implementarlas.

---

# Si hay dudas

Priorizar siempre:

1. mantener compatibilidad
2. seguir el estilo existente
3. hacer el menor cambio posible

Nunca inventar comportamiento que no haya sido solicitado explícitamente.
