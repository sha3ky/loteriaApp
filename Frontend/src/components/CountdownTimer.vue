<template>
  <div v-if="configuracion.fecha_final_countdown">
    <div style="display: flex; justify-content: center; margin-bottom: 50px">
      <p style="color: aliceblue; position: absolute">
        {{
          configuracion.texto_countdown ||
          "Empezamos la cuenta atras. Gracias por la paciencia..."
        }}
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
  </div>
  <!--  <div>
    <button
      v-if="configuracion.mostrar_boton_demo"
      class="demo-btn"
      :style="{ backgroundColor: configuracion.color_principal }"
    >
      {{ configuracion.texto_boton_demo || "Modo Demo" }}
    </button>
  </div> -->
</template>

<script>
// CountdownTimer.vue - Adaptado
import { ref, onMounted, onUnmounted, computed } from "vue";
import { api } from "boot/axios";
export default {
  name: "CountdownTimer",
  emits: ["countdown-finished", "countdown-extending"], // ✅ Declarar el emit

  setup(props, { emit }) {
    const configuracion = ref({});
    const days = ref(0);
    const hours = ref(0);
    const minutes = ref(0);
    const seconds = ref(0);
    let countdownInterval = null;
    // Cargar configuración del cliente
    const cargarConfiguracion = async () => {
      try {
        const response = await api.get("/api/configuracion-cliente/");
        configuracion.value = response.data;
      } catch (error) {
        console.error("❌ Error completo:", error.response?.data);
        // Muestra el mensaje específico del backend
      }
    };

    const targetDate = computed(() => {
      if (!configuracion.value.fecha_final_countdown) return null;

      const fechaStr = configuracion.value.fecha_final_countdown;
      const match = fechaStr.match(/^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})/);

      if (match) {
        const [_, year, month, day, targetHours, targetMinutes] = match;

        // ✅ Forzar la hora EXACTA ignorando zona horaria
        const targetDate = new Date();
        targetDate.setFullYear(parseInt(year));
        targetDate.setMonth(parseInt(month) - 1);
        targetDate.setDate(parseInt(day));
        targetDate.setHours(parseInt(targetHours)); // ← 11
        targetDate.setMinutes(parseInt(targetMinutes)); // ← 33
        targetDate.setSeconds(0);
        targetDate.setMilliseconds(0);

        // ✅ RESTAR 2 horas manualmente para compensar
        targetDate.setHours(targetDate.getHours() - 2);

        console.log("✅ Hora objetivo:", `${targetHours}:${targetMinutes}`);
        console.log("✅ Fecha FINAL (corregida):", targetDate);
        console.log(
          "✅ getHours() después de corrección:",
          targetDate.getHours()
        );

        return targetDate.getTime();
      }

      return null;
    });

    const updateCountdown = () => {
      if (!targetDate.value) {
        console.log("❌ No hay targetDate");
        return;
      }

      const now = new Date().getTime();
      const distance = targetDate.value - now;

      console.log("🕒 Countdown - distancia:", distance);

      if (distance <= 0) {
        console.log("⏰ Countdown terminado o en negativo");

        days.value = 0;
        hours.value = 0;
        minutes.value = 0;
        seconds.value = 0;

        // ✅ VERIFICAR SI HAY EXTENSIÓN CONFIGURADA
        if (configuracion.value.horas_extension_countdown > 0) {
          console.log("🔄 Countdown terminado - APLICANDO EXTENSIÓN");

          // ✅ CALCULAR NUEVA FECHA con la extensión
          const horasExtension = configuracion.value.horas_extension_countdown;
          const nuevaFecha = new Date();
          nuevaFecha.setHours(nuevaFecha.getHours() + horasExtension);

          // ✅ ACTUALIZAR la fecha en la configuración
          configuracion.value.fecha_final_countdown = nuevaFecha.toISOString();

          console.log(`⏰ Nueva fecha con extensión: ${nuevaFecha}`);

          // ✅ NO emitir finished=true porque se está extendiendo
          // ✅ NO limpiar el interval - que siga con la nueva fecha
        } else {
          // ✅ NO hay extensión - terminar definitivamente
          console.log("⏹️ Countdown terminado DEFINITIVAMENTE");
          emit("countdown-finished", true);

          /* if (countdownInterval) {
            clearInterval(countdownInterval);
            countdownInterval = null;
            console.log("🛑 Interval limpiado");
          } */
        }
      } else {
        // Countdown ACTIVO
        days.value = Math.floor(distance / (1000 * 60 * 60 * 24));
        hours.value = Math.floor(
          (distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
        );
        minutes.value = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        seconds.value = Math.floor((distance % (1000 * 60)) / 1000);
      }
    };

    onMounted(async () => {
      await cargarConfiguracion();
      updateCountdown();

      // ✅ Inicializar el interval
      countdownInterval = setInterval(updateCountdown, 1000);
    });
    onUnmounted(() => {
      // ✅ Limpiar interval al desmontar el componente
      if (countdownInterval) {
        clearInterval(countdownInterval);
      }
    });

    return {
      days,
      hours,
      minutes,
      seconds,
      configuracion,
    };
  },
};
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
