<template>
  <div>
    <div style="background-color: black; padding: 5px; margin-bottom: 3px">
      <span style="color: white; font-weight: 700">
        Por favor, selecciona uno de los 50 números:
      </span>
    </div>

    <div class="square-grid">
      <div
        v-for="number in totalNumbers"
        :key="number"
        class="square"
        :class="{ green: isNumberGreen(number) }"
        @click="openDialog(number)"
      >
        {{ number }}
      </div>
    </div>
    <!-- Dialogo de Quasar -->
    <q-dialog v-model="isDialogOpen">
      <q-card>
        <q-card-section>
          <div class="text-h6">Reserva el Número {{ selectedNumber }}</div>
        </q-card-section>

        <q-card-section>
          <q-input v-model="formData.name" label="Nombre" outlined />
          <q-input v-model="formData.surname" label="Apellido" outlined />
          <q-input v-model="formData.phone" label="Teléfono" outlined />
          <q-input
            v-model="formData.email"
            label="Correo Electrónico"
            outlined
          />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="negative" @click="closeDialog" />
          <q-btn flat label="Enviar" color="positive" @click="submitForm" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from "vue";
import { api } from "boot/axios";
import { toRaw } from "vue";
import { Notify } from "quasar";
export default {
  name: "NumbersSquares",

  setup() {
    const totalNumbers = Array.from({ length: 50 }, (_, i) => i + 1); // Genera [1, 2, ..., 99]
    const selectedNumber = ref(null);
    const isDialogOpen = ref(false);
    const formData = ref({
      name: "",
      surname: "",
      phone: "",
      email: "",
    });

    const status = ref({});

    // Actualizar el estado cada cierto tiempo
    const updateInterval = 5000; // 5 segundos
    let intervalId = null;

    const fetchStatusUpdate = async () => {
      try {
        // ✅ Usar axios en lugar de apiCall
        const response = await api.get("/api/number-status/");
        // Con axios, response.ok no existe - la respuesta viene directamente
        const updatedStatus = response.data; // ← Los datos vienen en .data
        status.value = updatedStatus;
      } catch (error) {
        console.error("🚨 Error al actualizar el estado:", error);

        // Manejo de errores con axios
        if (error.response) {
          // El servidor respondió con un código de error
          console.error("❌ Error del servidor:", error.response.data);
        } else if (error.request) {
          // La request se hizo pero no hubo respuesta
          console.error("❌ Error de red:", error.request);
        } else {
          // Algo pasó en la configuración
          console.error("❌ Error:", error.message);
        }
      }
    };

    // Inicia la actualización periódica
    onMounted(() => {
      fetchStatusUpdate(); // Llamada inicial
      intervalId = setInterval(fetchStatusUpdate, updateInterval);
    });

    // Limpia el intervalo cuando el componente se desmonta
    onUnmounted(() => {
      if (intervalId) clearInterval(intervalId);
    });

    // Función para abrir el diálogo
    const openDialog = (number) => {
      if (isNumberGreen(number)) {
        // console.log("Estado actual:", toRaw(status.value));
        const toRawStatus = toRaw(status.value);
        const filteredStatus = Object.values(toRawStatus).find(
          (value) => value.numero === number
        );

        const nombreCompleto = filteredStatus?.nombre_completo || "desconocido";

        Notify.create({
          message: `Este número está asignado a ${nombreCompleto} !`,
          color: "positive", // Cambia a 'negative', 'warning', etc.
          position: "bottom", // Puede ser 'top', 'bottom', 'left', 'right', 'top-left', etc.
          timeout: 3000, // Tiempo en milisegundos antes de desaparecer automáticamente
        });
        isDialogOpen.value = false; // Asegura que el diálogo no se abra
      } else {
        selectedNumber.value = number;
        isDialogOpen.value = true;
      }
    };

    // Función para cerrar el diálogo
    const closeDialog = () => {
      isDialogOpen.value = false;
      resetForm();
    };

    // Función para manejar el envío del formulario
    const submitForm = async () => {
      if (!formData.value.phone && !formData.value.email) {
        Notify.create({
          message: "Por favor, proporciona un teléfono o correo electrónico.",
          color: "negative",
          timeout: 3000, // Se oculta automáticamente después de 3 segundos
        });
        return;
      }
      debugger;
      const payload = {
        number: selectedNumber.value,
        name: formData.value.name,
        surname: formData.value.surname,
        phone: formData.value.phone,
        email: formData.value.email,
      };

      try {
        const response = await api.post("/api/reserve-number/", payload);

        if (response.data.message) {
          Notify.create({
            message: "Número reservado exitosamente.",
            color: "positive",
            timeout: 3000,
          });
          fetchStatusUpdate(); // Actualizar el estado tras reservar
        } else {
          Notify.create({
            message: "Hubo un error al reservar el número.",
            color: "negative",
            timeout: 3000,
          });
        }
      } catch (error) {
        console.error("Error al enviar los datos:", error);
        Notify.create({
          message: "No se pudo conectar con el servidor.",
          color: "negative",
          timeout: 3000,
        });
      } finally {
        closeDialog();
      }
    };

    // Función para reiniciar el formulario
    const resetForm = () => {
      formData.value = {
        name: "",
        surname: "",
        phone: "",
        email: "",
      };
    };

    // Determina si el número está en estado "green"
    const isNumberGreen = (numero) => {
      // Iterar por cada clave en el objeto status
      for (const key in status.value) {
        if (status.value[key]?.numero === numero) {
          // Si el número coincide y su estado es "green", devuelve true
          return status.value[key]?.status === "green";
        }
      }
      // Si no se encuentra el número, devuelve false
      return false;
    };

    return {
      totalNumbers,
      selectedNumber,
      isDialogOpen,
      formData,
      openDialog,
      closeDialog,
      submitForm,
      isNumberGreen,
    };
  },
};
</script>

<style scoped>
/* Contenedor de la cuadrícula */
.square-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(50px, 1fr));
  gap: 4px;
  width: 100%;
  height: 100%;
}

/* Estilos de los cuadrados */
.square {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #5a575796;
  color: white;
  font-size: 1rem;
  font-weight: bold;
  aspect-ratio: 1 / 1;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.square.green {
  background-color: #008000d1;
}

.q-dialog {
  max-width: 400px;
  width: 90%;
}
</style>
