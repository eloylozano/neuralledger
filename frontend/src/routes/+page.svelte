<svelte:head>
  <title>NeuralLedger | Dashboard</title>
</svelte:head>

<div class="welcome-section">
  <header>
    <h1>Bienvenido a <span>NeuralLedger</span></h1>
    <p>Tu asistente inteligente de contabilidad</p>
  </header>

  <div class="mockup-section">
    <div class="glass-card">
      <h3>Estado del Sistema</h3>
      <div class="stats-grid">
        <div class="stat">
          <span>Procesadas</span>
          <strong>24</strong>
        </div>
        <div class="stat">
          <span>Pendientes</span>
          <strong>3</strong>
        </div>
      </div>

      <div class="ia-note">
        DeepSeek-R1 está listo para procesar tus documentos.
      </div>

      <a href="/upload" class="main-btn">Nueva Subida</a>
    </div>
  </div>
</div>

<style>
  .welcome-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 3rem;
  }

  header {
    text-align: center;
  }
  header h1 {
    font-size: 3rem;
    margin-bottom: 0.5rem;
  }
  header h1 span {
    color: var(--primary);
  }
  header p {
    opacity: 0.6;
    font-size: 1.1rem;
  }
  h1 {
    color: var(--text-main); /* <--- Usa la variable, no "white" */
  }
  p {
    color: var(--text-muted);
  }
  .glass-card {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 2.5rem;
    border-radius: 24px;
    width: 400px;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin: 1.5rem 0;
  }

  .stat {
    background: rgba(255, 255, 255, 0.05);
    padding: 1rem;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
  }

  .stat span {
    font-size: 0.8rem;
    opacity: 0.5;
  }
  .stat strong {
    font-size: 1.5rem;
    color: var(--primary);
  }

  .ia-note {
    background: rgba(255, 255, 255, 0.05);
    border-left: 3px solid var(--primary);
    padding: 1rem;
    font-size: 0.9rem;
    margin-bottom: 2rem;
    font-style: italic;
  }

  .main-btn {
    display: block;
    text-align: center;
    text-decoration: none;
    padding: 1rem;
    border-radius: 12px;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    color: white;
    font-weight: bold;
    box-shadow: 0 10px 20px -5px var(--primary);
  }
</style>
