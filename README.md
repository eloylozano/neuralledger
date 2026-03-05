# 🧠 NeuralLedger: AI-Powered Invoice Management

NeuralLedger es una solución Full-Stack de última generación diseñada para automatizar la extracción y gestión de facturas mediante **Inteligencia Artificial local**. El sistema no solo extrae datos, sino que audita el comportamiento financiero y organiza el almacenamiento digital de forma inteligente y privada.



## 🚀 Características Principales

* **Extracción Inteligente:** Integración con LLMs locales (Llama 3.1/3.2, Mistral, Phi-3) vía Ollama para extracción de metadatos con privacidad total (GDPR compliant por diseño).
* **Interfaz Reactiva (Svelte 5):** Arquitectura basada completamente en **Svelte Runes** (`$state`, `$effect`, `$props`, `$bindable`) para una gestión de estado reactiva de alto rendimiento.
* **Dashboard de Auditoría:** Panel de control con métricas en tiempo real, gráficas de evolución de gasto (ApexCharts) e "Insights" automáticos generados por el motor neural sobre el estado de la base de datos.
* **Gestión de Base de Datos:** Herramientas integradas de mantenimiento para exportación/importación en JSON, re-indexación masiva de archivos y limpieza integral del sistema.
* **Almacenamiento Jerárquico:** Clasificación automática y normalización de documentos en la ruta: `storage/NombreEmpresa_CIF/Factura_XXX.pdf`.
* **UI/UX Premium:** Interfaz con efectos de Glassmorphism, sistema de temas dinámicos sincronizados (Dark/Light/Neural) y animaciones fluidas con Svelte Transition.

## 🛠️ Stack Tecnológico

* **Backend:** Python 3.12, FastAPI, SQLAlchemy (ORM), PyMuPDF (extracción de texto).
* **Frontend:** Svelte 5 (Runes), SvelteKit, Lucide Icons, ApexCharts.
* **AI/LLM:** Ollama (Orquestación local de modelos GGUF).
* **Base de Datos:** PostgreSQL 15 & SQLite (Soporte agnóstico mediante SQLAlchemy).
* **Validación:** Pydantic V2 para asegurar la integridad de datos financieros y esquemas de salida de la IA.

## 📂 Arquitectura del Proyecto

```text
neuralledger/
├── backend/                # API REST (FastAPI) y Lógica de Negocio
│   ├── models.py           # Modelos SQLAlchemy (Supplier, Invoice, InvoiceLine)
│   ├── schemas.py          # Validadores Pydantic (Esquemas de la IA)
│   ├── utils/              # Procesamiento de PDF y orquestación de prompts
│   └── storage/            # Volumen persistente de documentos clasificados
├── frontend/               # Interfaz de Usuario (SvelteKit + Runes)
│   ├── src/lib/components/ # Componentes (KpiCard, AiEngine, DbSettings)
│   └── src/routes/         # Vistas dinámicas y lógica de navegación
└── data/                   # Volúmenes de persistencia (Postgres & Ollama)
```

## ⚙️ Instalación y Despliegue
Requisitos Previos
- Docker y Docker Compose.

- Ollama instalado y ejecutándose en el host (para aprovechar aceleración por GPU/CUDA).

Pasos Rápidos

**1. Clonar el repositorio:**
```Bash
git clone [https://github.com/eloylozano/neuralledger.git](https://github.com/eloylozano/neuralledger.git)
cd neuralledger
```

**2. Configurar variables de entorno (.env):**

```Bash
DATABASE_URL=postgresql://user:pass@db:5432/neuralledger
OLLAMA_HOST=[http://host.docker.internal:11434](http://host.docker.internal:11434)
```

**3. Levantar la infraestructura:**

```
docker-compose up --build
```


## 🧠 Flujo de Datos y Auditoría
1. **Ingesta**: Subida de PDF mediante Dropzone reactiva.

2. **Procesamiento**: Extracción de texto y envío al LLM con un prompt de salida JSON estricto.

3. **Persistencia**: Almacenamiento relacionado (Proveedor -> Factura -> Líneas de detalle).

4. **Auditoría**: El Dashboard calcula automáticamente el volumen total, proveedores activos e identifica discrepancias mediante el motor de IA.

## 📝 Notas de Desarrollo Recientes
- **Optimización Svelte 5**: Implementación de lógica segura para evitar errores de compilación TSTypeCastExpression, garantizando un build de producción estable.

- **Coherencia Visual Dinámica**: Uso de color-mix en CSS para que sombras, pulsos de estado y fondos de iconos se sincronicen perfectamente con el color primario del tema seleccionado por el usuario.

- **Robustez de API**: Configuración de CORS dinámico para permitir operaciones avanzadas de mantenimiento (DELETE/OPTIONS) en la gestión de la base de datos.