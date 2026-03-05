// src/lib/theme.svelte.ts
export const palettes = [
    { name: "Oceanic", primary: "#00d2ff", secondary: "#3a7bd5", bg: "#0f172a", dark: true },
    { name: "Neon", primary: "#f222ff", secondary: "#8e2de2", bg: "#0b0114", dark: true },
    { name: "Magma", primary: "#ff4b1f", secondary: "#ff9068", bg: "#1a0b08", dark: true },

    // --- NUEVAS PALETAS DARK ---
    { name: "Matrix", primary: "#00ff41", secondary: "#008f11", bg: "#050505", dark: true }, // Estilo hacker clásico
    { name: "Midnight", primary: "#818cf8", secondary: "#c084fc", bg: "#020617", dark: true }, // Elegante y suave (tipo Linear)
    { name: "Gold", primary: "#fbbf24", secondary: "#d97706", bg: "#0c0a09", dark: true }, // Premium / Lujo

    // --- NUEVAS PALETAS LIGHT ---
    { name: "Sky", primary: "#00d2ff", secondary: "#3a7bd5", bg: "#f0f9ff", dark: false },
    { name: "Mint", primary: "#00b09b", secondary: "#96c93d", bg: "#f0fdf4", dark: false },
    { name: "Sakura", primary: "#ec4899", secondary: "#f43f5e", bg: "#fff1f2", dark: false }, // Rosado/Cálido agradable
];

let _selected = $state(palettes[0]);

export const theme = {
    get selected() { return _selected; },
    apply(p: typeof palettes[0]) {
        _selected = p;
        if (typeof document === 'undefined') return;

        const root = document.documentElement;
        root.style.setProperty("--primary", p.primary);
        root.style.setProperty("--secondary", p.secondary);
        root.style.setProperty("--bg-main", p.bg);

        // Transición suave para que el cambio de color sea placentero
        root.style.transition = "background-color 0.4s ease, color 0.4s ease";

        if (p.dark) {
            root.style.setProperty("--text-main", "#ffffff");
            root.style.setProperty("--text-muted", "rgba(255, 255, 255, 0.6)");
            root.style.setProperty("--glass-bg", "rgba(255, 255, 255, 0.03)");
            root.style.setProperty("--glass-border", "rgba(255, 255, 255, 0.08)");
            root.classList.add("dark-mode");
        } else {
            root.style.setProperty("--text-main", "#0f172a");
            root.style.setProperty("--text-muted", "rgba(15, 23, 42, 0.65)");
            root.style.setProperty("--glass-bg", "rgba(255, 255, 255, 0.7)");
            root.style.setProperty("--glass-border", "rgba(0, 0, 0, 0.08)");
            root.classList.remove("dark-mode");
        }
        localStorage.setItem("neural-theme", p.name);
    }
};