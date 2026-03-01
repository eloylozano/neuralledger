<script>
  import { Save, RotateCcw } from "lucide-svelte";
  import { onMount } from "svelte";
  import SupplierInfo from "./SupplierInfo.svelte";
  import ArticleList from "./ArticleList.svelte";
  import Preview from "./PdfPreview.svelte";

  let { data, fileUrl, onSave, onCancel } = $props();

  // Estado para controlar si el formulario ha sido modificado
  // (Opcional: puedes ponerlo a true directamente si quieres que siempre avise)
  let isDirty = $state(true);

  $effect(() => {
    const handleBeforeUnload = (e) => {
      if (isDirty) {
        e.preventDefault();
        // Chrome requiere que se asigne un valor de retorno
        e.returnValue = "";
      }
    };

    window.addEventListener("beforeunload", handleBeforeUnload);

    // Limpieza al desmontar el componente
    return () => {
      window.removeEventListener("beforeunload", handleBeforeUnload);
    };
  });

  // Función envoltorio para guardar y desactivar el aviso
  function handleSave() {
    isDirty = false;
    onSave(data);
  }

  // Función envoltorio para descartar
  function handleCancel() {
    if (confirm("¿Estás seguro de que quieres descartar los cambios?")) {
      isDirty = false;
      onCancel();
    }
  }
</script>

<div class="editor-container">
  <div class="top-row">
    <SupplierInfo bind:data />
    <Preview {fileUrl} />
  </div>

  <ArticleList bind:items={data.items} />

  <div class="form-footer">
    <button
      class="secondary-action flex items-center gap-4"
      onclick={handleCancel}
    >
      <RotateCcw size={16} /> <span>Descartar</span>
    </button>
    <button class="primary-action flex items-center gap-4" onclick={handleSave}>
      <Save size={16} /> Confirmar Factura
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
    height: auto;
  }

  .form-footer {
    margin-top: 0.5rem;
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    padding: 1.5rem;
    border-top: 1px solid var(--glass-border);
  }

  /* Estilos globales de botones */
  .primary-action {
    background: var(--primary);
    color: white;
    border: none;
    padding: 0.8rem 1rem;
    border-radius: 10px;
    font-weight: 700;
    cursor: pointer;
    transition: 0.2s;
  }
  .primary-action:hover {
    filter: brightness(1.1);
    transform: translateY(-1px);
  }

  .secondary-action {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid var(--glass-border);
    color: var(--text-muted);
    padding: 0.8rem 1rem;
    border-radius: 10px;
    cursor: pointer;
  }
</style>
