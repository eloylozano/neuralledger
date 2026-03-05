<script lang="ts">
  import { onMount } from "svelte";
  import { fade, slide } from "svelte/transition";
  import {
    TrendingUp,
    FileText,
    Users,
    BrainCircuit,
    Plus,
    CheckCircle2,
  } from "lucide-svelte";
  import ApexCharts from "apexcharts";
  import KpiCard from "$lib/components/KpiCard.svelte";

  // --- ESTADOS ---
  let loading = $state(true);
  let showInsights = $state(false); // Para controlar cuándo aparecen las frases
  let dashboardData = $state({
    kpis: {
      total_spent: "0,00 €",
      processed_count: 0,
      suppliers_count: 0,
      pending_count: 0,
    },
    chart: { labels: [], values: [] },
    insights: [],
  });

  // --- ACCIÓN DE LA GRÁFICA ---
  function chartAction(node: HTMLElement) {
    let chart: ApexCharts;
    const style = getComputedStyle(document.documentElement);
    const primaryColor =
      style.getPropertyValue("--primary").trim() || "#00d2ff";
    const textMuted =
      style.getPropertyValue("--text-muted").trim() || "#94a3b8";

    const options = {
      chart: {
        type: "bar",
        height: "100%",
        toolbar: { show: false },
        background: "transparent",
        foreColor: textMuted,
        fontFamily: "Inter, ui-sans-serif, system-ui",
      },
      series: [{ name: "Gastos", data: dashboardData.chart.values }],
      xaxis: {
        categories: dashboardData.chart.labels,
        labels: { style: { colors: textMuted } },
      },
      yaxis: {
        labels: {
          style: { colors: textMuted },
          formatter: (val: number) => val.toLocaleString() + "€",
        },
      },
      colors: [primaryColor],
      plotOptions: { bar: { borderRadius: 6, columnWidth: "50%" } },
      dataLabels: { enabled: false },
      tooltip: { theme: "dark" },
    };

    chart = new ApexCharts(node, options);
    chart.render();

    return {
      update() {
        chart.updateSeries([{ data: dashboardData.chart.values }]);
        chart.updateOptions({
          xaxis: { categories: dashboardData.chart.labels },
        });
      },
      destroy() {
        chart.destroy();
      },
    };
  }

  // --- CICLO DE VIDA ---
  onMount(async () => {
    try {
      const res = await fetch("http://localhost:8000/dashboard/stats");
      if (res.ok) {
        dashboardData = await res.json();

        // Pequeño delay para que la gráfica cargue y luego mostramos los hallazgos
        setTimeout(() => {
          showInsights = true;
        }, 800);
      }
    } catch (e) {
      console.error("Error cargando dashboard:", e);
    } finally {
      loading = false;
    }
  });
</script>

<div class="dashboard-container">
  <header class="welcome-header">
    <div class="text">
      <h1>Panel de <span class="highlight">Control</span></h1>
      <p>
        NeuralLedger ha optimizado {dashboardData.kpis.processed_count} entradas
        hoy.
      </p>
    </div>
    <a href="/upload" class="new-btn"><Plus size={20} /> Nueva Subida</a>
  </header>

  <div class="kpi-grid">
    <KpiCard
      title="Volumen Total"
      value={dashboardData.kpis.total_spent}
      icon={TrendingUp}
      type="total"
    />
    <KpiCard
      title="Facturas"
      value={dashboardData.kpis.processed_count}
      icon={FileText}
      type="docs"
    />
    <KpiCard
      title="Proveedores"
      value={dashboardData.kpis.suppliers_count}
      icon={Users}
      type="suppliers"
    />
    <KpiCard
      title="Pendientes"
      value={dashboardData.kpis.pending_count}
      icon={BrainCircuit}
      type="brain"
      isWarning={dashboardData.kpis.pending_count > 0}
    />
  </div>

  <div class="main-grid">
    <div class="chart-card">
      <h3>Evolución de Gastos</h3>
      <div class="chart-wrapper">
        {#if !loading && dashboardData.chart.labels.length > 0}
          <div use:chartAction style="height: 100%; width: 100%;"></div>
        {:else}
          <div class="loading-overlay">Sincronizando métricas...</div>
        {/if}
      </div>
    </div>

    <div class="glass-card status-card">
      <h3>Auditoría de Datos</h3>
      <div class="ia-status">
        <div class="pulse-ring"></div>
        <span>NeuralLedger: Online</span>
      </div>

      <div class="insights-list">
        {#if showInsights}
          {#each dashboardData.insights as insight, i}
            <div
              class="insight-item"
              in:slide={{ delay: i * 200, duration: 400 }}
            >
              <CheckCircle2 size={16} class="icon-check" />
              <p>{insight}</p>
            </div>
          {/each}
        {:else}
          <p class="loading-text" in:fade>
            Analizando patrones de la base de datos...
          </p>
        {/if}
      </div>
    </div>
  </div>
</div>

<style>
  .dashboard-container {
    padding: 2rem;
    max-width: 1400px;
    margin: 0 auto;
    color: var(--text-main);
  }

  .welcome-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2.5rem;
  }

  .welcome-header h1 {
    font-size: 2.5rem;
    margin: 0;
    font-weight: 700;
  }

  .highlight {
    color: var(--primary);
    font-weight: 900;
  }

  .new-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: var(--primary);
    color: #000 !important;
    padding: 0.8rem 1.5rem;
    border-radius: 14px;
    font-weight: bold;
    text-decoration: none;
    box-shadow: 0 10px 20px -5px rgba(0, 210, 255, 0.4);
    transition: transform 0.2s;
  }

  .new-btn:hover {
    transform: translateY(-2px);
  }

  .kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
  }

  /* Ajustada la proporción para dar más espacio a los textos de la auditoría */
  .main-grid {
    display: grid;
    grid-template-columns: 3fr 1.5fr;
    gap: 1.5rem;
    align-items: start;
  }

  .chart-card,
  .status-card {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 24px;
    padding: 1.5rem;
    backdrop-filter: blur(10px);
    height: 100%;
  }

  .chart-wrapper {
    position: relative;
    height: 350px;
    width: 100%;
    margin-top: 1rem;
  }

  .ia-status {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
    color: var(--primary);
    font-weight: bold;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  .pulse-ring {
    width: 8px;
    height: 8px;
    background: var(--primary);
    border-radius: 50%;
    animation: pulse 2s infinite;
  }

  /* Contenedor de la lista de hallazgos */
  .insights-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  /* Estilo para cada hallazgo individual */
  .insight-item {
    display: flex;
    align-items: flex-start;
    gap: 0.8rem;
    background: rgba(255, 255, 255, 0.03);
    padding: 1rem;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-left: 4px solid var(--primary);
    transition: background 0.3s;
  }

  .insight-item:hover {
    background: rgba(255, 255, 255, 0.06);
  }

  .insight-item p {
    margin: 0;
    font-size: 0.9rem;
    line-height: 1.4;
    color: var(--text-muted);
  }

  /* Icono de check de Lucide */
  :global(.icon-check) {
    color: var(--primary);
    flex-shrink: 0;
    margin-top: 2px;
  }

  .loading-text {
    color: var(--text-muted);
    font-size: 0.9rem;
    font-style: italic;
    padding: 1rem;
  }

  @keyframes pulse {
    0% {
      transform: scale(0.95);
      box-shadow: 0 0 0 0 rgba(0, 210, 255, 0.7);
    }
    70% {
      transform: scale(1);
      box-shadow: 0 0 0 10px rgba(0, 210, 255, 0);
    }
    100% {
      transform: scale(0.95);
      box-shadow: 0 0 0 0 rgba(0, 210, 255, 0);
    }
  }

  .loading-overlay {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-muted);
    font-style: italic;
  }

  /* Responsivo para pantallas pequeñas */
  @media (max-width: 1024px) {
    .main-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
