<script>
    let { progress = 0, status = "Procesando..." } = $props();
  </script>
  
  <div class="loading-wrapper">
    <div class="glass-card loading-card">
      <div class="progress-ring">
        <svg width="120" height="120">
          <circle class="bg" cx="60" cy="60" r="54" />
          <circle 
            class="fill" 
            cx="60" cy="60" r="54" 
            style="stroke-dashoffset: {339 - (339 * progress) / 100}" 
          />
        </svg>
        <div class="percentage">{progress}%</div>
      </div>
      <h3>{status}</h3>
      <p>La IA  está analizando los datos...</p>
    </div>
  </div>
  
  <style>
    .loading-wrapper {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 400px;
    }
    .loading-card {
      padding: 3rem;
      text-align: center;
      width: 320px;
    }
    .progress-ring {
      position: relative;
      width: 120px;
      height: 120px;
      margin: 0 auto 1.5rem;
    }
    svg { transform: rotate(-90deg); }
    circle {
      fill: none;
      stroke-width: 8;
      stroke-linecap: round;
    }
    .bg { stroke: var(--glass-border); }
    .fill {
      stroke: var(--primary);
      stroke-dasharray: 339;
      transition: stroke-dashoffset 0.5s ease;
    }
    .percentage {
      position: absolute;
      top: 50%; left: 50%;
      transform: translate(-50%, -50%);
      font-size: 1.5rem;
      font-weight: 700;
      color: var(--primary);
    }
  </style>