
# 🧠 NeuralLedger: AI-Powered Invoice Management

NeuralLedger es una solución Full-Stack diseñada para automatizar la extracción y gestión de facturas mediante Inteligencia Artificial local. El sistema procesa documentos PDF, extrae datos estructurados (JSON) utilizando LLMs y organiza automáticamente el almacenamiento físico y digital de los documentos.



## 🚀 Características Principales

* **Extracción Inteligente:** Integración con LLMs locales (Llama 3.2, Phi-3) vía Ollama para extraer metadatos sin enviar datos a la nube.
* **Procesamiento de PDF:** Motor de extracción de texto basado en PyMuPDF (fitz).
* **Almacenamiento Organizado:** Sistema de archivos dinámico que clasifica los documentos en carpetas jerárquicas: `storage/NombreEmpresa_CIF/Factura_XXX.pdf`.
* **Validación de Datos:** Capa de validación estricta con Pydantic para asegurar la integridad de los datos financieros antes de su persistencia.
* **Infraestructura Robusta:** Arquitectura orquestada con Docker y persistencia en PostgreSQL.

## 🛠️ Stack Tecnológico

* **Backend:** Python 3.12, FastAPI, SQLAlchemy (ORM).
* **Frontend:** Svelte / SvelteKit, Tailwind CSS.
* **AI/LLM:** Ollama (Llama 3.2 3B / Llama 3.2 1B).
* **Base de Datos:** PostgreSQL 15.
* **DevOps:** Docker, Docker Compose.

## 📂 Arquitectura del Proyecto

```text
neuralledger/
├── backend/                # API REST con FastAPI y Lógica de Negocio
│   ├── utils/              # Procesamiento de PDF y Prompts para LLM
│   └── storage/            # Volumen para persistencia de documentos PDF
├── frontend/               # Interfaz de usuario reactiva con SvelteKit
├── data/                   # Volúmenes persistentes (Postgres & Ollama)
└── docker-compose.yml      # Orquestación de microservicios

```

## ⚙️ Instalación y Despliegue

### Requisitos Previos

* Docker y Docker Compose.
* Ollama instalado en el host (para aceleración por GPU).

### Pasos

1. **Clonar el repositorio:**
```bash
git clone [https://github.com/eloylozano/neuralledger.git](https://github.com/eloylozano/neuralledger.git)
cd neuralledger

```


2. **Configurar variables de entorno:**
Crea un archivo `.env` basado en el ejemplo:
```env
DATABASE_URL=postgresql://user:pass@db:5432/neuralledger
OLLAMA_HOST=[http://host.docker.internal:11434](http://host.docker.internal:11434)

```


3. **Levantar la infraestructura:**
```bash
docker-compose up --build

```



La API estará disponible en `http://localhost:8000/docs` y el Frontend en `http://localhost:5173`.

## 🧠 Flujo de Datos (Data Pipeline)

1. **Ingesta:** El usuario sube un PDF a través de la Dropzone en Svelte.
2. **Extracción:** El Backend procesa el PDF, limpia el texto y envía un prompt estructurado al LLM local.
3. **Validación:** Se normalizan los campos (impuestos, totales, fechas) mediante validadores de Pydantic.
4. **Persistencia:** Los datos se guardan en PostgreSQL y el archivo físico se mueve de un estado temporal a su carpeta final clasificada por proveedor.

## 📝 Notas de Desarrollo

Este proyecto implementa patrones avanzados como:

* **Manejo de estados temporales de archivos** para evitar la acumulación de basura en el servidor.
* **Normalización de nombres de archivos y carpetas** mediante expresiones regulares para compatibilidad entre SO.
* **CORS dinámico** y manejo de errores asíncronos en FastAPI.

```