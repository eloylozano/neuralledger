<script lang="ts">
  let { icon: Icon, title, children, fullWidth = false } = $props();
</script>

<section class="settings-card" class:full-width={fullWidth}>
  <div class="card-title">
    {#if Icon}<Icon size={20} />{/if}
    <h2>{title}</h2>
  </div>
  {@render children()}
</section>

<style>
  .settings-card {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    padding: 1.5rem;
    border-radius: 20px;
    backdrop-filter: blur(10px);
  }
  .full-width {
    grid-column: span 2;
  }
  .card-title {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    color: var(--primary);
    margin-bottom: 1rem;
    text-transform: uppercase;
    font-weight: 800;
    font-size: 0.75rem;
  }
  .card-title h2 {
    font-size: 1rem;
    margin: 0;
    color: var(--text-muted);
  }
</style>
