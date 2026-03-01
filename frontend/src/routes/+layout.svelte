<script>
  import "./layout.css";
  import {
    LayoutDashboard,
    Upload,
    Database,
    Palette,
    Settings,
  } from "lucide-svelte";
  import { onMount } from "svelte";

  let { children } = $props();

  const palettes = [
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
      name: "Sky",
      primary: "#00d2ff",
      secondary: "#3a7bd5",
      bg: "#f0f9ff",
      dark: false,
    },
    {
      name: "Mint",
      primary: "#00b09b",
      secondary: "#96c93d",
      bg: "#f0fdf4",
      dark: false,
    },
  ];

  let selectedPalette = $state(palettes[0]);

  function applyPalette(p, save = true) {
    selectedPalette = p;
    const root = document.documentElement;

    // Aplicar variables CSS
    root.style.setProperty("--primary", p.primary);
    root.style.setProperty("--secondary", p.secondary);
    root.style.setProperty("--bg-main", p.bg);

    if (p.dark) {
      root.style.setProperty("--text-main", "#ffffff");
      root.style.setProperty("--text-muted", "rgba(255, 255, 255, 0.7)");
      root.style.setProperty("--glass-bg", "rgba(255, 255, 255, 0.03)");
      root.style.setProperty("--glass-border", "rgba(255, 255, 255, 0.1)");
      root.classList.add("dark-mode");
    } else {
      root.style.setProperty("--text-main", "#0f172a");
      root.style.setProperty("--text-muted", "rgba(15, 23, 42, 0.7)");
      root.style.setProperty("--glass-bg", "rgba(0, 0, 0, 0.05)");
      root.style.setProperty("--glass-border", "rgba(0, 0, 0, 0.12)");
      root.classList.remove("dark-mode");
    }

    // Guardar preferencia
    if (save) {
      localStorage.setItem("neural-theme", p.name);
    }
  }

  onMount(() => {
    // 1. Intentar recuperar del localStorage
    const savedThemeName = localStorage.getItem("neural-theme");

    if (savedThemeName) {
      const found = palettes.find((p) => p.name === savedThemeName);
      if (found) {
        applyPalette(found, false);
        return;
      }
    }

    // 2. Si no hay nada, aplicar el por defecto
    applyPalette(palettes[0], false);
  });
</script>

<div class="app-container">
  <aside class="sidebar">
    <div class="logo">
      <a href="/" class="logo-link">
        <div class="logo-icon">
          <Database size={20} color="white" />
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
      <div class="palette-picker">
        <p><Palette size={14} /> Estilo Visual</p>
        <div class="palette-buttons">
          {#each palettes as p}
            <button
              aria-label="Seleccionar tema {p.name}"
              class="p-dot {selectedPalette.name === p.name ? 'active' : ''}"
              style="background: linear-gradient(135deg, {p.primary}, {p.secondary})"
              onclick={() => applyPalette(p)}
            ></button>
          {/each}
        </div>
      </div>

      <a href="/settings" class="nav-item" style="margin-top: 1.5rem;">
        <Settings size={20} />
        <span>Ajustes</span>
      </a>
    </div>
  </aside>

  <main class="main-content">
    {@render children()}
  </main>
</div>

<style>
  /* Estilos adicionales para los botones de la paleta */
  .palette-buttons {
    display: flex;
    gap: 8px;
    margin-top: 10px;
  }

  .p-dot {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    border: 2px solid transparent;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    padding: 0;
  }

  .p-dot:hover {
    transform: scale(1.2);
  }

  .p-dot.active {
    border-color: var(--text-main);
    box-shadow: 0 0 10px var(--primary);
    transform: scale(1.1);
  }

  .logo-text span {
    color: var(--primary);
  }
</style>
