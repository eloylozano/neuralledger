<script>
  let { value = $bindable(), type = "text", align = "left" } = $props();
</script>

<div class="table-input-wrapper">
  <input
    class="table-input"
    class:text-right={align === "right"}
    {type}
    bind:value
    spellcheck="false"
  />
  <div class="input-focus-line"></div>
</div>

<style>
  .table-input-wrapper {
    position: relative;
    width: 100%;
    display: flex;
    align-items: center;
    /* Aseguramos que el contenedor no corte el resplandor */
    overflow: visible; 
  }

  .table-input {
    background: transparent;
    border: 1px solid transparent;
    padding: 0.5rem 0.6rem;
    border-radius: 6px;
    color: var(--text-main); /* Asegúrate de que esto sea #ffffff */
    width: 100%;
    font-size: 0.85rem;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    outline: none;
    z-index: 2;
    position: relative;
  }

  /* ESTADO: HOVER */
  .table-input:hover {
    background: var(--glass-bg); /* rgba(255, 255, 255, 0.03) */
    border-color: var(--glass-border); /* rgba(255, 255, 255, 0.1) */
  }

  /* ESTADO: FOCUS (Cuando haces clic) */
  .table-input:focus {
    /* Usamos color-mix para crear un fondo sutil del color primario */
    background: color-mix(in srgb, var(--primary), transparent 92%);
    border-color: var(--primary);
    color: #ffffff;
  }

  /* La línea brillante inferior */
  .input-focus-line {
    position: absolute;
    bottom: 0;
    left: 50%;
    width: 0;
    height: 1px;
    background: var(--primary);
    box-shadow: 0 0 12px var(--primary);
    transition: all 0.3s ease;
    transform: translateX(-50%);
    pointer-events: none;
    z-index: 3;
  }

  /* Animación de la línea al enfocar */
  .table-input:focus + .input-focus-line {
    width: 90%;
  }

  .text-right {
    text-align: right;
  }

  /* Chrome, Safari, Edge, Opera: Quitar flechas de números */
  input::-webkit-outer-spin-button,
  input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }

  /* Firefox: Quitar flechas de números */
  input[type=number] {
    -moz-appearance: textfield;
  }

  /* Icono de fecha */
  input[type="date"]::-webkit-calendar-picker-indicator {
    filter: invert(1) brightness(0.8);
    opacity: 0.5;
    cursor: pointer;
  }
</style>