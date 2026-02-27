src/routes/
├── +layout.svelte       <-- Menú lateral y diseño global
├── +page.svelte         <-- Dashboard (Resumen)
├── upload/
│   └── +page.svelte     <-- Aquí va el "Drag & Drop" y el Editor
└── invoices/
    └── +page.svelte     <-- Listado tipo Drive (llama a GET /invoices/)