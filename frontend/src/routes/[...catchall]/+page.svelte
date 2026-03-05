<script lang="ts">
    import { Home, ArrowLeft, Activity } from "lucide-svelte";
    import { fade, fly } from "svelte/transition";
  </script>
  
  <div class="error-internal-container" in:fade={{ duration: 400 }}>
    <div class="glass-card error-card" in:fly={{ y: 20, duration: 600 }}>
      
      <div class="neural-visual">
        <div class="central-node">
          <Activity size={32} class="node-icon" />
          <div class="rings">
            <div class="ring"></div>
            <div class="ring"></div>
            <div class="ring"></div>
          </div>
        </div>
        <h1 class="error-code">404</h1>
      </div>
  
      <div class="text-section">
        <h2 class="error-title">Nodo <span class="highlight">No Sincronizado</span></h2>
        <p class="error-message">
          La dirección solicitada no responde. El Ledger ha escaneado la ruta neural sin encontrar registros válidos.
        </p>
      </div>
  
      <div class="actions">
        <button class="btn-secondary" onclick={() => history.back()}>
          <ArrowLeft size={16} />
          Volver
        </button>
        
        <a href="/" class="btn-primary">
          <Home size={16} />
          Volver al inicio
        </a>
      </div>
    </div>
  </div>
  
  <style>
    .error-internal-container {
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 75vh;
      width: 100%;
    }
  
    .error-card {
      width: 100%;
      max-width: 460px;
      padding: 3.5rem 2.5rem;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      gap: 2rem;
      overflow: hidden;
    }
  
    /* Visual Neural */
    .neural-visual {
      position: relative;
      height: 120px;
      display: flex;
      justify-content: center;
      align-items: center;
    }
  
    .central-node {
      position: relative;
      z-index: 2;
      color: var(--primary);
      filter: drop-shadow(0 0 15px var(--primary));
    }
  
    .node-icon {
      animation: pulse-icon 2s ease-in-out infinite;
    }
  
    .rings {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
    }
  
    .ring {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      border: 1px solid var(--primary);
      border-radius: 50%;
      opacity: 0;
      animation: ripple 3s linear infinite;
    }
  
    .ring:nth-child(2) { animation-delay: 1s; }
    .ring:nth-child(3) { animation-delay: 2s; }
  
    .error-code {
      font-size: 7rem;
      font-weight: 900;
      margin: 0;
      line-height: 1;
      opacity: 0.05;
      position: absolute;
      color: var(--text-main);
      letter-spacing: -5px;
    }
  
    /* Texto */
    .error-title { font-size: 1.6rem; margin-bottom: 0.5rem; color: var(--text-main); }
    .highlight { color: var(--primary); text-shadow: 0 0 10px rgba(0, 210, 255, 0.3); }
    .error-message { 
      color: var(--text-muted); 
      font-size: 0.95rem; 
      line-height: 1.5;
      max-width: 300px;
    }
  
    /* Botones */
    .actions { display: flex; gap: 12px; width: 100%; }
  
    .btn-primary, .btn-secondary {
      flex: 1;
      padding: 0.8rem;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      font-size: 0.85rem;
      font-weight: 700;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      cursor: pointer;
      text-decoration: none;
    }
  
    .btn-primary {
      background: var(--primary);
      color: #0f172a;
      border: none;
      box-shadow: 0 4px 15px rgba(0, 210, 255, 0.2);
    }
  
    .btn-secondary {
      background: rgba(255, 255, 255, 0.03);
      color: var(--text-main);
      border: 1px solid var(--glass-border);
    }
  
    .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0, 210, 255, 0.4); }
    .btn-secondary:hover { background: rgba(255, 255, 255, 0.08); border-color: var(--primary); }
  
    /* Animaciones */
    @keyframes ripple {
      0% { width: 40px; height: 40px; opacity: 0.5; }
      100% { width: 200px; height: 200px; opacity: 0; }
    }
  
    @keyframes pulse-icon {
      0%, 100% { transform: scale(1); opacity: 1; }
      50% { transform: scale(1.1); opacity: 0.7; }
    }
  </style>