<script>
  import "./layout.css";
  import { LayoutDashboard, Upload, Database, Palette, Settings } from "lucide-svelte";
  import { onMount } from "svelte";

  let { children } = $props();

  const palettes = [
    { name: "Oceanic", primary: "#00d2ff", secondary: "#3a7bd5", bg: "#0f172a", dark: true },
    { name: "Neon", primary: "#f222ff", secondary: "#8e2de2", bg: "#0b0114", dark: true },
    { name: "Magma", primary: "#ff4b1f", secondary: "#ff9068", bg: "#1a0b08", dark: true },
    { name: "Sky", primary: "#00d2ff", secondary: "#3a7bd5", bg: "#f0f9ff", dark: false },
    { name: "Mint", primary: "#00b09b", secondary: "#96c93d", bg: "#f0fdf4", dark: false }
  ];

  let selectedPalette = $state(palettes[0]);

  function applyPalette(p) {
    selectedPalette = p;
    const root = document.documentElement;

    root.style.setProperty("--primary", p.primary);
    root.style.setProperty("--secondary", p.secondary);
    root.style.setProperty("--bg-main", p.bg);

    if (p.dark) {
      root.style.setProperty("--text-main", "#ffffff");
      root.style.setProperty("--text-muted", "rgba(255, 255, 255, 0.7)");
      root.style.setProperty("--glass-bg", "rgba(255, 255, 255, 0.03)");
      root.style.setProperty("--glass-border", "rgba(255, 255, 255, 0.1)");
    } else {
      root.style.setProperty("--text-main", "#0f172a");
      root.style.setProperty("--text-muted", "rgba(15, 23, 42, 0.7)");
      root.style.setProperty("--glass-bg", "rgba(0, 0, 0, 0.05)");
      root.style.setProperty("--glass-border", "rgba(0, 0, 0, 0.12)");
    }
  }

  onMount(() => applyPalette(palettes[0]));
</script>

<div class="app-container">
  <aside class="sidebar">
    <div class="logo">
      <a href="/" class="logo-link">
        <div class="logo-icon">
          <Database size={20} color="white" />
        </div>
        <span class="logo-text">Neural Ledger</span>
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
      <a href="/invoices" class="nav-item">
        <Database size={20} />
        <span>Histórico</span>
      </a>
    </nav>

    <div class="sidebar-footer">
      <div class="palette-picker">
        <p><Palette size={14} /> Estilo Visual</p>
        <div class="palette-buttons">
          {#each palettes as p}
            <button
            aria-label="Change palette"
              class="p-dot {selectedPalette.name === p.name ? 'active' : ''}"
              style="background: {p.primary}"
              onclick={() => applyPalette(p)}
            ></button>
          {/each}
        </div>
      </div>
      
      <a href="/settings" class="nav-item" style="margin-top: 1rem;">
        <Settings size={20} />
        <span>Ajustes</span>
      </a>
    </div>
  </aside>

  <main class="main-content">
    {@render children()}
  </main>
</div>
