<script lang="ts">
  import { theme, palettes } from "$lib/theme.svelte";

  function handleThemeChange(p) {
    theme.apply(p);
  }
</script>

<p>Selecciona una paleta de colores:</p>
<div class="palette-grid">
  {#each palettes as p}
    <button
      class="palette-option"
      class:active={theme.selected.name === p.name}
      onclick={() => handleThemeChange(p)}
    >
      <div
        class="preview-circle"
        style="background: linear-gradient(135deg, {p.primary}, {p.secondary})"
      ></div>
      <span>{p.name}</span>
    </button>
  {/each}
</div>

<style>
  p {
    color: var(--text-muted);
    font-size: 0.9rem;
    margin-bottom: 1rem;
  }

  .palette-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 1rem;
  }

  .palette-option {
    background: rgba(255, 255, 255, 0.05);
    border: 2px solid transparent;
    padding: 1rem;
    border-radius: 12px;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    transition: all 0.2s ease;
    color: var(--text-muted);
  }

  .palette-option:hover {
    background: rgba(255, 255, 255, 0.1);
    transform: translateY(-2px);
  }

  .palette-option.active {
    border-color: var(--primary);
    background: rgba(255, 255, 255, 0.1);
    color: var(--text-main);
  }

  .preview-circle {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  }
</style>
