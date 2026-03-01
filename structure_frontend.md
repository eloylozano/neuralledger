src/
├── lib/               # Componentes reutilizables (Botones, Cards, etc.)
│   └── components/
│       ├── GlassCard.svelte
│       └── FileUpload.svelte
├── routes/
│   ├── +layout.svelte # Tu Sidebar y lógica de paletas
│   ├── layout.css     # Estilos globales de las paletas
│   ├── +page.svelte   # El Dashboard (Home)
│   ├── upload/        # Carpeta para Subir Factura
│   │   └── +page.svelte
│   └── invoices/      # Carpeta para el Histórico
│       └── +page.svelte
└── app.html           # El esqueleto HTML