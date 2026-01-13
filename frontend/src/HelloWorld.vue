<template>
  <div class="hello">
    <h2>Componente HelloWorld</h2>
    <p>Hora local: {{ now }}</p>
    <button @click="tick">Actualizar hora</button>
  </div>
</template>

<script>
export default {
  name: "HelloWorld",
  data() {
    return {
      now: new Date().toLocaleTimeString()
    };
  },
  methods: {
    tick() {
      this.now = new Date().toLocaleTimeString();
    }
  }
};
</script>

<style scoped>
.hello {
  padding: 12px;
  border-radius: 8px;
  background: #fff;
  border: 1px solid #e6e9ef;
}
h2 { margin: 0 0 8px 0; font-size:16px; }
button {
  margin-top:8px;
  padding:6px 10px;
  border-radius:6px;
  border:0;
  background:#0b5fff;
  color:#fff;
  cursor:pointer;
}
</style>
