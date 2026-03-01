<script>
  import { Building2, Tag, Calendar, Hash, Sparkles } from "lucide-svelte";
  import { fly } from "svelte/transition";
  import NeuralInput from "./NeuralInput.svelte"; // Importamos el nuevo componente

  let { data = $bindable() } = $props();
</script>

<div class="glass-card info-global">
  <div class="column-header">
    <span>Datos del Proveedor</span>
  </div>

  {#if data.ia_notes}
    <div class="ia-alert" in:fly={{ y: -10 }}>
      <div class="ia-alert-header">
        <span>Auditoría Neural Ledger</span>
      </div>
      <p>{data.ia_notes}</p>
    </div>
  {/if}

  <div class="global-grid">
    <NeuralInput
      label="Proveedor / Emisor"
      icon={Building2}
      bind:value={data.supplier_name}
      placeholder="Nombre de la empresa"
      isFull={true}
    />

    <NeuralInput
      label="CIF/NIF"
      icon={Tag}
      bind:value={data.supplier_cif}
      placeholder="ESA12345678"
    />

    <NeuralInput
      label="Fecha de Factura"
      icon={Calendar}
      type="date"
      bind:value={data.date}
    />

    <NeuralInput
      label="Nº Factura"
      icon={Hash}
      bind:value={data.invoice_num}
      placeholder="FAC-0000"
      isFull={true}
    />
  </div>

  <div class="totals-summary">
    <div class="total-box">
      <span>Base Imponible</span>
      <p>{data.taxable_base}€</p>
    </div>
    <div class="total-box primary">
      <span>Total Factura</span>
      <p>{data.total}€</p>
    </div>
  </div>
</div>

<style>
  .info-global {
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    height: 100%;
    box-sizing: border-box;
  }

  .column-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 1.25rem;
    font-size: 0.7rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
  }
  .ia-alert {
    background: color-mix(in srgb, var(--primary), transparent 92%);
    border: 1px solid color-mix(in srgb, var(--primary), transparent 70%);
    padding: 0.8rem;
    border-radius: 12px;
    margin-bottom: 1.25rem;
  }

  .ia-alert-header {
    color: var(--primary);
    font-size: 0.65rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 4px;
  }
  .ia-alert p {
    font-size: 0.85rem;
    color: var(--text-main);
    line-height: 1.4;
  }

  .global-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-bottom: 1.5rem;
  }

  .totals-summary {
    display: grid;
    grid-template-columns: 1fr 1.2fr;
    gap: 1rem;
    margin-top: auto;
  }

  .total-box {
    background: var(--glass-bg);
    padding: 1rem;
    border-radius: 16px;
    border: 1px solid var(--glass-border);
    text-align: center;
    transition: all 0.3s ease;
  }

  .total-box.primary {
    border-color: color-mix(in srgb, var(--primary), transparent 50%);
    background: color-mix(in srgb, var(--primary), transparent 90%);
  }

  .total-box.primary p {
    color: var(--primary);
    text-shadow: 0 0 15px color-mix(in srgb, var(--primary), transparent 60%);
  }
  .total-box span {
    font-size: 0.6rem;
    color: var(--text-muted);
    text-transform: uppercase;
    display: block;
  }

  .total-box p {
    font-size: 1.4rem;
    font-weight: 800;
    margin: 0;
  }
</style>
