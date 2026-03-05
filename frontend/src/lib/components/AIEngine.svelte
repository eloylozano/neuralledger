<script lang="ts">
  let { threshold = $bindable() } = $props(); // Usamos bindable para sincronizar con el padre
</script>

<div class="input-group">
  <label for="model">Modelo Activo</label>
  <select id="model">
    <option>Llama 3.1 (Recomendado)</option>
    <option>Mistral</option>
    <option>Phi-3 (Ligero)</option>
  </select>
</div>
<div class="input-group">
  <label for="threshold">Umbral de Alerta Crítica (€)</label>
  <input type="number" id="threshold" bind:value={threshold} />
</div>

<style>
  .input-group {
    margin-bottom: 1.2rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  label {
    font-size: 0.9rem;
    color: var(--text-muted);
  }

  select,
  input {
    background: rgba(0, 0, 0, 0.2);
    border: 1px solid var(--glass-border);
    padding: 0.7rem;
    border-radius: 8px;
    color: var(--text-main);
    outline: none;
    transition: border-color 0.2s;
  }

  select:focus,
  input:focus {
    border-color: var(--primary);
  }
</style>
