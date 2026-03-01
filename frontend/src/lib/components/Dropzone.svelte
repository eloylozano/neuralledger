<script>
  import { Upload, FileText, X } from "lucide-svelte";

  // Recibimos una función del padre para cuando el archivo esté listo
  let { onFileSelect } = $props();

  let isOver = $state(false);
  let file = $state(null);

  function handleDrop(e) {
    e.preventDefault();
    isOver = false;
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.type === "application/pdf") {
      file = droppedFile;
      onFileSelect(file);
    } else {
      alert("Por favor, sube un archivo PDF válido.");
    }
  }
</script>

<div
  class="dropzone-container glass-card {isOver ? 'active' : ''}"
  ondragover={(e) => {
    e.preventDefault();
    isOver = true;
  }}
  ondragleave={() => (isOver = false)}
  ondrop={handleDrop}
>
  {#if !file}
    <div class="info">
      <div class="icon-circle">
        <Upload size={32} />
      </div>
      <h3>Arrastra tu factura aquí</h3>
      <p>O haz clic para buscar en tu ordenador (.pdf)</p>
    </div>
  {:else}
    <div class="file-selected">
      <FileText size={40} color="var(--primary)" />
      <div class="file-info">
        <strong>{file.name}</strong>
        <span>{(file.size / 1024 / 1024).toFixed(2)} MB</span>
      </div>
      <button onclick={() => (file = null)} class="remove-btn">
        <X size={18} />
      </button>
    </div>
  {/if}
</div>

<style>
  .dropzone-container {
    width: 100%;
    max-width: 600px;
    height: 300px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px dashed var(--glass-border);
    transition: all 0.3s ease;
    cursor: pointer;
    margin: 0 auto;
  }

  .dropzone-container.active {
    border-color: var(--primary);
    background: rgba(var(--primary-rgb, 0, 210, 255), 0.05);
    transform: scale(1.02);
  }

  .info {
    text-align: center;
  }

  .icon-circle {
    width: 64px;
    height: 64px;
    background: var(--glass-bg);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1.5rem;
    color: var(--primary);
  }

  .file-selected {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    padding: 1rem 2rem;
    background: var(--glass-bg);
    border-radius: 16px;
    width: 80%;
  }

  .file-info {
    display: flex;
    flex-direction: column;
    flex: 1;
  }

  .remove-btn {
    background: none;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    padding: 5px;
  }
  .remove-btn:hover {
    color: #ff4b2b;
  }
</style>
