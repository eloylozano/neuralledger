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
    <div class="identity" style="flex: 1; margin-right: 1rem;">
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
    color: var(--text-main);
  }

  .card:hover {
    transform: translateY(-4px);
    border-color: rgba(var(--primary-rgb, 0, 210, 255), 0.4);
  }

  /* Indicador lateral de color primario */
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

  .card.is-editing {
    border-color: var(--primary);
    background: rgba(var(--primary-rgb, 0, 210, 255), 0.05);
    box-shadow: 0 0 20px rgba(var(--primary-rgb, 0, 210, 255), 0.15);
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 1.5rem; /* Espacio de seguridad entre texto/input y botones */
  }

  .identity {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    flex: 1;
    min-width: 0; /* Permite que el texto trunque si es necesario */
  }

  .name {
    font-size: 1.35rem;
    font-weight: 700;
    color: var(--text-main);
    margin: 0;
  }

  .cif {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.8rem;
    color: var(--text-muted);
    font-family: monospace;
  }

  /* CONTROLES DE EDICIÓN */
  .input-inline {
    background: var(--glass-bg);
    border: 1px solid var(--primary);
    border-radius: 10px;
    color: var(--text-main);
    padding: 0.6rem 0.8rem;
    width: 100%;
    outline: none;
    box-sizing: border-box;
    transition: box-shadow 0.2s;
  }

  .input-inline:focus {
    box-shadow: 0 0 0 2px rgba(var(--primary-rgb, 0, 210, 255), 0.2);
  }

  .input-inline.name {
    font-size: 1.35rem;
    font-weight: 700;
  }

  .textarea-inline {
    width: 100%;
    background: var(--glass-bg);
    border: 1px solid var(--primary);
    color: var(--text-main);
    font-size: 0.85rem;
    min-height: 80px;
    border-radius: 12px;
    padding: 0.8rem;
    outline: none;
    font-family: inherit;
    resize: vertical;
    box-sizing: border-box;
  }

  .input-inline::placeholder,
  .textarea-inline::placeholder {
    color: var(--text-muted);
    opacity: 0.5;
  }

  /* BOTONES DE ACCIÓN */
  .actions {
    display: flex;
    gap: 0.75rem; /* Separación entre botones para que no se peguen */
    flex-shrink: 0;
    padding-top: 0.25rem;
  }

  .action-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0.7rem;
    cursor: pointer;
    border-radius: 12px;
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    color: var(--text-muted);
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .action-icon:hover {
    background: rgba(255, 255, 255, 0.1);
    color: var(--text-main);
    transform: translateY(-2px);
  }

  .action-icon.save {
    color: #10b981;
    background: rgba(16, 185, 129, 0.1);
    border-color: rgba(16, 185, 129, 0.2);
  }

  .action-icon.save:hover {
    background: #10b981;
    color: white;
    border-color: #10b981;
  }

  .action-icon.cancel {
    color: #ef4444;
    background: rgba(239, 68, 68, 0.1);
    border-color: rgba(239, 68, 68, 0.2);
  }

  .action-icon.cancel:hover {
    background: #ef4444;
    color: white;
    border-color: #ef4444;
  }

  .action-icon.delete:hover {
    background: #ef4444;
    color: white;
  }

  /* MÉTRICAS E INTELIGENCIA */
  .card-metrics {
    display: grid;
    grid-template-columns: 1fr 1fr;
    background: rgba(0, 0, 0, 0.15);
    border-radius: 16px;
    padding: 1.2rem;
    gap: 1rem;
  }

  .metric .label {
    font-size: 0.65rem;
    text-transform: uppercase;
    color: var(--text-muted);
    letter-spacing: 0.5px;
  }

  .metric .value {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-main);
  }

  .card-intelligence {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    padding: 1.2rem;
  }

  .intelligence-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--primary);
    font-size: 0.7rem;
    font-weight: 800;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
  }

  .notes {
    font-size: 0.85rem;
    line-height: 1.6;
    color: var(--text-muted);
    font-style: italic;
    margin: 0;
  }
</style>
