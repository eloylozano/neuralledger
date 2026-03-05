<script>
  import { onMount } from "svelte";
  let { progress = 0 } = $props();

  let seconds = $state(0);
  let timerInterval;

  // Usamos onMount para que el cronómetro empiece nada más nacer el componente
  onMount(() => {
    timerInterval = setInterval(() => {
      // Solo sumamos si el progreso no ha llegado al final
      if (progress < 100) {
        seconds += 1;
      }
    }, 1000);

    // Limpieza al destruir el componente
    return () => {
      if (timerInterval) clearInterval(timerInterval);
    };
  });

  // Efecto reactivo para detenerlo si el progreso llega a 100 súbitamente
  $effect(() => {
    if (progress >= 100) {
      clearInterval(timerInterval);
    }
  });

  let statusMessage = $derived(
    progress < 30
      ? "Subiendo documento..."
      : progress < 60
        ? "NeuralLedger analizando conceptos..."
        : progress < 90
          ? "Extrayendo líneas de detalle..."
          : "Finalizando auditoría..."
  );
</script>

<div class="loading-wrapper">
  <div class="glass-card loading-card">
    <div class="progress-ring" class:analyzing={progress > 0 && progress < 100}>
      <svg width="140" height="140">
        <circle class="bg" cx="70" cy="70" r="62" />
        <circle
          class="fill"
          cx="70"
          cy="70"
          r="62"
          style="stroke-dasharray: 390; stroke-dashoffset: {390 - (390 * progress) / 100}"
        />
      </svg>
      
      <div class="percentage-container">
        <span class="number">{progress}%</span>
        <span class="chrono">{seconds}s</span>
        <span class="label">Neural Scan</span>
      </div>
    </div>

    <div class="status-info">
      <h3>{statusMessage}</h3>
      <div class="scanning-line"></div>
    </div>
  </div>
</div>

<style>
  /* Mantenemos tus estilos anteriores, asegurando que .chrono se vea bien */
  .loading-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 450px;
  }

  .loading-card {
    padding: 3rem;
    text-align: center;
    width: 360px;
    display: flex;
    flex-direction: column;
    align-items: center;
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    backdrop-filter: blur(20px);
    border-radius: 24px;
  }

  .progress-ring {
    position: relative;
    width: 140px;
    height: 140px;
    margin-bottom: 2rem;
  }

  .analyzing {
    filter: drop-shadow(0 0 15px color-mix(in srgb, var(--primary), transparent 50%));
    animation: pulse 2s infinite ease-in-out;
  }

  svg { transform: rotate(-90deg); }
  circle { fill: none; stroke-width: 10; stroke-linecap: round; }
  .bg { stroke: var(--glass-border); opacity: 0.3; }
  .fill {
    stroke: var(--primary);
    transition: stroke-dashoffset 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .percentage-container {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    flex-direction: column;
    align-items: center;
    line-height: 1.2;
  }

  .number {
    font-size: 1.8rem;
    font-weight: 800;
    color: var(--text-main);
  }

  .chrono {
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 0.9rem;
    color: var(--primary);
    font-weight: 700;
    text-shadow: 0 0 10px color-mix(in srgb, var(--primary), transparent 70%);
    margin: 2px 0;
  }

  .label {
    font-size: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--text-muted);
    font-weight: 700;
  }

  .status-info h3 {
    font-size: 0.9rem;
    color: var(--text-main);
    font-weight: 500;
    margin-bottom: 1rem;
  }

  .scanning-line {
    width: 100px;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--primary), transparent);
    margin: 0 auto;
    position: relative;
    overflow: hidden;
  }

  .scanning-line::after {
    content: "";
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: white;
    animation: scan 1.5s infinite;
  }

  @keyframes scan { 0% { left: -100%; } 100% { left: 100%; } }
  @keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.02); opacity: 0.8; }
  }
</style>