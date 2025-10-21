<!-- CountdownTimer.vue -->
<template>
  <div style="display: flex; justify-content: center; margin-bottom: 50px">
    <p style="color: aliceblue; position: absolute">
      Empezamos la cuenta atras. Gracias por la paciencia...
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
    <!-- <div class="time-block">
      <span>{{ miliseconds }}</span>
      <p>miliseconds</p>
    </div> -->
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from "vue";

export default {
  name: "CountdownTimer",
  setup() {
    const initialTargetDate = new Date("2025-12-21T06:17:00").getTime();
    const additionalTime = 2 * 60 * 60 * 1000; // 2 horas en milisegundos
    const targetDate = ref(initialTargetDate);
    // const fechaFinal=ref(false)
    const days = ref(0);
    const hours = ref(0);
    const minutes = ref(0);
    const seconds = ref(0);
    const fraseCuentaAtras = ref(false);
    let oneTimeLoop = true;
    const updateCountdown = () => {
      const now = new Date().getTime();
      const distance = targetDate.value - now; // Tiempo restante desde ahora

      if (distance <= 0 && oneTimeLoop == true) {
        // Reinicia la cuenta regresiva añadiendo 2 horas
        targetDate.value += additionalTime;
        ("añadir solo una vez dos horas");
        oneTimeLoop = false;
      } else if (oneTimeLoop != false) {
        // Actualiza los valores de tiempo restante
        days.value = Math.floor(distance / (1000 * 60 * 60 * 24));
        hours.value = Math.floor(
          (distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
        );
        minutes.value = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        seconds.value = Math.floor((distance % (1000 * 60)) / 1000);
      }
    };

    let countdownInterval;
    onMounted(() => {
      updateCountdown(); // Inicia el conteo al montar el componente
      countdownInterval = setInterval(updateCountdown, 1000); // Actualiza cada segundo
    });

    onUnmounted(() => {
      clearInterval(countdownInterval); // Limpia el intervalo al desmontar
    });

    return {
      days,
      hours,
      minutes,
      seconds,
      fraseCuentaAtras,
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
