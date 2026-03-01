<div class="welcome-section">
  <header>
    <h1>Bienvenido a <span>NeuralLedger</span></h1>
    <p>Tu asistente inteligente de contabilidad</p>
  </header>

  <div class="mockup-section">
    <div class="glass-card p-10 w-[450px]">
      <h3 class="text-xl font-bold mb-4">Estado del Sistema</h3>
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
    font-size: 3.5rem;
    margin: 0;
  }
  header h1 span {
    color: var(--primary);
  }

  .stats-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-bottom: 2rem;
  }
  .stat {
    background: var(--glass-bg);
    padding: 1.5rem;
    border-radius: 16px;
    border: 1px solid var(--glass-border);
  }
  .stat strong {
    font-size: 1.8rem;
    color: var(--primary);
    display: block;
  }

  .ia-note {
    background: var(--glass-bg);
    border-left: 4px solid var(--primary);
    padding: 1rem;
    font-size: 0.9rem;
    margin-bottom: 2rem;
    font-style: italic;
  }

  .main-btn {
    display: block;
    text-align: center;
    text-decoration: none;
    padding: 1.2rem;
    border-radius: 14px;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    color: white !important;
    font-weight: bold;
    transition: 0.3s;
    box-shadow: 0 10px 20px -5px var(--primary);
  }
  .main-btn:hover {
    transform: translateY(-2px);
    filter: brightness(1.1);
  }
</style>
