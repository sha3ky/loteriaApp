<!-- InfiniteScrollComponent.vue -->
<template>
   <q-option-group
        v-model="panel"
        inline
        :options="[
          { label: 'Muro Movil', value: 'muroMovil' },
          { label: 'Lista', value: 'lista' },
        ]"
        style="text-align: center;"
      />

      <q-tab-panels v-model="panel" animated class="shadow-2 rounded-borders">
        <q-tab-panel name="muroMovil">
          <div
    ref="scrollContainer"
    style="
      height: 100vh;
      overflow: hidden;
      height: 80vh;
      position: relative;
      padding: 10px;
   "
    @scroll="handleScroll"
  >
    <div
      v-for="(post, index) in posts"
      :key="index"
      class="post"
      style="overflow: hidden"
    >
      <h5 style="margin: 0px">{{ post.nombre }}</h5>
      <img
        :src="post.imagen"
        style="width: 45%; height: auto; margin-bottom: 10px"
        alt="Imagen del producto"
      />
      <p style="margin: 0px">{{ post.descripcion }}</p>
    </div>
  </div>
        </q-tab-panel>

       <q-tab-panel name="lista">
        <div class="text-h6" style="text-align: center;">Lista Completa</div>
       
          <template v-for="(post, index) in contenedor" :key="index">
        <p class="post">{{ post.nombre }} {{ post.price ?? '' }}</p>         
       </template>
       
        </q-tab-panel>

       
      </q-tab-panels>
 
</template>

<script>
import { ref, onMounted, onUnmounted, nextTick } from "vue";
import { getPosts } from "../variosJs/post-loader";

export default {
  setup() {
    const panel= ref('muroMovil')
    const posts = ref([]); // Lista de posts
    const loading = ref(false); // Estado de carga
    const scrollContainer = ref(null); // Contenedor de scroll
    let retryTimeout = null; // Controla el reintento
    let scrollInterval = null; // Variable para almacenar el intervalo de auto-scroll
    let fetchInterval = null;
    // cargar productos desde la base de datos
    const contenedor=ref([])

    const loadProductosBBDD = async (count = 10) => {
      if (loading.value) {
        return; // Evita múltiples solicitudes concurrentes
      }
      loading.value = true; // Marca el estado como cargando
      try {
        const newPosts = await getPosts(count); // Obtiene nuevos posts
        contenedor.value=newPosts
        if (newPosts.length > 0) {
          posts.value.push(...newPosts); // Agrega los nuevos posts si existen
        } else {
          console.log("No hay nuevos productos.");
        }
      } catch (error) {
        console.error("Error fetching posts:", error);
      } finally {
        loading.value = false; // Finaliza el estado de carga
      }
    };

    // movimiento automatico de scroll

    const autoScroll = () => {
      const container = scrollContainer.value;
      if (!container) return;
      // Configurar la velocidad de desplazamiento
      const speed = 1; // Ajusta la velocidad del desplazamiento
      container.scrollTop += speed;
      // Si llega al final, reinicia el scroll al principio
      if (
        container.scrollTop >=
        container.scrollHeight - container.clientHeight
      ) {
        container.scrollTop = 0;
        console.log("Scroll al final, reiniciando al principio.");
      }
    };

    onMounted(async () => {
      await loadProductosBBDD(20);

      nextTick(() => {
        const container = scrollContainer.value;

        // Duplica contenido una vez si es necesario
        if (container.scrollHeight <= container.clientHeight) {
          posts.value = [...posts.value, ...posts.value]; // Duplica una vez
          console.log("Contenido duplicado para scroll infinito.");
        } else {
          console.log("No se requiere duplicar el contenido.");
        }
      });
      fetchInterval = setInterval(() => {
        loadProductosBBDD(20);
      }, 30000);

      // Inicia el auto-scroll
      scrollInterval = setInterval(autoScroll, 30);
    });

    onUnmounted(() => {
      // Limpia el intervalo para evitar fugas de memoria
      if (scrollInterval) {
        clearInterval(scrollInterval);
        scrollInterval = null;
      }
      if (fetchInterval) {
        clearInterval(fetchInterval);
        fetchInterval = null;
      }
    });

    return {
      posts,
      loading,
      scrollContainer,
      panel,
contenedor
    };
  },
};
</script>

<style scoped>
.scrolling-component {
  max-width: 600px;
  margin: 0 auto;
  padding: 1em;
  overflow-y: auto; /* Enables vertical scrolling */
  max-height: 500px; /* Limits height to make scrolling visible */
  border: 1px solid #ddd; /* Optional styling */
  border-radius: 8px;
}

.post {
  margin: 10px 0;
  text-align: center;
}

.post img {
  width: 100px;
  height: auto;
  margin-bottom: 10px;
}

.loading-message {
  text-align: center;
  font-size: 1.5em;
  color: gray;
}
.q-drawer__content.fit.scroll {
  overflow: hidden !important; /* Oculta las barras de desplazamiento */
}
</style>
