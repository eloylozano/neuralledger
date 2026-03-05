<script lang="ts">
  import type { Component } from "svelte";

  interface Props {
    title: string;
    value: string | number;
    icon: Component;
    type: "total" | "docs" | "suppliers" | "brain";
    isWarning?: boolean;
  }

  let { title, value, icon: Icon, type, isWarning = false }: Props = $props();
</script>

<div class="kpi-card">
  <div class="kpi-icon {type}">
    <Icon size={20} />
  </div>
  <div class="kpi-info">
    <span>{title}</span>
    <strong class={isWarning ? "text-orange" : ""}>{value}</strong>
  </div>
</div>

<style>
  .kpi-card {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    padding: 1.5rem;
    border-radius: 20px;
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  .kpi-icon {
    width: 45px;
    height: 45px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .kpi-icon.total {
    background: rgba(0, 210, 255, 0.1);
    color: var(--primary);
  }
  .kpi-icon.docs {
    background: rgba(167, 139, 250, 0.1);
    color: #a78bfa;
  }
  .kpi-icon.suppliers {
    background: rgba(52, 211, 153, 0.1);
    color: #34d399;
  }
  .kpi-icon.brain {
    background: rgba(251, 146, 60, 0.1);
    color: #fb923c;
  }

  .kpi-info span {
    font-size: 0.75rem;
    color: var(--text-muted);
    text-transform: uppercase;
    font-weight: bold;
  }
  .kpi-info strong {
    font-size: 1.25rem;
    display: block;
  }
  .text-orange {
    color: #fb923c;
  }
</style>
