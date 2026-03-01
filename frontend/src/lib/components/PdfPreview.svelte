<script>
  import { FileText } from "lucide-svelte";
  let { fileUrl } = $props();
</script>

<div class="glass-card preview-box">
  <div class="column-header">
    <span>Vista del Documento</span>
  </div>
  <div class="pdf-container">
    <iframe src="{fileUrl}#view=FitH&toolbar=0" title="PDF"></iframe>
  </div>
</div>

<style>
  .preview-box {
    padding: 24px;
    display: flex;
    flex-direction: column;
    height: 100%;
  }
  .pdf-container {
    flex: 1;
    border-radius: 8px;
    overflow: hidden;
    background: #020617;
    border: 1px solid var(--glass-border);
  }
  iframe {
    width: 100%;
    height: 100%;
    border: none;
  }
</style>
