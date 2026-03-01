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
        // Preparamos el cuerpo exacto según tu schema 'InvoiceResponse'
        // Tu API espera los datos del proveedor y el nombre del archivo temporal
        const payload = {
          ...data.extracted,    // supplier_name, supplier_cif, items, etc.
          temp_file: data.temp_file // CRUCIAL: Para que FastAPI encuentre el PDF
        };
  
        const response = await fetch("http://localhost:8000/save-invoice/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
  
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || "Error al guardar en la DB");
        }
  
        const result = await response.json();
        
        saveSuccess = true;
        isDirty = false;
  
        // Esperamos un segundo para que el usuario vea el check de éxito antes de salir
        setTimeout(() => {
          onSave(result);
        }, 1000);
  
      } catch (error) {
        console.error("API Error:", error);
        alert("Error de NeuralLedger: " + error.message);
      } finally {
        isSaving = false;
      }
    }
  
    function handleCancel() {
      if (confirm("¿Estás seguro de que quieres descartar los cambios? El archivo temporal será eliminado.")) {
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
      color: white;
      border: none;
      padding: 0.8rem 2rem;
      border-radius: 10px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.3s ease;
      min-width: 220px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
    }
  
    .primary-action:hover:not(:disabled) {
      filter: brightness(1.1);
      box-shadow: 0 0 20px color-mix(in srgb, var(--primary), transparent 50%);
    }
  
    .primary-action.success {
      background: #10b981; /* Verde esmeralda para éxito */
    }
  
    .secondary-action {
      background: var(--glass-bg);
      border: 1px solid var(--glass-border);
      color: var(--text-main);
      padding: 0.8rem 1.5rem;
      border-radius: 10px;
      cursor: pointer;
    }
  
    button:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
  
    :global(.spinner) {
      animation: spin 1s linear infinite;
    }
  
    @keyframes spin {
      from { transform: rotate(0deg); }
      to { transform: rotate(360deg); }
    }
  </style>