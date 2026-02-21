neuralledger/
├── docker-compose.yml          # Orquestador de todos los servicios
├── .env                        # Variables de entorno (DB_USER, PASS, etc.)
│
├── backend/                    # API con FastAPI
│   ├── main.py                 # Punto de entrada de la aplicación
│   ├── database.py             # Configuración de SQLAlchemy/SQLModel
│   ├── models.py               # Definición de tablas (Proveedor, Factura)
│   ├── schemas.py              # Esquemas Pydantic para el LLM y validación
│   ├── utils/
│   │   └── pdf_processor.py    # Lógica de PyMuPDF y prompts para el LLM
│   ├── storage/                # Carpeta local donde se guardarán los PDFs (volumen)
│   ├── Dockerfile              # Configuración de imagen Docker para Python
│   └── requirements.txt        # Librerías (fastapi, sqlalchemy, pymupdf, etc.)
│
├── frontend/                   # Aplicación Svelte (SvelteKit recomendado)
│   ├── src/
│   │   ├── lib/
│   │   │   ├── components/     # Dropzone, InvoiceForm, PDFViewer
│   │   │   └── api.js          # Funciones fetch para conectar con el backend
│   │   └── routes/             # Páginas (Home, Listado de Facturas, Detalle)
│   ├── static/                 # Assets estáticos
│   ├── Dockerfile              # Configuración de imagen Docker para Node/Svelte
│   └── package.json            # Dependencias de JS
│
└── data/                       # Carpeta persistente fuera de los contenedores
    ├── postgres_data/          # Datos de la base de datos PostgreSQL
    └── ollama_data/            # Modelos descargados (Llama3, etc.)