<script lang="ts">
  import { onMount } from "svelte";
  import { Users, Search, RefreshCw } from "lucide-svelte";
  import SupplierCard from "$lib/components/SupplierCard.svelte";

  // Definición de la interfaz
  interface Supplier {
    id: number;
    name: string;
    cif: string;
    ia_notes: string;
    invoice_count: number;
    total_spent: number;
  }

  // Runes de Svelte 5
  let suppliers = $state<Supplier[]>([]);
  let loading = $state(true);
  let searchTerm = $state("");

  async function fetchSuppliers() {
    loading = true;
    try {
      const res = await fetch("http://localhost:8000/suppliers/");
      if (res.ok) {
        suppliers = await res.json();
      }
    } catch (e) {
      console.error("Error al conectar con el servidor:", e);
    } finally {
      loading = false;
    }
  }

  // --- FUNCIONES QUE FALTABAN ---

  // Se ejecuta cuando el hijo avisa que se actualizó un proveedor
  function handleUpdate(event) {
    const updated = event.detail;
    suppliers = suppliers.map((s) =>
      s.id === updated.id ? { ...s, ...updated } : s
    );
  }

  // Elimina de la lista local inmediatamente
  function handleDelete(event) {
    const id = event.detail.id;
    suppliers = suppliers.filter((s) => s.id !== id);
  }

  onMount(fetchSuppliers);

  // Derivado reactivo para el filtrado
  let filtered = $derived(
    suppliers.filter(
      (s) =>
        s.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        s.cif.toLowerCase().includes(searchTerm.toLowerCase())
    )
  );
</script>

<div class="page-container">
  <header class="page-header">
    <div class="header-main">
      <div class="title-section">
        <div class="icon-badge"><Users size={24} /></div>
        <div>
          <h1>Directorio de Entidades</h1>
          <p>{suppliers.length} proveedores registrados</p>
        </div>
      </div>

      <div class="controls">
        <div class="search-wrapper">
          <input
            type="text"
            bind:value={searchTerm}
            placeholder="Filtrar por nombre o CIF..."
          />
        </div>
        <button on:click={fetchSuppliers} class="btn-refresh" title="Refrescar">
          <RefreshCw size={18} class={loading ? "spinning" : ""} />
        </button>
      </div>
    </div>
  </header>

  {#if loading && suppliers.length === 0}
    <div class="loader-container">
      <div class="pulse-loader"></div>
    </div>
  {:else}
    <div class="suppliers-list">
      {#each filtered as s (s.id)}
        <SupplierCard
          supplier={s}
          on:update={handleUpdate}
          on:delete={handleDelete}
        />
      {/each}
    </div>

    {#if filtered.length === 0 && !loading}
      <div class="empty-state">
        <p>No se han encontrado resultados para "{searchTerm}"</p>
      </div>
    {/if}
  {/if}
</div>

<style>
  .page-container {
    padding: 2rem;
    max-width: 1400px;
    margin: 0 auto;
    /* Aseguramos que el contenedor base use el color de texto del tema */
    color: var(--text-main);
  }

  .header-main {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 2rem;
    margin-bottom: 3rem;
  }

  .title-section {
    display: flex;
    align-items: center;
    gap: 1.25rem;
  }

  .title-section h1 {
    color: var(--text-main);
    font-size: 1.875rem;
    font-weight: 800;
    margin: 0;
  }

  .title-section p {
    color: var(--text-muted);
    margin: 0.25rem 0 0 0;
  }

  .icon-badge {
    background: var(--primary);
    /* Color de icono oscuro para contraste sobre el primario brillante */
    color: #0f172a; 
    padding: 1rem;
    border-radius: 18px;
    box-shadow: 0 10px 20px -5px rgba(var(--primary-rgb, 0, 210, 255), 0.4);
  }

  .controls {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .search-wrapper {
    position: relative;
    width: 350px;
  }

  .search-wrapper input {
    width: 100%;
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    padding: 0.8rem 1rem;
    border-radius: 14px;
    /* CAMBIO: Texto dinámico */
    color: var(--text-main);
    transition: all 0.3s ease;
  }

  .search-wrapper input::placeholder {
    color: var(--text-muted);
    opacity: 0.7;
  }

  .search-wrapper input:focus {
    outline: none;
    border-color: var(--primary);
    background: rgba(255, 255, 255, 0.05);
  }

  .btn-refresh {
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    /* CAMBIO: Icono dinámico */
    color: var(--text-main);
    width: 46px;
    height: 46px;
    border-radius: 14px;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .btn-refresh:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: var(--primary);
    color: var(--primary);
  }

  .btn-refresh:active {
    transform: scale(0.95);
  }

  :global(.spinning) {
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }

  .suppliers-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
    gap: 1.5rem;
  }

  .loader-container {
    display: flex;
    justify-content: center;
    padding: 5rem;
  }

  .pulse-loader {
    width: 48px;
    height: 48px;
    border: 3px solid var(--primary);
    border-radius: 50%;
    animation: pulse 1.5s infinite;
  }

  @keyframes pulse {
    0% { transform: scale(0.8); opacity: 0.5; }
    50% { transform: scale(1.2); opacity: 0.2; }
    100% { transform: scale(0.8); opacity: 0.5; }
  }

  .empty-state {
    text-align: center;
    color: var(--text-muted);
    margin-top: 4rem;
    font-style: italic;
  }
</style>
