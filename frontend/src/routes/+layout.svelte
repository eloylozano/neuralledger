<script lang="ts">
  import "./layout.css";
  import { theme, palettes } from "$lib/theme.svelte";
  import { LayoutDashboard, Upload, Database, Palette, Settings } from "lucide-svelte";
  import { onMount } from "svelte";

  let { children } = $props();

  onMount(() => {
    const saved = localStorage.getItem("neural-theme");
    const found = palettes.find(p => p.name === saved) || palettes[0];
    theme.apply(found);
  });
</script>

<div class="app-container">
  <div class="bg-glow spot-1"></div>
  <div class="bg-glow spot-2"></div>

  <aside class="sidebar">
    <div class="logo">
      <a href="/" class="logo-link">
        <div class="logo-icon">
          <img src="/logo.png" alt="Logo" class="img-fluid" />
        </div>
        <span class="logo-text">Neural <span>Ledger</span></span>
      </a>
    </div>

    <nav>
      <a href="/" class="nav-item">
        <LayoutDashboard size={20} />
        <span>Dashboard</span>
      </a>
      <a href="/upload" class="nav-item">
        <Upload size={20} />
        <span>Subir Factura</span>
      </a>
      <a href="/database" class="nav-item">
        <Database size={20} />
        <span>Base de Datos</span>
      </a>
    </nav>

    <div class="sidebar-footer">
      <a href="/settings" class="nav-item settings-item">
        <div class="settings-icon">
          <Settings size={20} />
        </div>
        <span>Ajustes</span>
      </a>
    </div>
  </aside>

  <main class="main-content">
    {@render children()}
  </main>
</div>

<style>
  /* Estilos para los focos de luz */
  .bg-glow {
    position: fixed;
    width: 600px;
    height: 600px;
    border-radius: 50%;
    filter: blur(120px);
    z-index: -1;
    opacity: 0.15;
    pointer-events: none;
    transition: background 0.8s ease;
  }

  .spot-1 {
    top: -200px;
    right: -100px;
    background: var(--primary);
  }

  .spot-2 {
    bottom: -200px;
    left: 10%;
    background: var(--secondary);
  }

  /* El resto de tus estilos de sidebar... */
  .logo-text span { color: var(--primary); }

  .settings-icon {
    display: flex;
    transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  }
  
  .nav-item:hover .settings-icon {
    transform: rotate(90deg);
    color: var(--primary);
  }
</style>