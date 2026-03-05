<script>
  import Dropzone from "$lib/components/Dropzone.svelte";
  import InvoiceEditor from "$lib/components/InvoiceEditor.svelte";
  import LoadingBar from "$lib/components/LoadingBar.svelte";
  import { fade, fly } from "svelte/transition";
  import { onDestroy } from "svelte";

  let fileUrl = $state("");
  let fileName = $state(""); // <-- ¡FALTABA ESTO!
  let uploadProgress = $state(0);
  let status = $state("idle");
  let apiResponse = $state(null);

  // Limpieza de memoria (Esencial al crear ObjectURLs)
  onDestroy(() => {
    if (fileUrl) {
      URL.revokeObjectURL(fileUrl);
    }
  });

  async function handleFile(file) {
    fileName = file.name; // Ahora no dará error
    fileUrl = URL.createObjectURL(file);
    status = "loading";
    uploadProgress = 0;

    // Iniciamos un pequeño contador visual para que la barra no esté quieta
    const progressInterval = setInterval(() => {
      if (uploadProgress < 90) {
        uploadProgress += 1; // Sube lentamente mientras la IA piensa
      }
    }, 200);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/process-invoice/", {
        method: "POST",
        body: formData,
      });

      // ¡NUEVO!: Si falla, leemos el mensaje exacto que manda FastAPI
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Error desconocido en el servidor");
      }

      apiResponse = await response.json();

      uploadProgress = 100;
      clearInterval(progressInterval);

      setTimeout(() => {
        status = "editing";
      }, 500);
    } catch (error) {
      clearInterval(progressInterval);

      // Ahora el alert nos dirá el motivo real (ej: "No API key found", "Validation Error", etc.)
      console.error("Detalle del error:", error);
      alert("Error del Backend: " + error.message);

      status = "idle";
    }
  }
</script>

<svelte:head>
  <title>NeuralLedger</title>
</svelte:head>

<div class="upload-page-container {status === 'editing' ? 'is-editing' : ''}">
  <div class="upload-content">
    <header class="text-center">
      <h1>Procesar <span>Nueva Factura</span></h1>
      <p>Análisis inteligente de documentos con IA</p>
    </header>

    <div class="content-wrapper">
      {#if status === "idle"}
        <div in:fade><Dropzone onFileSelect={handleFile} /></div>
      {:else if status === "loading"}
        <div in:fade>
          <LoadingBar progress={uploadProgress} />
          <p class="loading-text">
            La IA está analizando los conceptos del PDF...
          </p>
        </div>
      {:else if status === "editing"}
        <div class="full-width-editor" in:fly={{ y: 20, duration: 500 }}>
          <InvoiceEditor
            data={apiResponse}
            {fileUrl}
            onSave={(result) => {
              console.log("Guardado final:", result);
              status = "idle";
              apiResponse = null;
            }}
            onCancel={() => {
              status = "idle";
              fileUrl = "";
              apiResponse = null;
            }}
          />
        </div>
      {/if}
    </div>
  </div>
</div>

<style>
  .loading-text {
    text-align: center;
    margin-top: 1rem;
    color: var(--primary);
    font-weight: 600;
    font-size: 0.9rem;
    letter-spacing: 1px;
    text-transform: uppercase;
  }
  .upload-page-container {
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    transition: all 0.5s ease;
  }

  /* Cuando editamos, permitimos que el contenido sea más ancho */
  .upload-page-container.is-editing .upload-content {
    max-width: 1400px;
    padding-top: 2rem;
  }

  .upload-content {
    width: 100%;
    max-width: 800px; /* Ancho normal para dropzone */
    transition: max-width 0.5s ease;
  }

  header h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
  }
  header h1 span {
    color: var(--primary);
  }
  header p {
    color: var(--text-muted);
  }

  .content-wrapper {
    margin-top: 3rem;
    width: 100%;
  }
</style>
