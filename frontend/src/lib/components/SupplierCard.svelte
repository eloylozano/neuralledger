<script lang="ts">
  import { Edit3, Trash2, Save, X, BrainCircuit, Hash } from "lucide-svelte";
  import { createEventDispatcher } from "svelte";

  export let supplier: any;
  const dispatch = createEventDispatcher();

  let editing = false;
  let editForm = { name: "", cif: "", ia_notes: "" };

  function startEdit() {
    editForm = {
      name: supplier.name,
      cif: supplier.cif,
      ia_notes: supplier.ia_notes || "",
    };
    editing = true;
  }

  // --- FUNCIÓN DE ACTUALIZAR ---
  async function saveEdit() {
    try {
      const res = await fetch(
        `http://localhost:8000/suppliers/${supplier.id}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            name: editForm.name,
            cif: editForm.cif.toUpperCase().trim(),
            ia_notes: editForm.ia_notes,
          }),
        }
      );

      if (res.ok) {
        const updated = await res.json();
        dispatch("update", updated); // Avisa al padre para refrescar la UI
        editing = false;
      } else {
        const errorData = await res.json();
        alert(`Error: ${errorData.detail || "No se pudo actualizar"}`);
      }
    } catch (e) {
      console.error("Error en PUT:", e);
      alert("Error de conexión al actualizar");
    }
  }

  // --- FUNCIÓN DE BORRAR ---
  async function handleDelete() {
    const confirmed = confirm(
      `¿Estás seguro de eliminar a "${supplier.name}"?`
    );
    if (!confirmed) return;

    try {
      const res = await fetch(
        `http://localhost:8000/suppliers/${supplier.id}`,
        {
          method: "DELETE",
        }
      );

      if (res.ok) {
        // IMPORTANTE: Avisamos al padre PRIMERO.
        // Si el servidor devolvió 200-299, el borrado es real.
        dispatch("delete", { id: supplier.id });
      } else {
        // Solo intentamos leer el error si la respuesta no es OK
        const errorData = await res.json();
        alert(`⚠️ ${errorData.detail || "Error al eliminar"}`);
      }
    } catch (e) {
      // Si el registro desaparece al refrescar, es que el servidor SÍ lo borró
      // pero hubo un hipo en la conexión de respuesta.
      console.error("Error en red:", e);
      // Opcional: podrías disparar el delete aquí también si confías en tu backend
      // dispatch("delete", { id: supplier.id });
    }
  }

  const formatCurrency = (val: number) =>
    new Intl.NumberFormat("es-ES", {
      style: "currency",
      currency: "EUR",
    }).format(val);
</script>

<div class="card {editing ? 'is-editing' : ''}">
  <div class="card-header">
    <div class="identity">
      {#if editing}
        <input
          bind:value={editForm.name}
          class="input-inline name"
          placeholder="Nombre"
        />
        <input
          bind:value={editForm.cif}
          class="input-inline cif"
          placeholder="CIF"
        />
      {:else}
        <h3 class="name">{supplier.name}</h3>
        <span class="cif"><Hash size={12} /> {supplier.cif}</span>
      {/if}
    </div>

    <div class="actions">
      {#if editing}
        <button
          class="action-icon save"
          on:click|stopPropagation={saveEdit}
          title="Guardar"
        >
          <Save size={18} />
        </button>
        <button
          class="action-icon cancel"
          on:click|stopPropagation={() => (editing = false)}
          title="Cancelar"
        >
          <X size={18} />
        </button>
      {:else}
        <button
          class="action-icon edit"
          on:click|stopPropagation={startEdit}
          title="Editar"
        >
          <Edit3 size={18} />
        </button>
        <button
          class="action-icon delete"
          on:click|stopPropagation={handleDelete}
          title="Eliminar"
        >
          <Trash2 size={18} />
        </button>
      {/if}
    </div>
  </div>

  <div class="card-metrics">
    <div class="metric">
      <span class="label">Operaciones</span>
      <span class="value">{supplier.invoice_count} <small>facturas</small></span
      >
    </div>
    <div class="metric highlight">
      <span class="label">Volumen Total</span>
      <span class="value">{formatCurrency(supplier.total_spent)}</span>
    </div>
  </div>

  <div class="card-intelligence">
    <div class="intelligence-header">
      <BrainCircuit size={14} />
      <span>Memoria Neural</span>
    </div>
    {#if editing}
      <textarea bind:value={editForm.ia_notes} class="textarea-inline"
      ></textarea>
    {:else}
      <p class="notes">
        {supplier.ia_notes || "Sin instrucciones específicas."}
      </p>
    {/if}
  </div>
</div>

<style>
  /* Tus estilos se mantienen iguales... */
  .card.is-editing {
    color: var(--text-main);
    border-color: var(--primary);
    background: rgba(var(--primary-rgb), 0.05);
  }
  /* Copia aquí los estilos específicos de la .card que tenías en +page.svelte */
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
    color: var(--text-main);
  }
  .cif {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.8rem;
    color: var(--text-muted);
    font-family: monospace;
  }
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
  }
  .metric .value {
    font-size: 1.1rem;
    font-weight: 700;
  }
  .metric.highlight .value {
    color: var(--primary);
  }
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
    border: none;
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
</style>
