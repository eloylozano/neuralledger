<script lang="ts">
  import { Coins, Info } from "lucide-svelte";
  import NeuralInput from "./NeuralInput.svelte";

  let { threshold = $bindable() } = $props();
</script>

<div class="engine-container">
  <div class="threshold-section">
    <div class="header-with-info">
      <NeuralInput
        label="Umbral de Alerta Crítica"
        type="number"
        bind:value={threshold}
        icon={Coins}
        placeholder="Ej: 1000"
      />

      <div class="info-container">
        <Info size={14} class="info-icon" />
        <div class="tooltip">
          Las facturas que superen este importe se marcarán automáticamente como
          "Críticas" en el panel principal.
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  .engine-container {
    display: flex;
    flex-direction: column;
    padding: 0.5rem 0;
  }

  .header-with-info {
    position: relative;
    width: 100%;
  }

  .info-container {
    position: absolute;
    top: 2px;
    right: 0;
    cursor: help;
  }

  .info-icon {
    color: var(--text-muted);
    transition: color 0.2s;
  }

  .info-icon:hover {
    color: var(--primary);
  }

  .tooltip {
    visibility: hidden;
    position: absolute;
    bottom: 130%;
    right: 0;
    width: 220px;
    background: #0f172a;
    border: 1px solid var(--glass-border);
    color: white;
    padding: 0.8rem;
    border-radius: 8px;
    font-size: 0.75rem;
    line-height: 1.4;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
    z-index: 100;
    opacity: 0;
    transition: all 0.3s ease;
    transform: translateY(10px);
    pointer-events: none;
  }

  .info-container:hover .tooltip {
    visibility: visible;
    opacity: 1;
    transform: translateY(0);
  }

  /* Limpieza de flechas para el input numérico */
  :global(input[type="number"]::-webkit-outer-spin-button),
  :global(input[type="number"]::-webkit-inner-spin-button) {
    -webkit-appearance: none;
    margin: 0;
  }
  :global(input[type="number"]) {
    -moz-appearance: textfield;
  }
</style>
