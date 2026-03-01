<script>
  import { FileText } from "lucide-svelte";
  let { fileUrl } = $props();
</script>

<div class="glass-card preview-box">
  <div class="column-header">
    <div class="header-left">
      <span>Vista del Documento</span>
    </div>
  </div>

  <div class="pdf-container">
    <iframe src="{fileUrl}#view=FitH&toolbar=0" title="PDF"></iframe>
    
    <div class="pdf-overlay"></div>
  </div>
</div>

<style>
  .preview-box {
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    height: 100%;
    box-sizing: border-box;
  }

  .column-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.25rem;
  }

  .header-left {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 0.75rem;
    font-weight: 800;
    color: var(--text-main);
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  .pdf-container {
    position: relative;
    flex: 1;
    border-radius: 12px;
    overflow: hidden;
    /* Fondo que se adapta al tema para evitar el flash blanco */
    background: color-mix(in srgb, var(--bg-main), black 20%);
    border: 1px solid var(--glass-border);
    box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.2);
    min-height: 400px;
  }

  iframe {
    width: 100%;
    height: 100%;
    border: none;
    background: white; /* El PDF suele ser blanco, esto evita bordes extraños */
  }

  /* Línea de acento neural en la parte superior del contenedor */
  .pdf-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--primary), transparent);
    opacity: 0.5;
    pointer-events: none;
  }

  .text-primary {
    color: var(--primary);
    /* Resplandor sutil para el icono */
    filter: drop-shadow(0 0 5px color-mix(in srgb, var(--primary), transparent 60%));
  }

  /* Ajuste para temas claros */
  :global(.light-mode) .pdf-container {
    background: #f8fafc;
    box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.05);
  }
</style>