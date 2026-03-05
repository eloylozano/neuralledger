<script lang="ts">
    import SettingsCard from "$lib/components/SettingsCard.svelte";
    import ThemeSelector from "$lib/components/ThemeSelector.svelte";
    import DbSettings from "$lib/components/DbSettings.svelte";
    import { Palette, Brain, Database } from "lucide-svelte";
    import { fade } from "svelte/transition";
    import { onMount } from "svelte";
    import AIEngine from "$lib/components/AIEngine.svelte";
  
    let threshold = $state(2000);
    let timeoutId: number;
    let initialized = $state(false);
  
    onMount(async () => {
      // 1. Intentar cargar desde localStorage primero para rapidez visual
      const saved = localStorage.getItem("neural-threshold");
      if (saved) threshold = Number(saved);
  
      // 2. Sincronizar con los ajustes reales del servidor
      try {
        const res = await fetch("http://localhost:8000/api/settings");
        if (res.ok) {
          const data = await res.json();
          threshold = data.threshold;
        }
      } finally {
        initialized = true;
      }
    });
  
    // Efecto para guardado automático (Debounce de 800ms)
    $effect(() => {
      if (!initialized) return;
  
      clearTimeout(timeoutId);
      timeoutId = setTimeout(async () => {
        try {
          await fetch("http://localhost:8000/api/settings", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ threshold: Number(threshold) }),
          });
          localStorage.setItem("neural-threshold", threshold.toString());
        } catch (e) {
          console.error("Error guardando ajustes:", e);
        }
      }, 800);
    });
  </script>
  
  <div class="settings-container" in:fade>
    <header class="settings-header">
      <h1>Configuración del <span class="highlight">Sistema</span></h1>
      <p>Gestiona el comportamiento de los umbrales y el entorno visual.</p>
    </header>
  
    <div class="settings-grid">
      <SettingsCard title="Estilo Visual" icon={Palette}>
        <ThemeSelector />
      </SettingsCard>
  
      <SettingsCard title="Umbrales Críticos" icon={Brain}>
        <AIEngine bind:threshold />
      </SettingsCard>
  
      <SettingsCard
        title="Mantenimiento y Base de Datos"
        icon={Database}
        fullWidth={true}
      >
        <DbSettings />
      </SettingsCard>
    </div>
  </div>
  
  <style>
    .settings-container {
      padding: 2rem;
      max-width: 1000px;
      margin: 0 auto;
    }
    .settings-header { margin-bottom: 3rem; }
    .settings-header h1 {
      font-size: 2.5rem;
      margin: 0;
      color: var(--text-main);
    }
    .highlight { color: var(--primary); }
    .settings-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.5rem;
    }
  </style>