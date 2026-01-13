<template>
  <div class="container">
    <div class="header">
      <h1>Generador de QR (PNG)</h1>
      <div class="small">Frontend: Vue 3 + Vite · Backend: Flask</div>
    </div>

    <div class="form-row">
      <input
        type="text"
        v-model="url"
        placeholder="Pega una URL (ej. https://example.com)"
        @keyup.enter="onGenerate"
      />
      <button @click="onGenerate" :disabled="loading">Generar</button>
    </div>

    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="imgVisible" class="preview">
      <div class="qr-card">
        <img :src="imgSrc" alt="QR" />
      </div>
      <div class="actions">
        <button @click="onDownload" :disabled="downloading">Descargar PNG</button>
        <div class="small">URL: <strong>{{ trimmedUrl }}</strong></div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from "vue";

export default {
  setup() {
    const backendBase = "http://localhost:5000";
    const url = ref("");
    const error = ref("");
    const loading = ref(false);
    const downloading = ref(false);
    const imgVisible = ref(false);
    const imgSrc = ref("");

    const trimmedUrl = computed(() => url.value.trim());

    async function onGenerate() {
      error.value = "";
      imgVisible.value = false;
      imgSrc.value = "";
      const raw = url.value || "";
      const candidate = raw.trim();
      if (!candidate) {
        error.value = "Introduce una URL.";
        return;
      }
      // Build endpoint
      const endpoint = `${backendBase}/qr?url=${encodeURIComponent(candidate)}`;
      loading.value = true;
      try {
        // Validate by calling the endpoint and checking response
        const resp = await fetch(endpoint, { method: "GET" });
        if (!resp.ok) {
          // backend returns JSON { error: "..." }
          let json;
          try {
            json = await resp.json();
          } catch (e) {
            throw new Error("Respuesta inválida del servidor.");
          }
          throw new Error(json.error || "Error al generar el QR.");
        }
        // OK: show image by setting img src (browser will request again)
        imgSrc.value = endpoint;
        imgVisible.value = true;
      } catch (err) {
        error.value = err.message || "Error desconocido.";
      } finally {
        loading.value = false;
      }
    }

    async function onDownload() {
      if (!imgVisible.value) return;
      downloading.value = true;
      error.value = "";
      try {
        const endpoint = `${backendBase}/qr?url=${encodeURIComponent(trimmedUrl.value)}`;
        const resp = await fetch(endpoint, { method: "GET" });
        if (!resp.ok) {
          let json;
          try {
            json = await resp.json();
          } catch (e) {
            throw new Error("Respuesta inválida del servidor al descargar.");
          }
          throw new Error(json.error || "Error al descargar el PNG.");
        }
        const blob = await resp.blob();
        const blobUrl = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = blobUrl;
        a.download = "qr.png";
        document.body.appendChild(a);
        a.click();
        a.remove();
        URL.revokeObjectURL(blobUrl);
      } catch (err) {
        error.value = err.message || "Error desconocido al descargar.";
      } finally {
        downloading.value = false;
      }
    }

    return {
      url,
      error,
      loading,
      imgVisible,
      imgSrc,
      onGenerate,
      onDownload,
      downloading,
      trimmedUrl,
    };
  },
};
</script>
