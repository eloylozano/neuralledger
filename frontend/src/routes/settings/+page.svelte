<script lang="ts">
  import SettingsCard from "$lib/components/SettingsCard.svelte";
  import ThemeSelector from "$lib/components/ThemeSelector.svelte";
  import DbSettings from "$lib/components/DbSettings.svelte"; // Nuevo
  import { Palette, Brain, Database } from "lucide-svelte";
  import { fade } from "svelte/transition";
  import { onMount } from "svelte";
  import AIEngine from "$lib/components/AIEngine.svelte";

  let threshold = $state(2000);
  let timeoutId: number;

  onMount(() => {
    const saved = localStorage.getItem("neural-threshold");
    if (saved) threshold = Number(saved);
  });

  // Sincronización DB Settings
  $effect(() => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(async () => {
      try {
        await fetch("/api/settings", {
          method: "POST",
          body: JSON.stringify({ threshold }),
          headers: { "Content-Type": "application/json" },
        });
      } catch (e) {
        console.error(e);
      }
    }, 800);
  });

  $effect(() => {
    localStorage.setItem("neural-threshold", threshold.toString());
  });
</script>

<div class="settings-container" in:fade>
  <header class="settings-header">
    <h1>Configuración del <span class="highlight">Sistema</span></h1>
    <p>Gestiona el comportamiento de la IA y el entorno visual.</p>
  </header>

  <div class="settings-grid">
    <SettingsCard title="Estilo Visual" icon={Palette}>
      <ThemeSelector />
    </SettingsCard>

    <SettingsCard title="Motor Neural (Ollama)" icon={Brain}>
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
  .settings-header {
    margin-bottom: 3rem;
  }
  .settings-header h1 {
    font-size: 2.5rem;
    margin: 0;
    color: var(--text-main);
  }
  .highlight {
    color: var(--primary);
  }
  .settings-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
  }
</style>
