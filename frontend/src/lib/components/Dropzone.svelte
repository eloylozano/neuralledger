<script>
    import { UploadCloud } from "lucide-svelte";
    let { onFileSelect } = $props(); // Propiedad para devolver el archivo al padre
    let fileInput; // Referencia al input oculto
  
    function triggerExplorer() {
      fileInput.click(); // Al hacer clic en el div, clicamos el input real
    }
  
    function handleChange(e) {
      const file = e.target.files?.[0];
      if (file) onFileSelect(file);
    }
  
    function handleDrop(e) {
      e.preventDefault();
      const file = e.dataTransfer.files?.[0];
      if (file) onFileSelect(file);
    }
  </script>
  
  <div 
    class="dropzone-container glass-card"
    onclick={triggerExplorer}
    ondragover={(e) => e.preventDefault()}
    ondrop={handleDrop}
  >
    <input 
      type="file" 
      accept="application/pdf" 
      bind:this={fileInput} 
      onchange={handleChange} 
      hidden 
    />
    
    <div class="drop-content">
      <div class="icon-circle">
        <UploadCloud size={32} class="text-primary" />
      </div>
      <h3>Selecciona o arrastra una factura</h3>
      <p>Formatos aceptados: PDF (Máx. 10MB)</p>
    </div>
  </div>
  
  <style>
    .dropzone-container {
      padding: 4rem 2rem;
      border: 2px dashed var(--glass-border);
      cursor: pointer;
      transition: all 0.3s ease;
      text-align: center;
    }
    .dropzone-container:hover {
      border-color: var(--primary);
      background: rgba(0, 210, 255, 0.05);
      transform: scale(1.01);
    }
    .icon-circle {
      width: 64px;
      height: 64px;
      background: rgba(0, 210, 255, 0.1);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0 auto 1.5rem;
    }
    h3 { font-size: 1.25rem; margin-bottom: 0.5rem; }
    p { color: var(--text-muted); font-size: 0.9rem; }
  </style>