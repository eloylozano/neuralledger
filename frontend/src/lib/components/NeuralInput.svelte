<script>
  /** * @typedef {Object} Props
   * @property {any} value - Bindable value
   * @property {string} label - Text for the label
   * @property {import('lucide-svelte').Icon} [icon] - Lucide icon component
   * @property {string} [type] - Input type (text, date, number...)
   * @property {string} [placeholder] - Input placeholder
   * @property {boolean} [isFull] - If true, takes 2 columns in the grid
   */
  let {
    value = $bindable(),
    label,
    icon: Icon,
    type = "text",
    placeholder = "",
    isFull = false,
  } = $props();
</script>

<div class="neural-field" class:is-full={isFull}>
  <label>
    {#if Icon}
      <div class="icon-wrapper">
        <Icon size={13} strokeWidth={2.5} />
      </div>
    {/if}
    <span>{label}</span>
  </label>

  <div class="input-wrapper">
    <input
      {type}
      bind:value
      {placeholder}
      spellcheck="false"
      autocomplete="off"
    />
    <div class="focus-glow"></div>
  </div>
</div>

<style>
  .neural-field {
    display: flex;
    flex-direction: column;
    gap: 6px;
    width: 100%;
  }

  /* Importante: esto asegura que el componente respete el grid del padre */
  .neural-field.is-full {
    grid-column: span 2;
  }

  label {
    display: flex;
    align-items: center;
    gap: 8px;
    padding-left: 2px;
  }

  label span {
    font-size: 0.65rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.8px;
  }

  .icon-wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--primary);
    opacity: 0.8;
  }

  .input-wrapper {
    position: relative;
    width: 100%;
    border-radius: 10px;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  input {
    width: 100%;
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    color: var(--text-main);
    padding: 0.75rem 1rem;
    border-radius: 10px;
    font-size: 0.9rem;
    font-family: inherit;
    transition: all 0.2s ease;
    outline: none;
    position: relative;
    z-index: 2;
  }

  /* Efecto Hover */
  input:hover {
    background: rgba(255, 255, 255, 0.06);
    border-color: rgba(255, 255, 255, 0.2);
  }

  /* Efecto Focus con Glow */
  input:focus {
    border-color: var(--primary);
    background: color-mix(in srgb, var(--primary), transparent 96%);
  }

  /* El resplandor azul sutil al enfocar */
  .focus-glow {
    /* Gradiente dinámico basado en la paleta */
    background: radial-gradient(
      circle at center,
      var(--primary) 0%,
      transparent 70%
    );
    opacity: 0;
    filter: blur(15px);
    transition: opacity 0.3s ease;
    position: absolute;
    inset: 0;
    pointer-events: none;
  }

  input:focus + .focus-glow {
    opacity: 0.15;
  }

  input::placeholder {
    color: rgba(255, 255, 255, 0.15);
    font-weight: 400;
  }

  /* Ajustes para el input de fecha */
  input[type="date"] {
    min-height: 43px;
  }

  input[type="date"]::-webkit-calendar-picker-indicator {
    filter: invert(0.8) sepia(100%) saturate(1000%) hue-rotate(170deg); /* Color primario */
    opacity: 0.6;
    cursor: pointer;
    transform: scale(1.1);
  }

  /* Estilo para navegadores Firefox */
  input[type="date"]::-moz-calendar-picker-indicator {
    filter: invert(1);
  }
</style>
