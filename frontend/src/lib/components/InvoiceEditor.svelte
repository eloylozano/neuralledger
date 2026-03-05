<script>
  import { Save, RotateCcw, Loader2, CheckCircle2 } from "lucide-svelte";
  import SupplierInfo from "./SupplierInfo.svelte";
  import ArticleList from "./ArticleList.svelte";
  import Preview from "./PdfPreview.svelte";

  // Recibimos 'data' que viene de la respuesta de '/process-invoice/'
  // 'data' debe contener: extracted, temp_file, etc.
  let { data, fileUrl, onSave, onCancel } = $props();

  let isDirty = $state(true);
  let isSaving = $state(false);
  let saveSuccess = $state(false);

  // Bloqueo de recarga
  $effect(() => {
    const handleBeforeUnload = (e) => {
      if (isDirty) {
        e.preventDefault();
        e.returnValue = "";
      }
    };
    window.addEventListener("beforeunload", handleBeforeUnload);
    return () => window.removeEventListener("beforeunload", handleBeforeUnload);
  });

  async function handleSave() {
    if (isSaving) return;
    isSaving = true;

    try {
      const ext = data.extracted;

      // Construimos el objeto EXACTO que pide schemas.py
      const payload = {
        id: ext.id || null, // Si existe, se envía para edición
        supplier_name: ext.supplier_name,
        supplier_cif: ext.supplier_cif,
        date: ext.date || "",
        invoice_num: ext.invoice_num,
        taxable_base: Number(ext.taxable_base) || 0,
        vat: Number(ext.vat) || 0,
        discount: Number(ext.discount) || 0,
        total: Number(ext.total) || 0,
        ia_notes: ext.ia_notes || "",
        temp_file: data.temp_file || null,
        items: (ext.items || []).map((item, index) => ({
          position: item.position || index + 1,
          description: item.description || "Sin descripción",
          quantity: Number(item.quantity) || 0,
          price: Number(item.price) || 0,
          tax: Number(item.tax) || 0.0,
          discount: Number(item.discount) || 0,
          total_item: Number(item.total_item) || 0,
          ia_notes: item.ia_notes || "",
        })),
      };

      console.log("Enviando Payload:", payload); // Revisa esto en la consola F12

      const response = await fetch("http://localhost:8000/save-invoice/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json();
        // Esto te dirá exactamente qué campo falla en el alert
        const detail = JSON.stringify(errorData.detail);
        throw new Error(detail);
      }

      const result = await response.json();
      saveSuccess = true;
      isDirty = false;

      setTimeout(() => {
        onSave(result);
      }, 1000);
    } catch (error) {
      console.error("API Error:", error);
      alert("Error de validación: " + error.message);
    } finally {
      isSaving = false;
    }
  }

  function handleCancel() {
    if (
      confirm(
        "¿Estás seguro de que quieres descartar los cambios? El archivo temporal será eliminado."
      )
    ) {
      isDirty = false;
      onCancel();
    }
  }
</script>

<div class="editor-container">
  <div class="top-row">
    <SupplierInfo bind:data={data.extracted} />
    <Preview {fileUrl} />
  </div>

  <ArticleList bind:items={data.extracted.items} />

  <div class="form-footer">
    <button
      class="secondary-action flex items-center gap-2"
      onclick={handleCancel}
      disabled={isSaving}
    >
      <RotateCcw size={16} /> <span>Descartar</span>
    </button>

    <button
      class="primary-action flex items-center gap-2"
      class:success={saveSuccess}
      onclick={handleSave}
      disabled={isSaving || saveSuccess}
    >
      {#if isSaving}
        <Loader2 size={16} class="spinner" />
        <span>Procesando en DB...</span>
      {:else if saveSuccess}
        <CheckCircle2 size={16} />
        <span>¡Guardado!</span>
      {:else}
        <Save size={16} />
        <span>Confirmar y Archivar</span>
      {/if}
    </button>
  </div>
</div>

<style>
  .editor-container {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    max-width: 1400px;
    margin: 0 auto;
    width: 95%;
    padding: 1rem 0;
  }

  .top-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
  }

  .form-footer {
    margin-top: 0.5rem;
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    padding: 1.5rem;
    border-top: 1px solid var(--glass-border);
  }
  .primary-action {
    background: var(--primary);
    /* FORZAMOS COLOR OSCURO SÓLIDO */
    color: white !important;
    border: none;
    padding: 0.8rem 2rem;
    border-radius: 10px;
    font-weight: 800; /* Fuente extra gruesa para compensar el brillo */
    cursor: pointer;
    transition: all 0.3s ease;
    min-width: 220px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
  }

  /* Aseguramos que el span interno no herede el blanco transparente */
  .primary-action span {
    color: white !important;
    opacity: 1 !important;
  }

  /* Aseguramos que los iconos de Lucide también sean oscuros */
  .primary-action :global(svg) {
    color: white !important;
    stroke-width: 3px; /* Iconos más definidos */
  }

  .primary-action:hover:not(:disabled) {
    filter: brightness(1.1);
    transform: translateY(-2px);
    box-shadow: 0 8px 25px color-mix(in srgb, var(--primary), transparent 40%);
  }

  .primary-action.success {
    background: #10b981;
    color: white !important;
  }

  .primary-action.success span,
  .primary-action.success :global(svg) {
    color: white !important;
  }
  .secondary-action {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    color: var(--text-main);
    padding: 0.8rem 1.5rem;
    border-radius: 10px;
    cursor: pointer;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); /* Animación fluida */
    position: relative;
    overflow: hidden;
  }

  /* Animación al hacer Hover */
  .secondary-action:hover:not(:disabled) {
    background: rgba(239, 68, 68, 0.1); /* Un toque rojo muy sutil */
    border-color: rgba(239, 68, 68, 0.4);
    color: #ef4444; /* Rojo suave (Tailwind red-500) */
    transform: translateY(-2px); /* Se mueve ligeramente a la izquierda */
  }

  /* Animación del icono de flecha/rotar */
  .secondary-action:hover :global(svg) {
    transform: rotate(-335deg); /* El icono gira hacia atrás */
    transition: transform 0.4s ease;
  }

  /* Efecto de pulsación al hacer click */
  .secondary-action:active:not(:disabled) {
    transform: scale(0.95) translateX(-4px);
  }

  button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    filter: grayscale(1);
  }

  :global(.spinner) {
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
  }
</style>
