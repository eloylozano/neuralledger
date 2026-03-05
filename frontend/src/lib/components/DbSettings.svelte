<script lang="ts">
    import { RefreshCw, Download, Upload, Trash2 } from "lucide-svelte";
  
    let isProcessing = $state(false);
    let fileInput: HTMLInputElement;
  
    async function handleReindex() {
      if (isProcessing) return;
      isProcessing = true;
      try {
        const response = await fetch("http://localhost:8000/api/maintenance/reindex", { method: "POST" });
        const result = await response.json();
        if (result.success) alert(`Éxito: ${result.count} facturas.`);
      } catch (e) { alert("Error de conexión"); }
      finally { isProcessing = false; }
    }
  
    async function handleDBExport() {
      isProcessing = true;
      try {
        const response = await fetch("http://localhost:8000/api/db/export");
        const data = await response.json();
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = `backup-${Date.now()}.json`;
        link.click();
      } catch (e) { alert("Error exportando"); }
      finally { isProcessing = false; }
    }
  
    // Simplificamos la función para evitar el error del compilador
    async function handleDBImport(event: any) {
      const file = event.target?.files?.[0];
      if (!file || !confirm("¿Sobrescribir base de datos?")) return;
  
      isProcessing = true;
      const reader = new FileReader();
      reader.onload = async (e: any) => {
        try {
          const content = JSON.parse(e.target.result);
          const response = await fetch("http://localhost:8000/api/db/import", {
            method: "POST",
            body: JSON.stringify(content),
            headers: { "Content-Type": "application/json" },
          });
          if (response.ok) alert("Restaurado con éxito");
        } catch (err) { alert("Archivo inválido"); }
        finally { 
          isProcessing = false;
          if (event.target) event.target.value = ""; 
        }
      };
      reader.readAsText(file);
    }
  
    async function handleClearData() {
      if (!confirm("¿Borrar todo?")) return;
      try {
        await fetch("http://localhost:8000/api/db/clear", { method: "DELETE" });
        localStorage.clear();
        window.location.reload();
      } catch (e) { alert("Error al borrar"); }
    }
  </script>

<input
  type="file"
  accept=".json"
  bind:this={fileInput}
  onchange={handleDBImport}
  style="display: none;"
/>

<div class="action-buttons">
  <button class="btn-secondary" onclick={handleReindex} disabled={isProcessing}>
    <RefreshCw size={16} class={isProcessing ? "spin" : ""} />
    {isProcessing ? "Procesando..." : "Re-indexar Facturas"}
  </button>

  <button
    class="btn-secondary"
    onclick={handleDBExport}
    disabled={isProcessing}
  >
    <Download size={16} /> Exportar DB (JSON)
  </button>

  <button
    class="btn-secondary"
    onclick={() => fileInput.click()}
    disabled={isProcessing}
  >
    <Upload size={16} /> Importar DB (JSON)
  </button>

  <button class="btn-danger" onclick={handleClearData} disabled={isProcessing}>
    <Trash2 size={16} /> Borrar todo
  </button>
</div>

<style>
  .action-buttons {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
    flex-wrap: wrap;
  }

  .btn-secondary,
  .btn-danger {
    padding: 0.7rem 1.2rem;
    border-radius: 10px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: 0.2s;
    font-size: 0.9rem;
  }

  .btn-secondary {
    background: var(--glass-bg);
    color: var(--text-main);
    border: 1px solid var(--glass-border);
  }

  .btn-danger {
    background: rgba(255, 50, 50, 0.1);
    color: #ff4444;
    border: 1px solid rgba(255, 0, 0, 0.2);
    margin-left: auto;
  }

  .btn-secondary:hover {
    background: rgba(255, 255, 255, 0.15);
  }
  .btn-danger:hover {
    background: rgba(255, 50, 50, 0.2);
  }

  :global(.spin) {
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

  button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
</style>
