<script>
  import Dropzone from "$lib/components/Dropzone.svelte";
  import LoadingBar from "$lib/components/LoadingBar.svelte";
  import { fade, fly } from "svelte/transition";

  let status = $state("idle");
  let uploadProgress = $state(0);
  let fileName = $state("");

  function handleFile(file) {
    fileName = file.name;
    status = "loading";
    simulateUpload();
  }

  function simulateUpload() {
    uploadProgress = 0;
    const interval = setInterval(() => {
      uploadProgress += Math.floor(Math.random() * 15) + 5;
      if (uploadProgress >= 100) {
        uploadProgress = 100;
        clearInterval(interval);
        setTimeout(() => {
          status = "editing";
        }, 800);
      }
    }, 400);
  }
</script>

<svelte:head>
  <title>NeuralLedger | Subir Factura</title>
</svelte:head>

<div class="upload-page-container">
  <div class="upload-content">
    <header class="text-center">
      <h1 in:fly={{ y: -20, duration: 500 }}>
        Procesar <span>Nueva Factura</span>
      </h1>
      <p in:fly={{ y: -10, duration: 500, delay: 200 }}>
        Sube tu documento en PDF y deja que la IA extraiga los datos por ti.
      </p>
    </header>

    <div class="content-wrapper">
      {#if status === "idle"}
        <div in:fade={{ duration: 300 }} out:fade={{ duration: 200 }}>
          <Dropzone onFileSelect={handleFile} />
        </div>
      {:else if status === "loading"}
        <div in:fade={{ duration: 300 }} out:fade={{ duration: 200 }}>
          <LoadingBar
            progress={uploadProgress}
            status="DeepSeek está analizando {fileName}..."
          />
        </div>
      {:else if status === "editing"}
        <div
          in:fly={{ y: 20, duration: 600 }}
          class="editor-placeholder glass-card"
        >
          <h2>🎉 ¡Factura Procesada!</h2>
          <p>
            Aquí irá el componente <strong>InvoiceEditor.svelte</strong> con la vista
            dividida.
          </p>
          <button onclick={() => (status = "idle")} class="reset-btn"
            >Subir otra</button
          >
        </div>
      {/if}
    </div>
  </div>
</div>

<style>
  /* Contenedor que ocupa todo el espacio disponible */
  .upload-page-container {
    height: 100%; /* Toma el alto del main-content del layout */
    display: flex;
    align-items: center; /* Centrado vertical */
    justify-content: center; /* Centrado horizontal */
  }

  .upload-content {
    width: 100%;
    max-width: 900px;
    padding-bottom: 5rem; /* Pequeño offset para que no se vea "tan abajo" visualmente */
  }

  header h1 {
    font-size: 3rem; /* Un poco más grande para llenar el espacio */
    margin-bottom: 0.75rem;
  }

  header h1 span {
    color: var(--primary);
  }

  header p {
    font-size: 1.1rem;
    color: var(--text-muted);
  }

  .content-wrapper {
    margin-top: 4rem;
    width: 100%;
    display: flex;
    justify-content: center;
  }

  /* Ajustamos el ancho del wrapper para que los componentes internos decidan su tamaño */
  .content-wrapper > div {
    width: 100%;
  }

  .editor-placeholder {
    padding: 4rem;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
  }

  .reset-btn {
    padding: 0.8rem 2rem;
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    color: var(--text-main);
    cursor: pointer;
    transition: 0.3s;
  }

  .reset-btn:hover {
    background: var(--primary);
    color: white;
    border-color: var(--primary);
    box-shadow: 0 0 20px rgba(0, 210, 255, 0.3);
  }
</style>
