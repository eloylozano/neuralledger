<script>
  import {
    Building2,
    Tag,
    Calendar,
    Hash,
    Percent,
    TicketPercent,
  } from "lucide-svelte";
  import { fly, fade } from "svelte/transition";
  import NeuralInput from "./NeuralInput.svelte";

  let { data = $bindable() } = $props();

  let globalTax = $state(21);
  let subtotalBruto = $state(0);
  
  // Estado para el porcentaje (se sincroniza con los euros)
  let discountPercent = $state(0);

  // 1. Cuando cambian los ITEMS, calculamos el subtotal y el % inicial
  $effect(() => {
    if (data.items) {
      subtotalBruto = data.items.reduce(
        (acc, item) => acc + Number(item.quantity) * Number(item.price),
        0
      );
      
      // Si el backend ya mandó un descuento en €, calculamos su % inicial
      if (subtotalBruto > 0 && Number(data.discount) > 0 && discountPercent === 0) {
        discountPercent = ((Number(data.discount) / subtotalBruto) * 100).toFixed(1);
      }
    }
  });

  // 2. Lógica de vinculación: Si el usuario cambia el %, actualizamos los €
  function handlePercentChange(e) {
    const newPercent = Number(e.target.value);
    discountPercent = newPercent;
    data.discount = ((subtotalBruto * newPercent) / 100).toFixed(2);
  }

  // 3. Lógica de vinculación: Si el usuario cambia los €, actualizamos el %
  function handleEuroChange(e) {
    const newEuros = Number(e.target.value);
    data.discount = newEuros;
    if (subtotalBruto > 0) {
      discountPercent = ((newEuros / subtotalBruto) * 100).toFixed(1);
    }
  }

  // 4. Cálculo final de totales (se dispara cuando cambia data.discount o globalTax)
  $effect(() => {
    const discount = Number(data.discount) || 0;
    const taxableBase = subtotalBruto - discount;
    const totalVat = taxableBase * (Number(globalTax) / 100);

    data.taxable_base = taxableBase.toFixed(2);
    data.vat = totalVat.toFixed(2);
    data.total = (taxableBase + totalVat).toFixed(2);
  });
</script>

<div class="glass-card info-global">
  <div class="column-header">
    <span>Datos del Proveedor y Ajustes</span>
  </div>

  {#if data.ia_notes !== undefined}
    <div class="ia-alert" in:fly={{ y: -10 }}>
      <div class="ia-alert-header">
        <span>Entrenamiento Neural Ledger</span>
      </div>
      <textarea
        bind:value={data.ia_notes}
        class="ia-notes-editor"
        placeholder="Instrucciones..."
      ></textarea>
    </div>
  {/if}

  <div class="global-grid no-arrows">
    <NeuralInput label="Proveedor" icon={Building2} bind:value={data.supplier_name} />
    <NeuralInput label="CIF/NIF" icon={Tag} bind:value={data.supplier_cif} />

    <NeuralInput label="Nº Factura" icon={Hash} bind:value={data.invoice_num} />
    <NeuralInput label="Fecha" icon={Calendar} type="date" bind:value={data.date} />

    <NeuralInput label="IVA Global %" icon={Percent} type="number" bind:value={globalTax} />
    
    <div class="dual-discount">
      <div class="input-field">
        <label><TicketPercent size={12} /> Dto %</label>
        <div class="table-input-wrapper">
          <input 
            class="table-input" 
            type="number" 
            value={discountPercent} 
            oninput={handlePercentChange}
          />
          <div class="input-focus-line"></div>
        </div>
      </div>
      <div class="input-field">
        <label>€ Importe Descuento </label>
        <div class="table-input-wrapper">
          <input 
            class="table-input" 
            type="number" 
            value={data.discount} 
            oninput={handleEuroChange}
          />
          <div class="input-focus-line"></div>
        </div>
      </div>
    </div>
  </div>

  <div class="totals-summary">
    <div class="total-box">
      <span>Base Bruta</span>
      <p>{subtotalBruto.toFixed(2)}€</p>
    </div>
    <div class="total-box discount-highlight">
      <span>Descuento ({discountPercent}%)</span>
      <p>-{Number(data.discount || 0).toFixed(2)}€</p>
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
  }

  .global-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.25rem 1rem;
    margin-bottom: 1.5rem;
  }

  /* Estilo para los dos inputs de descuento en la misma celda */
  .dual-discount {
    display: grid;
    grid-template-columns: 0.8fr 1.2fr;
    gap: 8px;
    align-items: flex-end;
  }

  .input-field {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .input-field label {
    font-size: 0.65rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 4px;
  }

  .table-input-wrapper {
    position: relative;
    width: 100%;
  }

  .table-input {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid var(--glass-border);
    padding: 0.6rem;
    border-radius: 8px;
    color: #ffffff;
    width: 100%;
    font-size: 0.9rem;
    outline: none;
    transition: all 0.2s;
  }

  .table-input:focus {
    border-color: var(--primary);
    background: color-mix(in srgb, var(--primary), transparent 94%);
  }

  .input-focus-line {
    position: absolute;
    bottom: 0;
    left: 50%;
    width: 0;
    height: 1px;
    background: var(--primary);
    transition: all 0.3s;
    transform: translateX(-50%);
  }

  .table-input:focus + .input-focus-line {
    width: 80%;
  }

  /* Eliminar flechas */
  .no-arrows :global(input::-webkit-outer-spin-button),
  .no-arrows :global(input::-webkit-inner-spin-button) {
    -webkit-appearance: none;
    margin: 0;
  }
  .no-arrows :global(input[type="number"]) { -moz-appearance: textfield; }

  /* Totales */
  .totals-summary {
    display: grid;
    grid-template-columns: 1fr 1fr 1.2fr;
    gap: 1rem;
    margin-top: auto;
  }

  .total-box {
    background: var(--glass-bg);
    padding: 0.8rem;
    border-radius: 12px;
    border: 1px solid var(--glass-border);
    text-align: center;
  }

  .total-box span { font-size: 0.55rem; color: var(--text-muted); text-transform: uppercase; }
  .total-box p { font-size: 1.2rem; font-weight: 800; margin: 0; }

  .discount-highlight {
    border-color: rgba(248, 113, 113, 0.3);
    color: #f87171;
  }

  .total-box.primary {
    background: color-mix(in srgb, var(--primary), transparent 90%);
    border-color: var(--primary);
    color: var(--primary);
  }

  .column-header { display: flex; align-items: center; gap: 8px; margin-bottom: 1.25rem; font-size: 0.7rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; }
  .ia-alert { background: color-mix(in srgb, var(--primary), transparent 92%); border: 1px solid color-mix(in srgb, var(--primary), transparent 70%); padding: 0.8rem; border-radius: 12px; margin-bottom: 1.25rem; }
  .ia-alert-header { color: var(--primary); font-size: 0.65rem; font-weight: 800; text-transform: uppercase; margin-bottom: 4px; }
  .ia-notes-editor { width: 100%; background: transparent; border: none; color: var(--text-main); font-size: 0.85rem; resize: vertical; outline: none; }
</style>