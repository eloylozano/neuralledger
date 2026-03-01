<script>
    import { FileText, Users, ArrowRight } from "lucide-svelte";
  </script>
  
  <div class="main-content">
    <header class="mb-10">
      <h1 class="text-3xl font-extrabold tracking-tight">Base de Datos Neural</h1>
      <p class="text-[var(--text-muted)] mt-2">Gestiona la información estructurada de tu negocio.</p>
    </header>
  
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
      <a href="/database/invoices" class="db-card group">
        <div class="icon-box">
          <FileText size={32} class="text-[var(--primary)]" />
        </div>
        <div class="content">
          <h2>Facturas</h2>
          <p>Visualiza el histórico, revisa PDFs y exporta datos contables.</p>
          <div class="stats">
            <span class="badge">Revisar detalles</span>
          </div>
        </div>
        <ArrowRight class="arrow" />
      </a>
  
      <a href="/database/suppliers" class="db-card group">
        <div class="icon-box">
          <Users size={32} class="text-[var(--primary)]" />
        </div>
        <div class="content">
          <h2>Proveedores</h2>
          <p>Gestiona la "memoria" de la IA, edita CIFs y notas de procesamiento.</p>
          <div class="stats">
            <span class="badge">Gestionar memoria</span>
          </div>
        </div>
        <ArrowRight class="arrow" />
      </a>
    </div>
  </div>
  
  <style>
    .db-card {
      background: var(--glass-bg);
      border: 1px solid var(--glass-border);
      padding: 2rem;
      border-radius: 24px;
      display: flex;
      align-items: flex-start;
      gap: 1.5rem;
      position: relative;
      transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
      text-decoration: none;
      color: var(--text-main);
      overflow: hidden;
    }
  
    .db-card:hover {
      background: rgba(255, 255, 255, 0.05);
      border-color: var(--primary);
      transform: translateY(-5px);
      box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }
  
    .icon-box {
      background: rgba(0, 210, 255, 0.1);
      padding: 1rem;
      border-radius: 16px;
      border: 1px solid rgba(0, 210, 255, 0.2);
    }
  
    .content h2 {
      font-size: 1.5rem;
      font-weight: 800;
      margin-bottom: 0.5rem;
    }
  
    .content p {
      font-size: 0.9rem;
      color: var(--text-muted);
      line-height: 1.5;
      margin-bottom: 1.5rem;
    }
  
    .badge {
      font-size: 0.7rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
      background: var(--primary);
      color: #0f172a;
      padding: 4px 12px;
      border-radius: 20px;
    }
  
    .arrow {
      position: absolute;
      right: 2rem;
      bottom: 2rem;
      opacity: 0;
      transform: translateX(-10px);
      transition: all 0.3s ease;
      color: var(--primary);
    }
  
    .db-card:hover .arrow {
      opacity: 1;
      transform: translateX(0);
    }
  
    /* Efecto de brillo de fondo */
    .db-card::before {
      content: "";
      position: absolute;
      top: 0; left: 0; width: 100%; height: 100%;
      background: radial-gradient(circle at top right, var(--primary), transparent 150px);
      opacity: 0;
      transition: opacity 0.4s;
    }
  
    .db-card:hover::before {
      opacity: 0.05;
    }
  </style>