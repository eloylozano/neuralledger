<script lang="ts">
  import { onMount } from "svelte";
  import {
    Users,
    Search,
    RefreshCw,
    Edit3,
    Trash2,
    Save,
    X,
    BrainCircuit,
    ArrowUpRight,
    TrendingUp,
    Hash,
  } from "lucide-svelte";

  interface Supplier {
    id: number;
    name: string;
    cif: string;
    ia_notes: string;
    invoice_count: number;
    total_spent: number;
  }

  let suppliers: Supplier[] = [];
  let loading = true;
  let searchTerm = "";
  let editingId: number | null = null;
  let editForm = { name: "", cif: "", ia_notes: "" };

  async function fetchSuppliers() {
    loading = true;
    try {
      const res = await fetch("http://localhost:8000/suppliers/");
      if (res.ok) suppliers = await res.json();
    } catch (e) {
      console.error(e);
    } finally {
      loading = false;
    }
  }

  function startEdit(s: Supplier) {
    editingId = s.id;
    editForm = { name: s.name, cif: s.cif, ia_notes: s.ia_notes || "" };
  }

  onMount(fetchSuppliers);

  $: filtered = suppliers.filter(
    (s) =>
      s.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      s.cif.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const formatCurrency = (val: number) =>
    new Intl.NumberFormat("es-ES", {
      style: "currency",
      currency: "EUR",
    }).format(val);
</script>

<div class="page-container">
  <header class="page-header">
    <div class="header-main">
      <div class="title-section">
        <div class="icon-badge"><Users size={24} /></div>
        <div>
          <h1>Directorio de Entidades</h1>
          <p>{suppliers.length} proveedores registrados en el sistema</p>
        </div>
      </div>

      <div class="controls">
        <div class="search-wrapper">
          <Search size={18} class="search-icon" />
          <input
            bind:value={searchTerm}
            placeholder="Filtrar por nombre o identificación..."
          />
        </div>
        <button on:click={fetchInvoices} class="btn-refresh"
          ><RefreshCw size={18} /></button
        >
      </div>
    </div>
  </header>

  {#if loading}
    <div class="loader-container">
      <div class="pulse-loader"></div>
    </div>
  {:else}
    <div class="suppliers-list">
      {#each filtered as s (s.id)}
        <div class="card {editingId === s.id ? 'is-editing' : ''}">
          <div class="card-header">
            <div class="identity">
              {#if editingId === s.id}
                <input bind:value={editForm.name} class="input-inline name" />
                <input bind:value={editForm.cif} class="input-inline cif" />
              {:else}
                <h3 class="name">{s.name}</h3>
                <span class="cif"><Hash size={12} /> {s.cif}</span>
              {/if}
            </div>

            <div class="actions">
              {#if editingId === s.id}
                <button
                  class="action-icon save "
                  on:click={() => (editingId = null)}><Save size={18} /></button
                >
                <button
                  class="action-icon cancel"
                  on:click={() => (editingId = null)}><X size={18} /></button
                >
              {:else}
                <button class="action-icon edit" on:click={() => startEdit(s)}
                  ><Edit3 size={18} /></button
                >
                <button class="action-icon delete"><Trash2 size={18} /></button>
              {/if}
            </div>
          </div>

          <div class="card-metrics">
            <div class="metric">
              <span class="label">Operaciones</span>
              <span class="value"
                >{s.invoice_count} <small>facturas</small></span
              >
            </div>
            <div class="metric highlight">
              <span class="label">Volumen Total</span>
              <span class="value">{formatCurrency(s.total_spent)}</span>
            </div>
          </div>

          <div class="card-intelligence">
            <div class="intelligence-header">
              <BrainCircuit size={14} />
              <span>Memoria Neural</span>
            </div>
            {#if editingId === s.id}
              <textarea bind:value={editForm.ia_notes} class="textarea-inline"
              ></textarea>
            {:else}
              <p class="notes">
                {s.ia_notes ||
                  "Sin instrucciones de procesamiento específicas."}
              </p>
            {/if}
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .page-container {
    padding: 2rem;
    max-width: 1400px;
    margin: 0 auto;
  }

  /* Header Styles */
  .page-header {
    margin-bottom: 3rem;
  }

  .header-main {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    gap: 2rem;
  }

  .title-section {
    display: flex;
    align-items: center;
    gap: 1.25rem;
  }

  .icon-badge {
    background: var(--primary);
    color: #000;
    padding: 1rem;
    border-radius: 18px;
    box-shadow: 0 10px 20px -5px var(--primary);
  }

  .title-section h1 {
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.02em;
  }

  .title-section p {
    color: var(--text-muted);
    font-size: 0.95rem;
  }

  .controls {
    display: flex;
    gap: 1rem;
  }

  .search-wrapper {
    position: relative;
    width: 400px;
  }

  .search-icon {
    position: absolute;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    opacity: 0.4;
  }

  .search-wrapper input {
    width: 100%;
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    padding: 0.8rem 1rem 0.8rem 3rem;
    border-radius: 14px;
    color: white;
    transition: all 0.2s;
  }

  .search-wrapper input:focus {
    border-color: var(--primary);
    background: rgba(255, 255, 255, 0.06);
    outline: none;
  }

  /* Grid Layout */
  .suppliers-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
    gap: 1.5rem;
  }

  /* Card Design */
  .card {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 24px;
    padding: 1.75rem;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
  }

  .card:hover {
    transform: translateY(-4px);
    border-color: rgba(255, 255, 255, 0.2);
    box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.5);
  }

  .card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: var(--primary);
    opacity: 0.3;
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
  }

  .name {
    font-size: 1.35rem;
    font-weight: 700;
    color: #fff;
  }
  .cif {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.8rem;
    color: var(--text-muted);
    font-family: monospace;
    margin-top: 0.2rem;
  }

  /* Metrics Section */
  .card-metrics {
    display: grid;
    grid-template-columns: 1fr 1fr;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 16px;
    padding: 1rem;
  }

  .metric {
    display: flex;
    flex-direction: column;
  }
  .metric .label {
    font-size: 0.65rem;
    text-transform: uppercase;
    color: var(--text-muted);
    letter-spacing: 0.05em;
  }
  .metric .value {
    font-size: 1.1rem;
    font-weight: 700;
  }
  .metric.highlight .value {
    color: var(--primary);
  }

  /* Intelligence Section */
  .card-intelligence {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 1rem;
  }

  .intelligence-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--primary);
    font-size: 0.7rem;
    font-weight: 800;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
  }

  .notes {
    font-size: 0.85rem;
    line-height: 1.6;
    color: var(--text-muted);
    font-style: italic;
  }

  /* Buttons */
  .actions {
    display: flex;
    gap: 0.5rem;
  }
  .action-icon {
    padding: 0.6rem;
    cursor: pointer;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.05);
    color: var(--text-muted);
    transition: all 0.2s;
  }

  .action-icon:hover {
    background: rgba(255, 255, 255, 0.1);
    color: #fff;
  }
  .action-icon.save {
    color: #10b981;
  }
  .action-icon.delete:hover {
    color: #ef4444;
  }

  /* Edición */
  .input-inline {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid var(--primary);
    border-radius: 8px;
    color: white;
    padding: 0.4rem;
    width: 100%;
  }

  .textarea-inline {
    width: 100%;
    background: transparent;
    border: 1px solid var(--primary);
    color: white;
    font-size: 0.85rem;
    min-height: 80px;
    border-radius: 8px;
    padding: 0.5rem;
  }

  /* Loader */
  .pulse-loader {
    width: 48px;
    height: 48px;
    border: 3px solid var(--primary);
    border-radius: 50%;
    animation: pulse 1.5s infinite;
    margin: 4rem auto;
  }

  @keyframes pulse {
    0% {
      transform: scale(0.8);
      opacity: 0.5;
    }
    50% {
      transform: scale(1.2);
      opacity: 0.2;
    }
    100% {
      transform: scale(0.8);
      opacity: 0.5;
    }
  }
</style>
