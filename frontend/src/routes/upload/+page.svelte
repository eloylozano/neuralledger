<script>
  import Dropzone from "$lib/components/Dropzone.svelte";
  import InvoiceEditor from "$lib/components/InvoiceEditor.svelte";
  import LoadingBar from "$lib/components/LoadingBar.svelte";
  import { fade, fly } from "svelte/transition";
  import { onDestroy } from "svelte"; // Importante para la memoria

  let status = $state("idle");
  let uploadProgress = $state(0);
  let fileName = $state("");
  let fileUrl = $state(""); // Aquí guardaremos la URL del PDF

  function handleFile(file) {
    fileName = file.name;

    // 1. CREAR LA URL DEL BLOB
    // Esto crea una dirección tipo "blob:http://localhost:5173/..."
    fileUrl = URL.createObjectURL(file);

    status = "loading";
    simulateUpload();
  }

  // Limpieza de memoria: cuando cambies de página, borramos la URL temporal
  onDestroy(() => {
    if (fileUrl) URL.revokeObjectURL(fileUrl);
  });
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
  let mockData = $state({
    supplier_name: "Amazon Web Services EMEA SARL",
    supplier_cif: "LU26375245",
    ia_notes:
      "CIF extraído de metadatos del pie de página. Advertencia: Se detectó una discrepancia de 0.01€ en el redondeo del IVA respecto al total calculado. Se recomienda revisar la posición 2.",
    date: "2024-02-15",
    invoice_num: "EU-1234567-2024",
    taxable_base: 120.5,
    vat: 25.31,
    total: 145.81,
    items: [
      {
        position: 1,
        description: "AWS Compute Service (EC2) - Region: Ireland",
        quantity: 1,
        price: 100.0,
        tax: 21.0,
        total_item: 121.0,
      },
      {
        position: 2,
        description: "Cloudwatch Logs Storage & Data Transfer",
        quantity: 1,
        price: 20.5,
        tax: 21.0,
        total_item: 24.81,
      },
    ],
  });
</script>

<svelte:head>
  <title>NeuralLedger | Subir Factura</title>
</svelte:head>
<div class="upload-page-container {status === 'editing' ? 'is-editing' : ''}">
  <div class="upload-content">
    <header class="text-center">
      <h1>Procesar <span>Nueva Factura</span></h1>
      <p>Análisis inteligente de documentos con DeepSeek IA</p>
    </header>

    <div class="content-wrapper">
      {#if status === "idle"}
        <div in:fade><Dropzone onFileSelect={handleFile} /></div>
      {:else if status === "loading"}
        <div in:fade><LoadingBar progress={uploadProgress} /></div>
      {:else if status === "editing"}
        <div class="full-width-editor" in:fly={{ y: 20, duration: 500 }}>
          <InvoiceEditor
            data={mockData}
            {fileUrl}
            onSave={(d) => console.log(d)}
            onCancel={() => {
              status = "idle";
              fileUrl = ""; // Limpiamos al cancelar
            }}
          />
        </div>
      {/if}
    </div>
  </div>
</div>

<style>
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
