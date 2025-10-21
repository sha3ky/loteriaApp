<template>
  <div v-if="configuracion.fecha_final_countdown">
    <div style="display: flex; justify-content: center; margin-bottom: 50px">
      <p style="color: aliceblue; position: absolute">
        {{ configuracion.texto_countdown || "Empezamos la cuenta atras. Gracias por la paciencia..." }}
      </p>
    </div>
    <div class="countdown">
      <div class="time-block" v-if="days > 0">
        <span>{{ days }}</span>
        <p>Días</p>
      </div>
      <div class="time-block" v-if="hours > 0">
        <span>{{ hours }}</span>
        <p>Horas</p>
      </div>
      <div class="time-block" v-if="minutes > 0">
        <span>{{ minutes }}</span>
        <p>Minutos</p>
      </div>
      <div class="time-block">
        <span>{{ seconds }}</span>
        <p>Segundos</p>
      </div>
    </div>
    
    <!-- Botón demo condicional -->
    <button 
      v-if="configuracion.mostrar_boton_demo" 
      class="demo-btn"
      :style="{ backgroundColor: configuracion.color_principal }"
    >
      {{ configuracion.texto_boton_demo || "Modo Demo" }}
    </button>
  </div>
</template>

<script>

// CountdownTimer.vue - Adaptado
import { ref, onMounted, onUnmounted, computed } from "vue";
import { api } from 'boot/axios';
export default {
  name: "CountdownTimer",
  setup() {
    const configuracion = ref({})
    const days = ref(0)
    const hours = ref(0)
    const minutes = ref(0)
    const seconds = ref(0)
    
    // Cargar configuración del cliente
 const cargarConfiguracion = async () => {
  try {
    // ✅ Usar axios - el token se agrega AUTOMÁTICAMENTE
    const response = await api.get('/api/configuracion-cliente/')
    configuracion.value = response.data // ← response.data con axios
    console.log("✅ Configuración cargada:", response.data)
  } catch (error) {
    console.error("❌ Error cargando configuración:", error)
  }
}
    const targetDate = computed(() => {
      return new Date(configuracion.value.fecha_final_countdown).getTime()
    })
    
    const updateCountdown = () => {
      if (!configuracion.value.fecha_final_countdown) return
      
      const now = new Date().getTime()
      const distance = targetDate.value - now

      if (distance <= 0) {
        // Extender countdown si está configurado
        if (configuracion.value.horas_extension_countdown) {
          // Lógica para extender (podría manejarse en backend)
        }
      } else {
        days.value = Math.floor(distance / (1000 * 60 * 60 * 24))
        hours.value = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
        minutes.value = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60))
        seconds.value = Math.floor((distance % (1000 * 60)) / 1000)
      }
    }

    onMounted(async () => {
      await cargarConfiguracion()
      if (configuracion.value.fecha_final_countdown) {
        setInterval(updateCountdown, 1000)
      }
    })

    return {
      days,
      hours,
      minutes,
      seconds,
      configuracion
    }
  }
}
</script>

<style scoped>
.countdown {
  display: flex;
  gap: 1em;
  justify-content: center;
  align-items: center;
  font-family: "Special Elite", monospace; /* Fuente de estilo antiguo */
  color: white;
}

.time-block {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.time-block span {
  font-size: 3em;
  color: white;
}

.time-block p {
  font-size: 1em;
  color: white;
  margin-top: -10px;
}
</style>
