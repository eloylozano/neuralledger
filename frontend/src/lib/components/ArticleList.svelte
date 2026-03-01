<script>
    // @ts-nocheck
    import { Tag, Trash2, Plus } from "lucide-svelte";
    import { fade } from "svelte/transition";
    import TableInput from "./TableInput.svelte";
  
    let { items = $bindable() } = $props();
  
    function removeItem(index) {
      items = items.filter((_, i) => i !== index);
    }
  
    function addItem() {
      const nextPos = items.length > 0 ? Math.max(...items.map((i) => i.position)) + 1 : 1;
      items = [...items, {
          position: nextPos,
          description: "",
          quantity: 1,
          price: 0,
          tax: 21,
          total_item: 0,
        }];
    }
  
    $effect(() => {
      items.forEach((item) => {
        const base = item.quantity * item.price;
        const total = base + base * (item.tax / 100);
        item.total_item = total.toFixed(2);
      });
    });
  </script>
  
  <div class="glass-card items-box">
    <div class="column-header">
      <div class="header-left">
        <Tag size={16} class="text-primary" />
        <span>Líneas de Detalle / Conceptos Extraídos</span>
      </div>
      <button class="add-btn" onclick={addItem}>
        <Plus size={14} /> Añadir Línea
      </button>
    </div>
  
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th width="50">#</th>
            <th>Descripción del Producto o Servicio</th>
            <th width="100">Cantidad</th>
            <th width="120">Precio Unit.</th>
            <th width="80">IVA %</th>
            <th width="120" class="text-right">Subtotal</th>
            <th width="50"></th>
          </tr>
        </thead>
        <tbody>
          {#each items as item, i (i)}
            <tr in:fade={{ duration: 200 }}>
              <td class="text-muted text-center font-mono pos-cell">{item.position}</td>
              <td><TableInput bind:value={item.description} /></td>
              <td><TableInput bind:value={item.quantity} type="number" align="right" /></td>
              <td><TableInput bind:value={item.price} type="number" align="right" /></td>
              <td><TableInput bind:value={item.tax} type="number" align="right" /></td>
              <td class="text-right subtotal-cell">
                <span class="subtotal-value">{item.total_item}€</span>
              </td>
              <td class="text-center">
                <button class="delete-btn" onclick={() => removeItem(i)} title="Eliminar">
                  <Trash2 size={14} />
                </button>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  </div>
  
  <style>
    .items-box {
      padding: 1.5rem;
      background: var(--glass-bg);
      backdrop-filter: blur(20px);
    }
  
    .column-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1.2rem;
    }
  
    .header-left {
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 0.75rem;
      font-weight: 800;
      color: var(--text-main); /* Cambiado a main para mejor contraste */
      text-transform: uppercase;
      letter-spacing: 1px;
    }
  
    .add-btn {
      display: flex;
      align-items: center;
      gap: 6px;
      background: color-mix(in srgb, var(--primary), transparent 90%);
      border: 1px solid color-mix(in srgb, var(--primary), transparent 60%);
      color: var(--primary);
      padding: 0.5rem 1rem;
      border-radius: 8px;
      font-size: 0.7rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.3s ease;
    }
  
    .add-btn:hover {
      background: var(--primary);
      color: white;
      box-shadow: 0 0 15px color-mix(in srgb, var(--primary), transparent 50%);
    }
  
    .table-container {
      border-radius: 12px;
      border: 1px solid var(--glass-border);
      /* Fondo que se adapta: oscuro en dark, muy levemente gris en light */
      background: color-mix(in srgb, var(--text-main), transparent 97%);
      overflow: hidden;
    }
  
    table {
      width: 100%;
      border-collapse: collapse;
    }
  
    th {
      /* Header con contraste */
      background: color-mix(in srgb, var(--bg-main), transparent 20%);
      backdrop-filter: blur(10px);
      font-size: 0.6rem;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.1em;
      padding: 1.2rem 1rem;
      border-bottom: 1px solid var(--glass-border);
      text-align: left;
    }
  
    td {
      padding: 0.4rem 1rem;
      border-bottom: 1px solid var(--glass-border);
      vertical-align: middle;
      color: var(--text-main);
    }
  
    tr:hover {
      background: color-mix(in srgb, var(--primary), transparent 96%);
    }
  

  
    .subtotal-value {
      font-weight: 800;
      font-size: 0.95rem;
      /* Efecto sutil de brillo solo si el fondo es oscuro */
      filter: drop-shadow(0 0 8px color-mix(in srgb, var(--primary), transparent 80%));
    }
  
    .pos-cell {
      font-size: 0.75rem;
      font-weight: 600;
    }
  
    .text-right { text-align: right; }
    .text-center { text-align: center; }
    
    .font-mono {
      font-family: "JetBrains Mono", ui-monospace, monospace;
    }
  
    .delete-btn {
      color: #f87171;
      opacity: 0.6;
      transition: all 0.2s;
      background: none;
      border: none;
      cursor: pointer;
    }
  
    .delete-btn:hover {
      opacity: 1;
      transform: scale(1.1);
      background: color-mix(in srgb, #f87171, transparent 90%);
      border-radius: 6px;
    }
  
    .text-primary { color: var(--primary); }
  </style>