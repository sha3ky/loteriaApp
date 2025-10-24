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
      <div class="time-block" v-if="seconds > 0">
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
    const hasEmittedFinished = ref(false);
    const isExtended = ref(false);
    // Cargar configuración del cliente
    const cargarConfiguracion = async () => {
      try {
        const response = await api.get("/api/configuracion-cliente/");
        configuracion.value = response.data;
        console.log("configuracion.value", configuracion.value);
      } catch (error) {
        console.error("❌ Error completo:", error.response?.data);
        // Muestra el mensaje específico del backend
      }
    };

    const targetDate = computed(() => {
      // Si no hay configuración o no hay fecha de countdown, retornamos null.
      if (!configuracion.value || !configuracion.value.fecha_final_countdown) {
        return null;
      }

      const fechaStrOriginal = configuracion.value.fecha_final_countdown;

      // Extraemos los componentes de la fecha y hora de la cadena ISO 8601.
      // Asumimos el formato "YYYY-MM-DDTHH:mm:ss+00:00" o similar,
      // extrayendo las partes clave con substring.
      const year = parseInt(fechaStrOriginal.substring(0, 4));
      const month = parseInt(fechaStrOriginal.substring(5, 7));
      const day = parseInt(fechaStrOriginal.substring(8, 10));
      const hours = parseInt(fechaStrOriginal.substring(11, 13));
      const minutes = parseInt(fechaStrOriginal.substring(14, 16));
      // Los segundos se pueden extraer si están presentes, o fijar a 0 si no son críticos
      // Para tu cadena "2025-10-23T16:12:00+00:00", los segundos son "00"
      const seconds = parseInt(fechaStrOriginal.substring(17, 19) || "0");

      // Construimos la marca de tiempo UTC utilizando Date.UTC().
      // Es crucial restar 1 al mes porque JavaScript los indexa desde 0 (Enero=0, Octubre=9).
      const timestampUTC = Date.UTC(
        year,
        month - 1, // Meses son 0-indexados en JavaScript
        day,
        hours,
        minutes,
        seconds
      );

      // Opcional: Para una inspección rápida en desarrollo, puedes descomentar estas líneas.
      // const finalDateFromTimestamp = new Date(timestampUTC);
      // console.log("Fecha FINAL calculada (UTC):", finalDateFromTimestamp.toUTCString());
      // console.log("Marca de tiempo FINAL (ms):", timestampUTC);

      return timestampUTC;
    });

    const updateCountdown = () => {
      if (!targetDate.value) {
        console.log(
          "❌ No hay targetDate.value. La configuración podría no haber cargado o es inválida."
        );
        // Podrías decidir si limpiar el interval aquí o esperar. Por ahora, solo salimos.
        return;
      }

      const now = new Date().getTime(); // Momento actual en ms
      let distance = targetDate.value - now; // Distancia restante al targetDate

      if (distance <= 0) {
        // --- COUNTDOWN TERMINADO ---
        days.value = 0;
        hours.value = 0;
        minutes.value = 0;
        seconds.value = 0;

        // ✅ Lógica para EXTENDER UNA SOLA VEZ
        // Se ejecuta si hay horas de extensión Y aún no se ha extendido
        if (
          configuracion.value.horas_extension_countdown > 0 &&
          !isExtended.value
        ) {
          console.log("🔄 Countdown terminado - APLICANDO EXTENSIÓN UNA VEZ");

          const horasExtension = configuracion.value.horas_extension_countdown;

          // Calculamos la nueva fecha sumando las horas de extensión al targetDate original.
          const nuevaMarcaTiempoExtendida =
            targetDate.value + horasExtension * 60 * 60 * 1000;
          const nuevaFechaExtendida = new Date(nuevaMarcaTiempoExtendida);

          configuracion.value.fecha_final_countdown =
            nuevaFechaExtendida.toISOString();

          isExtended.value = true; // Marcamos que ya se extendió

          console.log(
            `⏰ Nueva fecha con extensión: ${nuevaFechaExtendida.toISOString()}`
          );

          // IMPORTANTE: NO hacemos 'emit' ni limpiamos el interval aquí.
          // El countdown ahora se reanuda con la nueva fecha extendida.
        } else {
          // ✅ CONDICIÓN FINAL DE TERMINACIÓN:
          // Esto se ejecuta si:
          // 1. No hay extensión configurada
          // 2. O ya se extendió una vez y la extensión TAMBIÉN ha terminado (distance <= 0 nuevamente)

          if (!hasEmittedFinished.value) {
            // Solo emitimos si no lo hemos hecho ya
            console.log(
              "⏹️ Countdown terminado DEFINITIVAMENTE. Emitiendo evento."
            );
            emit("countdown-finished", true);
            hasEmittedFinished.value = true; // Marcamos que ya se emitió el evento final.
          }

          // ✅ Limpiar el interval SOLO cuando se ha terminado definitivamente y se ha emitido el evento
          if (countdownInterval) {
            clearInterval(countdownInterval);
            countdownInterval = null;
            console.log("🛑 Interval limpiado (final definitivo)");
          }
        }
      } else {
        // --- COUNTDOWN ACTIVO ---
        // Si la distancia es positiva, el countdown está funcionando.
        // Aseguramos que las banderas de control estén en estado de "no terminado/no extendido" si es necesario.
        if (isExtended.value) {
          // Si el countdown se puso activo de nuevo (ej. se extendió y se está contando)
          isExtended.value = false; // Resetear para permitir futuras extensiones si la configuración cambia o se resetea.
        }
        if (hasEmittedFinished.value) {
          hasEmittedFinished.value = false; // Resetear si el countdown vuelve a estar activo (raro, pero previene problemas)
        }

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
      if (!configuracion.value.mostrar_boton_demo) {
        updateCountdown();
        countdownInterval = setInterval(updateCountdown, 1000);
      }

      // ✅ Inicializar el interval
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
