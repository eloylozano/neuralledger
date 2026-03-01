<script lang="ts">
  import { onMount } from "svelte";
  import {
    FileText,
    RefreshCw,
    Eye,
    Search,
    Calendar,
    ChevronUp,
  } from "lucide-svelte";
  import PdfPreview from "$lib/components/PdfPreview.svelte";

  // Definición de interfaz para evitar fallos de tipado
  interface Invoice {
    id: number;
    invoice_num: string;
    date_str: string;
    total: number;
    pdf_path: string;
    supplier?: {
      name: string;
      cif: string;
    };
  }

  let invoices: Invoice[] = [];
  let loading = true;
  let error: string | null = null;
  let searchTerm = "";
  let expandedId: number | null = null;

  async function fetchInvoices() {
    loading = true;
    try {
      const response = await fetch("http://localhost:8000/invoices/");
      if (!response.ok) throw new Error("No se pudieron cargar las facturas");
      invoices = await response.json();
    } catch (e: any) {
      error = e.message;
    } finally {
      loading = false;
    }
  }

  function toggleExpand(id: number) {
    expandedId = expandedId === id ? null : id;
  }

  onMount(fetchInvoices);

  // Filtrado reactivo
  $: filteredInvoices = invoices.filter(
    (inv) =>
      inv.supplier?.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      inv.invoice_num.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("es-ES", {
      style: "currency",
      currency: "EUR",
    }).format(value);
  };
</script>

<div class="main-content">
  <div
    class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8"
  >
    <div>
      <h1 class="text-3xl font-extrabold tracking-tight">Histórico</h1>
      <p class="text-sm mt-1 text-[var(--text-muted)]">
        Consulta y previsualiza tus facturas
      </p>
    </div>

    <div class="flex items-center gap-3">
      <div class="relative">
        <Search
          class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[var(--text-muted)]"
        />
        <input
          type="text"
          bind:value={searchTerm}
          placeholder="Buscar proveedor..."
          class="bg-[var(--glass-bg)] border border-[var(--glass-border)] rounded-xl py-2 pl-10 pr-4 text-sm focus:outline-none focus:ring-2 focus:ring-[var(--primary)] transition-all w-64 text-white"
        />
      </div>
      <button
        on:click={fetchInvoices}
        class="p-2.5 bg-[var(--glass-bg)] border border-[var(--glass-border)] rounded-xl hover:bg-[rgba(255,255,255,0.1)] transition-all"
      >
        <RefreshCw class="w-5 h-5" />
      </button>
    </div>
  </div>

  {#if loading}
    <div class="flex flex-col items-center justify-center h-64">
      <div
        class="w-12 h-12 border-4 border-t-transparent border-[var(--primary)] rounded-full animate-spin mb-4"
      ></div>
      <p class="text-white">Cargando histórico...</p>
    </div>
  {:else if error}
    <div class="glass-card p-6 border-red-500/50 text-center text-red-400">
      {error}
    </div>
  {:else}
    <div class="glass-card overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr
              class="border-b border-[var(--glass-border)] bg-[rgba(255,255,255,0.02)] text-[var(--text-muted)]"
            >
              <th class="px-6 py-4 text-xs font-bold uppercase tracking-wider"
                >Fecha</th
              >
              <th class="px-6 py-4 text-xs font-bold uppercase tracking-wider"
                >Proveedor</th
              >
              <th class="px-6 py-4 text-xs font-bold uppercase tracking-wider"
                >Nº Factura</th
              >
              <th class="px-6 py-4 text-xs font-bold uppercase tracking-wider"
                >Total</th
              >
              <th
                class="px-6 py-4 text-right text-xs font-bold uppercase tracking-wider"
                >Acciones</th
              >
            </tr>
          </thead>
          <tbody class="divide-y divide-[var(--glass-border)]">
            {#each filteredInvoices as invoice (invoice.id)}
              <tr
                class="hover:bg-[rgba(255,255,255,0.03)] transition-colors {expandedId ===
                invoice.id
                  ? 'bg-[rgba(0,210,255,0.05)]'
                  : ''}"
              >
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm text-[var(--text-muted)]"
                  >{invoice.date_str}</td
                >
                <td class="px-6 py-4">
                  <div class="font-semibold text-white">
                    {invoice.supplier?.name || "Desconocido"}
                  </div>
                  <div class="text-[10px] opacity-50 uppercase tracking-widest">
                    {invoice.supplier?.cif || ""}
                  </div>
                </td>
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm font-mono text-[var(--text-muted)]"
                  >#{invoice.invoice_num}</td
                >
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="font-bold text-[var(--primary)]"
                    >{formatCurrency(invoice.total)}</span
                  >
                </td>
                <td class="px-6 py-4 text-right">
                  <button
                    on:click={() => toggleExpand(invoice.id)}
                    class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-[var(--glass-bg)] cursor-pointer border border-[var(--glass-border)] text-white font-bold text-xs hover:bg-[var(--primary)] hover:text-[#0f172a] transition-all"
                  >
                    {#if expandedId === invoice.id}
                      <ChevronUp class="w-4 h-4" /> CERRAR
                    {:else}
                      <Eye class="w-4 h-4" /> VER PDF
                    {/if}
                  </button>
                </td>
              </tr>

              {#if expandedId === invoice.id}
                <tr>
                  <td
                    colspan="5"
                    class="px-0 py-4 bg-[rgba(0,0,0,0.2)] "
                  >
                    <div
                      class="mx-6  overflow-hidden  border-[var(--glass-border)] shadow-2xl animate-in"
                    >
                      <div class="h-350 w-full">
                        <PdfPreview
                          fileUrl={`http://localhost:8000/${invoice.pdf_path}`}
                        />
                      </div>
                    </div>
                  </td>
                </tr>
              {/if}
            {/each}
          </tbody>
        </table>
      </div>
    </div>
  {/if}
</div>

<style>
  .animate-in {
    animation: slide-in 0.3s ease-out forwards;
  }
  @keyframes slide-in {
    from {
      transform: translateY(-10px);
      opacity: 0;
    }
    to {
      transform: translateY(0);
      opacity: 1;
    }
  }
</style>
