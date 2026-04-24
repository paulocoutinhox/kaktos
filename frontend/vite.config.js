import path from "path";
import { fileURLToPath } from "url";

import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "vite";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig({
    plugins: [tailwindcss()],

    base: "/static/",

    publicDir: "public",

    build: {
        outDir: "dist",
        emptyOutDir: true,
        manifest: true,

        rollupOptions: {
            input: {
                main: path.resolve(__dirname, "src/main.js"),
            },
            output: {
                entryFileNames: "[name]-[hash].js",
                chunkFileNames: "[name]-[hash].js",
                assetFileNames: "[name]-[hash][extname]",
            },
        },
    },
});
