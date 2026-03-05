<script lang="ts">
  import { onMount } from "svelte";
  import {
    RefreshCw,
    Eye,
    Search,
    ChevronUp,
    Pencil,
    Trash2,
    X,
  } from "lucide-svelte";
  import { fly } from "svelte/transition"; // Importante para la animación
  import PdfPreview from "$lib/components/PdfPreview.svelte";
  import InvoiceEditor from "$lib/components/InvoiceEditor.svelte";

  interface Invoice {
    id: number;
    invoice_num: string;
    date_str: string;
    date: string;
    taxable_base: number;
    vat: number;
    total: number;
    discount: number;
    pdf_path: string;
    supplier?: {
      name: string;
      cif: string;
    };
    items: any[];
  }

  let invoices = $state<Invoice[]>([]);
  let loading = $state(true);
  let error = $state<string | null>(null);
  let searchTerm = $state("");
  let expandedId = $state<number | null>(null);

  // ESTADO PARA EDICIÓN - Lo inicializamos como el objeto que espera InvoiceEditor
  let editingInvoice = $state<{ extracted: any; fileUrl: string } | null>(null);

  async function fetchInvoices() {
    loading = true;
    error = null;
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

  async function deleteInvoice(id: number, event: Event) {
    event.stopPropagation(); // Evita que se abra/cierre la preview al borrar
    if (!confirm("¿Estás seguro de que deseas eliminar esta factura?")) return;

    try {
      const res = await fetch(`http://localhost:8000/invoices/${id}`, {
        method: "DELETE",
      });
      if (res.ok) {
        invoices = invoices.filter((inv) => inv.id !== id);
      }
    } catch (e) {
      console.error(e);
    }
  }

  function startEdit(invoice: Invoice, event: Event) {
    event.stopPropagation();

    // Clonamos para evitar mutar la lista principal por error
    const invoiceCopy = JSON.parse(JSON.stringify(invoice));

    editingInvoice = {
      extracted: {
        id: invoiceCopy.id,
        supplier_name: invoiceCopy.supplier?.name || "",
        supplier_cif: invoiceCopy.supplier?.cif || "",
        invoice_num: invoiceCopy.invoice_num,
        date: invoiceCopy.date_str, // Asegúrate de usar el campo correcto
        taxable_base: invoiceCopy.taxable_base,
        vat: invoiceCopy.vat,
        discount: invoiceCopy.discount || 0,
        total: invoiceCopy.total,
        // SEGURIDAD: Si items viene null del back, pasamos un array vacío
        items: invoiceCopy.items || [],
        ia_notes: invoiceCopy.supplier?.ia_notes || "",
      },
      fileUrl: `http://localhost:8000/${invoiceCopy.pdf_path}`,
    };
  }

  function closeEditor() {
    editingInvoice = null;
  }

  onMount(fetchInvoices);

  let filteredInvoices = $derived(
    invoices.filter(
      (inv) =>
        inv.supplier?.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        inv.invoice_num?.toLowerCase().includes(searchTerm.toLowerCase())
    )
  );

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("es-ES", {
      style: "currency",
      currency: "EUR",
    }).format(value);
  };
</script>

<div class="main-content">
  {#if editingInvoice}
    <div class="editor-overlay" in:fly={{ y: 20 }}>
      <div class="editor-header">
        <button on:click={closeEditor} class="close-btn">
          <X size={18} /> <span>Volver al histórico</span>
        </button>
      </div>

      <InvoiceEditor
        bind:data={editingInvoice}
        fileUrl={editingInvoice.fileUrl}
        onSave={() => {
          editingInvoice = null;
          fetchInvoices();
        }}
        onCancel={closeEditor}
      />
    </div>
  {:else}
    <div
      class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8"
    >
      <div>
        <h1 class="text-3xl font-extrabold tracking-tight text-white">
          Histórico
        </h1>
        <p class="text-sm mt-1 text-[var(--text-muted)]">
          Gestiona tus facturas procesadas
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
            placeholder="Buscar proveedor o número..."
            class="search-input"
          />
        </div>
        <button on:click={fetchInvoices} class="refresh-btn">
          <RefreshCw class="w-5 h-5 {loading ? 'animate-spin' : ''}" />
        </button>
      </div>
    </div>

    {#if loading}
      <div class="flex justify-center py-20">
        <div class="loader"></div>
      </div>
    {:else}
      <div class="glass-card overflow-hidden">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="table-header">
              <th class="px-6 py-4">Fecha</th>
              <th class="px-6 py-4">Proveedor</th>
              <th class="px-6 py-4">Total</th>
              <th class="px-6 py-4 text-right">Acciones</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-[var(--glass-border)]">
            {#each filteredInvoices as invoice (invoice.id)}
              <tr class="table-row {expandedId === invoice.id ? 'active' : ''}">
                <td class="px-6 py-4 text-sm text-[var(--text-muted)]"
                  >{invoice.date_str}</td
                >
                <td class="px-6 py-4">
                  <div class="font-semibold text-[var(--text-main)]">
                    {invoice.supplier?.name || "Sin nombre"}
                  </div>
                  <div class="text-[10px] opacity-50 uppercase">
                    #{invoice.invoice_num}
                  </div>
                </td>
                <td class="px-6 py-4 font-bold text-[var(--text-muted)]"
                  >{formatCurrency(invoice.total)}</td
                >
                <td class="px-6 py-4">
                  <div class="flex justify-end gap-2">
                    <button
                      on:click={() =>
                        (expandedId =
                          expandedId === invoice.id ? null : invoice.id)}
                      class="action-btn"
                      title="Ver PDF"
                    >
                      <Eye size={16} />
                    </button>
                    <button
                      on:click={(e) => startEdit(invoice, e)}
                      class="action-btn edit"
                      title="Editar"
                    >
                      <Pencil size={16} />
                    </button>
                    <button
                      on:click={(e) => deleteInvoice(invoice.id, e)}
                      class="action-btn delete"
                      title="Eliminar"
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                </td>
              </tr>

              {#if expandedId === invoice.id}
                <tr in:fly={{ y: -10, duration: 200 }}>
                  <td colspan="4" class="p-0">
                    <div class="preview-container">
                      <PdfPreview
                        fileUrl={`http://localhost:8000/${invoice.pdf_path}`}
                      />
                    </div>
                  </td>
                </tr>
              {/if}
            {:else}
              <tr>
                <td
                  colspan="4"
                  class="px-6 py-20 text-center text-[var(--text-muted)]"
                  >No se han encontrado facturas.</td
                >
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {/if}
  {/if}
</div>

<style>
  /* ESTILOS DEL EDITOR */
  .editor-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    /* Usamos el fondo del tema en lugar de un azul oscuro fijo */
    background: var(--bg-main, #0b0f1a);
    z-index: 1000;
    overflow-y: auto;
    padding: 1.5rem;
  }

  .editor-header {
    max-width: 1400px;
    margin: 0 auto 1rem auto;
  }

  .close-btn {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0.6rem 1.2rem;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    /* CAMBIO AQUÍ */
    color: var(--text-main);
    cursor: pointer;
    font-weight: 600;
    transition: all 0.2s;
  }

  .close-btn:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: var(--primary);
    color: var(--primary); /* Feedback visual al hover */
  }

  /* BUSQUEDA */
  .search-input {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    padding: 0.6rem 1rem 0.6rem 2.5rem;
    font-size: 0.85rem;
    /* CAMBIO AQUÍ */
    color: var(--text-main);
    width: 280px;
    outline: none;
  }
  .search-input:focus {
    border-color: var(--primary);
  }

  /* TABLA */
  .table-header {
    background: rgba(255, 255, 255, 0.03);
    color: var(--text-muted);
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  .table-row {
    transition: all 0.2s;
    /* Aseguramos que el texto base de la fila siga el tema */
    color: var(--text-main);
  }

  .table-row.active {
    background: rgba(0, 210, 255, 0.08);
  }

  .preview-container {
    height: 600px;
    background: rgba(0, 0, 0, 0.4);
    margin: 1rem 1.5rem;
    border-radius: 12px;
    border: 1px solid var(--glass-border);
    overflow: hidden;
  }

  /* BOTONES ACCIÓN */
  .action-btn {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    /* CAMBIO AQUÍ */
    color: var(--text-main);
    cursor: pointer;
    transition: all 0.2s;
  }

  .action-btn:hover {
    background: var(--primary);
    color: #0f172a; /* Texto oscuro sobre fondo brillante siempre es mejor */
    transform: translateY(-2px);
  }

  .action-btn.edit:hover {
    background: #3b82f6;
    color: white;
  }

  .action-btn.delete:hover {
    background: #ef4444;
    color: white;
  }

  .refresh-btn {
    padding: 0.6rem;
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    /* CAMBIO AQUÍ */
    color: var(--text-main);
    cursor: pointer;
    transition: all 0.2s;
  }

  .refresh-btn:hover {
    border-color: var(--primary);
    color: var(--primary);
  }

  .loader {
    width: 40px;
    height: 40px;
    border: 3px solid var(--glass-border);
    border-top-color: var(--primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
</style>
