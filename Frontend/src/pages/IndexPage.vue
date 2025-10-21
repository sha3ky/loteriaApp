<template>
  <q-page class="page-container" style="min-height: 70vh">
    <div class="background-blur"></div>
    <div>
      <CountdownTimer />
    </div>
    <div style="height: 45vh; width: 45vh">
      <VueWheelSpinner
        ref="spinner"
        :slices="slices"
        :winner-index="defaultWinner"
        :sounds="sounds"
        :cursor-angle="cursorAngle"
        :cursor-position="cursorPosition"
        :cursor-distance="cursorDistance"
        @spin-start="onSpinStart"
        @spin-end="onSpinEnd"
      >
        <template #cursor>
          <img class="cursor-img" :src="cursorImage" alt="Cursor" />
        </template>
        <!-- style="position: fixed; bottom: -2.5vh; right: -30px; z-index: 9999" -->
        <template #default>
          <q-btn
            class="glossy spin-button"
            rounded
            color="deep-orange"
            label="Demo"
            :disabled="isSpinning"
            @click="handleSpinButtonClick"
            @mouseover="handleSpinButtonHover"
            @mouseleave="handleSpinButtonLeave"
            size="lg"
          />
        </template>
      </VueWheelSpinner>
    </div>
    <div style="display: contents">
      <!-- Placeholder invisible -->
      <h4
        v-if="winnerResult === null"
        style="
          font-size: 1.125rem;
          font-weight: 400;
          line-height: 0rem;
          letter-spacing: 0em;
          color: white;
          visibility: hidden; /* Invisible placeholder */
        "
      >
        Número ganador:
      </h4>

      <!-- Visible solo si hay un número ganador -->
      <h4
        v-else
        style="
          font-size: 1.125rem;
          font-weight: 400;
          line-height: 0rem;
          letter-spacing: 0em;
          color: white;
        "
      >
        Número ganador:
      </h4>

      <!-- Número ganador o marcador de posición -->
      <div>
        <h5 style="padding: 0px; margin: 0px; color: gold">
          <span
            style="font-weight: 700; visibility: hidden"
            v-if="winnerResult === null || winnerResult === undefined"
          >
            Placeholder text
          </span>
          <span style="font-weight: 700; color: gold" v-else>
            {{ winnerResult.text }}
          </span>
        </h5>
      </div>
    </div>
    <ConfettiAnimation :showConfetti="showConfetti" />

    <div class="q-pa-md q-gutter-sm">
      <!-- para testear solo -->

      <q-dialog
        v-model="isDialogOpen"
        persistent
        transition-show="scale"
        transition-hide="scale"
        class="custom-dialog"
      >
        <q-card class="text-white dialog-card">
          <q-card-section class="dialog-content">
            <div v-if="nombreGanador" class="winner-section">
              <div class="text-h6 winner-title">
                La ganadora o el Ganador es {{ nombreGanador }}
              </div>
              <div class="sign-container">
                <div class="sign">
                  <span class="fast-flicker">Fe</span>lic<span class="flicker">id</span>ad<span class="fast-flicker">es</span>
                </div>
              </div>
            </div>
            <div v-else class="try-again-section">
              <div class="text-h6 try-again-title">
                Vuelve a probar otra vez. Sin número asignado.
              </div>
            </div>
          </q-card-section>
          
          <q-card-actions align="center" class="dialog-actions bg-white text-teal">
            <q-btn flat label="Cerrar" v-close-popup class="close-btn" />
          </q-card-actions>
        </q-card>
      </q-dialog>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, onMounted, watch } from "vue";
import VueWheelSpinner from "../components/VueWheelSpinner.vue";
import cursorImage from "../icons/arrow_drop2.png";
// import flecha from "../icons/flecha.png";

import CountdownTimer from "../components/CountdownTimer.vue";
import { slices as importedSlices } from "../variosJs/slices.js";
import fondoImagen from "../images/fondo.jpg";
import ConfettiAnimation from "../components/ConfettiAnimation.vue";

import wonSound from "../sounds/winning2.wav";
import loseSound from "../sounds/lose.wav";
import clickSound from "../sounds/click.wav";
import hoverSound from "../sounds/hover.wav";
import leaveSound from "../sounds/hover.wav";
import spinningSound from "../sounds/spinning2.wav";

export default defineComponent({
  name: "IndexPage",
  components: {
    VueWheelSpinner,
    CountdownTimer,
    ConfettiAnimation,
  },
  setup() {
    const isDialogOpen = ref(false);
    const nombreGanador = ref("");
    const winnerResult = ref(null);
    const slices = ref(importedSlices); // Convertido a ref para evitar errores
    const isSpinning = ref(false);
    const defaultWinner = ref(0);
    const cursorAngle = ref(0);
    const cursorPosition = ref("center");
    const cursorDistance = ref(130);
    const spinner = ref(null);
    const showConfetti = ref(false);

    // Creamos instancias de Audio para cada sonido en onMounted
    const sounds = ref({
      won: null,
      spinButtonClick: null,
      spinButtonHover: null,
      spinButtonLeave: null,
      spinning: null,
    });

    watch(winnerResult, async (newValue) => {
      
     /*  showConfetti.value = newValue !== null; */
      // miramos el newValue y si no es vacio llamamos al nombre del ganador
      if (newValue !== null) {
        await searchWinner(); // Llamar a la función asíncrona aquí
      }
    });

    const handleSpinButtonClick = () => {
      
      stopAllSounds(); // Detener todos los sonidos antes de iniciar el giro
      if (
        !isSpinning.value &&
        spinner.value &&
        typeof spinner.value.spinWheel === "function"
      ) {
        isSpinning.value = true;
        showConfetti.value = false;
        playAudio(sounds.value.spinButtonClick); // Reproduce el sonido de click
        defaultWinner.value = Math.floor(Math.random() * 50) + 1;
        // defaultWinner.value = 5;
        console.log("defaultWinner.value", defaultWinner.value);
        spinner.value.spinWheel(defaultWinner.value);
      }
    };

    // Función para detener todos los sonidos
    const stopAllSounds = () => {
      for (const key in sounds.value) {
        const audio = sounds.value[key];
        if (audio) {
          audio.pause();
          audio.currentTime = 0;
        }
      }
    };

    const searchWinner = async () => {
      
       nombreGanador.value=""
      try {
        // para testear solo

        const response = await fetch(
          `${BASE_URL}/api/get-winner/${winnerResult.value.text}/`
        );

        if (response.ok) {
          const winner = await response.json();
          nombreGanador.value = winner.nombre_completo;
          isDialogOpen.value = true;
       
        // Reproduce el sonido de winning
        playAudio(sounds.value.won);
        // Muestra confetti mientras suena el audio de winning
        showConfetti.value = true;
        // Escucha cuando el sonido de 'won' termina y luego apaga el confetti
        sounds.value.won.onended = () => {
          showConfetti.value = false;
        };
        } else {
          console.error("Error al obtener el estado de los números.");
          isDialogOpen.value = true;
          playAudio(sounds.value.lose);
        }
      } catch (error) {
        console.error("Error al actualizar el estado:", error);
      }
    };

    const handleSpinButtonHover = () => playAudio(sounds.value.spinButtonHover);
    const handleSpinButtonLeave = () => playAudio(sounds.value.spinButtonLeave);

    const onSpinStart = () => {
      winnerResult.value = null;
      isSpinning.value = true;
      playAudio(sounds.value.spinning); // Inicia el sonido de "spinning"
    };

    const onSpinEnd = (winnerIndex) => {
      
      console.log("onspinEnd", winnerIndex);
      // Detener el sonido de spinning antes de reproducir el sonido de winning
      if (sounds.value.spinning) {
        stopAudio(sounds.value.spinning);
      }
      // Configura el ganador y termina el giro
      isSpinning.value = false;
      winnerResult.value = slices.value[winnerIndex];
    };
    // Función para detener un audio específico
    const stopAudio = (audio) => {
      if (audio) {
        audio.pause();
        audio.currentTime = 0;
      }
    };

    const playAudio = (audio) => {
      if (audio) {
        audio.volume = 0.5; // volumen sonido
        audio.play();
      }
    };

    onMounted(() => {
      // Inicializa las instancias de Audio cuando el componente está montado
      sounds.value.won = new Audio(wonSound);
      sounds.value.spinButtonClick = new Audio(clickSound);
      sounds.value.spinButtonHover = new Audio(hoverSound);
      sounds.value.spinButtonLeave = new Audio(leaveSound);
      sounds.value.spinning = new Audio(spinningSound);
      sounds.value.lose=new Audio(loseSound)
    });

    return {
      searchWinner,
      isDialogOpen,
      nombreGanador,
      winnerResult,
      slices,
      isSpinning,
      defaultWinner,
      sounds,
      cursorImage,
      cursorAngle,
      cursorPosition,
      cursorDistance,
      handleSpinButtonClick,
      handleSpinButtonHover,
      handleSpinButtonLeave,
      onSpinStart,
      onSpinEnd,
      spinner,
      fondoImagen, // Referencia a spinner para acceder a su método spinWheel
      showConfetti,
    };
  },
});
</script>

<style scoped>
/* Contenedor principal */

/* .custom-dialog {
  background-image: url("../images/hearts.jpg") no-repeat center center;
  background-size: cover;
} */

/* .dialog-card {
  width: 80vh;
  height: 70vh;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(10px);
  border-radius: 15px;
} */

html,
body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow: hidden; /* Evita el desplazamiento adicional */
}
.q-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between; /* Ajusta el contenido */
  height: 100vh; /* Ocupa toda la pantalla */
  margin: 0;
  padding: 0;
  overflow: hidden; /* Evita el desplazamiento adicional */
}
/* recien cambiado */
.dialog-card {
  width: min(80vh, 90vw); /* Responsive */
  max-width: 500px; /* Límite máximo */
  min-height: min(50vh, 60vw); /* Responsive */
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* Separa contenido y botones */
}

.dialog-content {
  flex: 1; /* Ocupa el espacio disponible */
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 20px;
}

.winner-section, .try-again-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  flex: 1;
}

.winner-title, .try-again-title {
  text-transform: uppercase;
  margin-bottom: 20px;
  word-wrap: break-word;
}

.sign-container {
  position: relative;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 20px 0;
}

.sign {
  display: flex;
  justify-content: center;
  align-items: center;
  width: auto;
  height: auto;
  background-image: radial-gradient(
    ellipse 50% 35% at 50% 50%,
    #6b1839,
    transparent
  );
  letter-spacing: 2px;
  font-family: "Clip";
  text-transform: uppercase;
  font-size: clamp(1.5em, 4vw, 3em); /* Responsive */
  color: #ffe6ff;
  text-shadow: 0 0 0.6rem #ffe6ff, 0 0 1.5rem #ff65bd,
    -0.2rem 0.1rem 1rem #ff65bd, 0.2rem 0.1rem 1rem #ff65bd,
    0 -0.5rem 2rem #ff2483, 0 0.5rem 3rem #ff2483;
  animation: shine 2s forwards, flicker 3s infinite;
  padding: 10px;
}

.dialog-actions {
  padding: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
}

.close-btn {
  min-width: 120px;
}

/* Media queries para mejor responsividad */
@media (max-width: 600px) {
  .dialog-card {
    width: 90vw;
    min-height: 50vh;
  }
  
  .sign {
    font-size: 1.8em;
  }
  
  .winner-title, .try-again-title {
    font-size: 1.1em;
  }
}

@media (max-width: 400px) {
  .sign {
    font-size: 1.5em;
  }
  
  .dialog-content {
    padding: 15px;
  }
}
.page-container {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 100%;
}

/* Fondo difuminado */
.background-blur {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("../images/fondo.jpg");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  filter: blur(5px);
  z-index: -1; /* Siempre detrás del contenido */
}

/* Estilos para centrar contenido */
.flex-center {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%; /* Centrado vertical */
}

.column {
  flex-direction: column;
}
.box {
  background: red;

  animation: colorFade 6s infinite; /* Smooth, continuous color change */
  cursor: pointer;
}

@keyframes colorFade {
  0% {
    background-color: red;
  }
  20% {
    background-color: orange;
  }
  40% {
    background-color: yellow;
  }
  60% {
    background-color: green;
  }
  80% {
    background-color: blue;
  }
  100% {
    background-color: red;
  }
}
/* .sign {
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: baseline;
  width: 50%;
  height: 50%;
  background-image: radial-gradient(
    ellipse 50% 35% at 50% 50%,
    #6b1839,
    transparent
  );
  transform: translate(-50%, -50%);
  letter-spacing: 2;
  left: 50%;
  top: 50%;
  font-family: "Clip";
  text-transform: uppercase;
  font-size: 3em;
  color: #ffe6ff;
  text-shadow: 0 0 0.6rem #ffe6ff, 0 0 1.5rem #ff65bd,
    -0.2rem 0.1rem 1rem #ff65bd, 0.2rem 0.1rem 1rem #ff65bd,
    0 -0.5rem 2rem #ff2483, 0 0.5rem 3rem #ff2483;
  animation: shine 2s forwards, flicker 3s infinite;
  margin-top: 2%;
} */

@keyframes blink {
  0%,
  22%,
  36%,
  75% {
    color: #ffe6ff;
    text-shadow: 0 0 0.6rem #ffe6ff, 0 0 1.5rem #ff65bd,
      -0.2rem 0.1rem 1rem #ff65bd, 0.2rem 0.1rem 1rem #ff65bd,
      0 -0.5rem 2rem #ff2483, 0 0.5rem 3rem #ff2483;
  }
  28%,
  33% {
    color: #ff65bd;
    text-shadow: none;
  }
  82%,
  97% {
    color: #ff2483;
    text-shadow: none;
  }
}

.flicker {
  animation: shine 2s forwards, blink 3s 2s infinite;
}

.fast-flicker {
  animation: shine 2s forwards, blink 10s 1s infinite;
}

@keyframes shine {
  0% {
    color: #6b1839;
    text-shadow: none;
  }
  100% {
    color: #ffe6ff;
    text-shadow: 0 0 0.6rem #ffe6ff, 0 0 1.5rem #ff65bd,
      -0.2rem 0.1rem 1rem #ff65bd, 0.2rem 0.1rem 1rem #ff65bd,
      0 -0.5rem 2rem #ff2483, 0 0.5rem 3rem #ff2483;
  }
}

@keyframes flicker {
  from {
    opacity: 1;
  }

  4% {
    opacity: 0.9;
  }

  6% {
    opacity: 0.85;
  }

  8% {
    opacity: 0.95;
  }

  10% {
    opacity: 0.9;
  }

  11% {
    opacity: 0.922;
  }

  12% {
    opacity: 0.9;
  }

  14% {
    opacity: 0.95;
  }

  16% {
    opacity: 0.98;
  }

  17% {
    opacity: 0.9;
  }

  19% {
    opacity: 0.93;
  }

  20% {
    opacity: 0.99;
  }

  24% {
    opacity: 1;
  }

  26% {
    opacity: 0.94;
  }

  28% {
    opacity: 0.98;
  }

  37% {
    opacity: 0.93;
  }

  38% {
    opacity: 0.5;
  }

  39% {
    opacity: 0.96;
  }

  42% {
    opacity: 1;
  }

  44% {
    opacity: 0.97;
  }

  46% {
    opacity: 0.94;
  }

  56% {
    opacity: 0.9;
  }

  58% {
    opacity: 0.9;
  }

  60% {
    opacity: 0.99;
  }

  68% {
    opacity: 1;
  }

  70% {
    opacity: 0.9;
  }

  72% {
    opacity: 0.95;
  }

  93% {
    opacity: 0.93;
  }

  95% {
    opacity: 0.95;
  }

  97% {
    opacity: 0.93;
  }

  to {
    opacity: 1;
  }
}
</style>
