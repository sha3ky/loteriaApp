<template>
  <div class="confetti-container" v-if="showConfetti">
    <div
      v-for="(confetti, index) in confettiItems"
      :key="index"
      :style="{ '--speed': confetti.speed, '--bg': confetti.color }"
      :class="confetti.shape"
    ></div>
  </div>
</template>

<script>
import { ref, watch } from "vue";

export default {
  name: "ConfettiAnimation",
  props: {
    showConfetti: {
      type: Boolean,
      required: true,
    },
  },
  setup(props) {
    const confettiItems = ref([]);
    let confettiTimeout = null;
    // Genera el confeti cuando `showConfetti` cambia a true
    watch(
      () => props.showConfetti,
      (newVal) => {
        if (newVal) {
          // Genera los elementos de confeti
          confettiItems.value = Array.from({ length: 100 }, () => ({
            speed: Math.floor(Math.random() * 50) + 10,
            color: getRandomColor(),
            shape: getRandomShape(),
          }));

          // Detiene el confeti después de 15 segundos
          if (confettiTimeout) {
            clearTimeout(confettiTimeout); // Limpia el temporizador anterior si existe
          }

          confettiTimeout = setTimeout(() => {
            confettiItems.value = []; // Limpia el confeti
          }, 15000); // 15 segundos
        } else {
          // Limpia inmediatamente si se desactiva `showConfetti`
          confettiItems.value = [];
          if (confettiTimeout) {
            clearTimeout(confettiTimeout);
            confettiTimeout = null;
          }
        }
      },
      { immediate: true }
    );
    function getRandomColor() {
      const colors = [
        "yellow",
        "white",
        "green",
        "blue",
        "red",
        "pink",
        "purple",
        "cyan",
      ];
      return colors[Math.floor(Math.random() * colors.length)];
    }

    function getRandomShape() {
      const shapes = [
        "square",
        "rectangle",
        "hexagram",
        "pentagram",
        "dodecagram",
        "wavy-line",
      ];
      return shapes[Math.floor(Math.random() * shapes.length)];
    }

    return { confettiItems };
  },
};
</script>

<style scoped>
.confetti-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  pointer-events: none;
  overflow: hidden;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-evenly;
  user-select: none;
  z-index: 10;
}

/* Estilos para cada tipo de confeti */

.square {
  width: 1rem;
  height: 1rem;
  background-color: var(--bg);
  animation: confettiFall calc(60s / var(--speed)) linear infinite;
}

.rectangle {
  width: 1rem;
  height: 0.5rem;
  background-color: var(--bg);
}

.hexagram {
  width: 0;
  height: 0;
  border-left: 0.5rem solid transparent;
  border-right: 0.5rem solid transparent;
  border-bottom: 1rem solid var(--bg);
  position: relative;
}

.hexagram:after {
  content: "";
  width: 0;
  height: 0;
  border-left: 0.5rem solid transparent;
  border-right: 0.5rem solid transparent;
  border-top: 1rem solid var(--bg);
  position: absolute;
  top: 0.33rem;
  left: -0.5rem;
}

.pentagram {
  width: 0;
  height: 0;
  display: block;
  border-right: 1rem solid transparent;
  border-bottom: 0.7rem solid var(--bg);
  border-left: 1rem solid transparent;
  transform: rotate(35deg);
  position: relative;
}

.pentagram:before {
  content: "";
  width: 0;
  height: 0;
  border-bottom: 0.8rem solid var(--bg);
  border-left: 0.3rem solid transparent;
  border-right: 0.3rem solid transparent;
  transform: rotate(-35deg);
  position: absolute;
  top: -0.45rem;
  left: -0.65rem;
}

.pentagram:after {
  content: "";
  width: 0rem;
  height: 0rem;
  border-right: 1rem solid transparent;
  border-bottom: 0.7rem solid var(--bg);
  border-left: 1rem solid transparent;
  transform: rotate(-70deg);
  position: absolute;
  top: 0.03rem;
  left: -1.05rem;
}

.dodecagram {
  width: 0.8rem;
  height: 0.8rem;
  background-color: var(--bg);
  position: relative;
}

.dodecagram:before {
  content: "";
  height: 0.8rem;
  width: 0.8rem;
  background-color: var(--bg);
  transform: rotate(30deg);
  position: absolute;
  top: 0;
  left: 0;
}

.dodecagram:after {
  content: "";
  height: 0.8rem;
  width: 0.8rem;
  background-color: var(--bg);
  transform: rotate(60deg);
  position: absolute;
  top: 0;
  left: 0;
}

.wavy-line {
  position: relative;
  width: 0.5rem;
  height: 0.5rem;
  background-color: var(--bg);
  animation: confettiFall calc(60s / var(--speed)) linear infinite;
}

/* Animación de caída de confeti */
.confetti-container div {
  animation: confettiFall calc(60s / var(--speed)) linear infinite;
}

@keyframes confettiFall {
  0% {
    transform: translateY(-100vh);
  }
  100% {
    transform: translateY(100vh);
  }
}
</style>
