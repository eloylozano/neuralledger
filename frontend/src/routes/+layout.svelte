<script>
  import "./layout.css";
  import {
    LayoutDashboard,
    Upload,
    Database,
    Settings,
    Palette,
  } from "lucide-svelte";
  import { onMount } from "svelte";

  let { children } = $props();

  const palettes = [
    // OSCURAS
    {
      name: "Oceanic",
      primary: "#00d2ff",
      secondary: "#3a7bd5",
      bg: "#0f172a",
      dark: true,
    },
    {
      name: "Neon",
      primary: "#f222ff",
      secondary: "#8e2de2",
      bg: "#0b0114",
      dark: true,
    },
    {
      name: "Magma",
      primary: "#ff4b1f",
      secondary: "#ff9068",
      bg: "#1a0b08",
      dark: true,
    },
    {
      name: "Forest",
      primary: "#10b981",
      secondary: "#059669",
      bg: "#02100d",
      dark: true,
    },
    {
      name: "Carbon",
      primary: "#f59e0b",
      secondary: "#d97706",
      bg: "#0c0a09",
      dark: true,
    },

  ];

  let selectedPalette = $state(palettes[0]);

  function applyPalette(p) {
    selectedPalette = p;
    const root = document.documentElement;

    // 1. Aplicar colores de fondo y acento
    root.style.setProperty("--primary", p.primary);
    root.style.setProperty("--secondary", p.secondary);
    root.style.setProperty("--bg-main", p.bg);

    // 2. Aplicar color de fuente según si la paleta es oscura o clara
    if (p.dark) {
      root.style.setProperty("--text-main", "#ffffff");
      root.style.setProperty("--text-muted", "rgba(255, 255, 255, 0.6)");
    } else {
      root.style.setProperty("--text-main", "#0f172a"); // Azul muy oscuro
      root.style.setProperty("--text-muted", "rgba(15, 23, 42, 0.6)");
    }
  }

  onMount(() => applyPalette(palettes[0]));
</script>

<div
  class="app-container"
  style="--primary: {selectedPalette.primary}; --secondary: {selectedPalette.secondary}; --bg-main: {selectedPalette.bg};"
>
  <div class="liquid-bg"></div>

  <aside class="sidebar">
    <div class="logo">
      <div class="logo-icon">
        <Database size={20} color="white" />
      </div>
      <span class="logo-text">Neural<span>Ledger</span></span>
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
      <a href="/invoices" class="nav-item">
        <Database size={20} />
        <span>Histórico</span>
      </a>
    </nav>

    <div class="palette-picker">
      <p><Palette size={14} /> Estilo</p>
      <div class="palette-buttons">
        {#each palettes as p}
          <button
            class="p-dot {selectedPalette.name === p.name ? 'active' : ''}"
            style="background: {p.primary}"
            onclick={() => applyPalette(p)}
            title={p.name}
          ></button>
        {/each}
      </div>
    </div>
  </aside>

  <main class="main-content">
    {@render children()}
  </main>
</div>

<style>
  :global(body) {
    margin: 0;
    background: var(--bg-main);
    color: white;
    font-family: "Inter", sans-serif;
    overflow: hidden;
  }

  h1 {
    color: var(--text-main); /* <--- Usa la variable, no "white" */
  }
  p {
    color: var(--text-muted);
  }
  .app-container {
    display: flex;
    height: 100vh;
    width: 100vw;
    background: var(--bg-main);
    transition: background 0.5s ease;
  }

  .liquid-bg {
    position: fixed;
    top: -150px;
    left: -150px;
    width: 600px;
    height: 600px;
    background: var(--primary);
    filter: blur(120px);
    opacity: 0.15;
    border-radius: 50%;
    z-index: 0;
    pointer-events: none;
  }

  .sidebar {
    width: 320px;
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    flex-direction: column;
    padding: 2rem 1.5rem;
    z-index: 10;
  }

  .logo {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 3rem;
  }
  .logo-icon {
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .logo-text {
    font-weight: 700;
    font-size: 1.2rem;
  }
  .logo-text span {
    color: var(--primary);
  }

  nav {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  .nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    color: var(--text-muted);
    padding: 0.8rem;
    color: rgba(255, 255, 255, 0.6);
    text-decoration: none;
    border-radius: 10px;
  }
  .nav-item:hover {
    background: rgba(255, 255, 255, 0.05);
    color: white;
    color: var(--text-main);
  }

  .palette-picker {
    padding-top: 1rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
  }
  .palette-picker p {
    font-size: 0.7rem;
    opacity: 0.5;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 5px;
  }
  .palette-buttons {
    display: flex;
    gap: 8px;
  }
  .p-dot {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    border: 2px solid transparent;
    cursor: pointer;
    transition: transform 0.2s;
  }
  .p-dot.active {
    border-color: white;
    transform: scale(1.2);
  }

  .main-content {
    flex: 1;
    overflow-y: auto;
    padding: 2rem;
    z-index: 1;
  }
</style>
