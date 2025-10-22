<template>
  <q-layout view="hHh lpR fFf">
    <q-header
      v-if="layoutStore.showToolbar"
      elevated
      class="bg-purple-3 text-white"
    >
      <q-toolbar>
        <q-btn
          dense
          flat
          round
          icon="card_giftcard"
          @click="toggleLeftDrawer"
          size="xl"
        />

        <q-toolbar-title class="flex flex-center" style="padding: 10px">
          <q-img
            src="/icons/bingo.png"
            style="height: 70px; max-width: 60px"
            @click="handleClick()"
          />
        </q-toolbar-title>

        <q-btn
          dense
          flat
          round
          icon="apps"
          @click="toggleRightDrawer"
          size="xl"
        />
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      side="left"
      behavior="mobile"
      elevated
      style="width: 50vh"
    >
      <div style="justify-content: flex-end; display: flex; padding: 10px">
        <q-btn
          outline
          round
          color="alert"
          icon="close"
          @click="closeLeftDrawer"
        />
      </div>

      <q-list>
        <q-item-label header>
          <h5 style="padding: 0; margin: 0; text-align: center">
            Cesta de Regalos
          </h5>
        </q-item-label>
        <InfiniteScrollComponent />
      </q-list>
    </q-drawer>

    <q-drawer
      v-model="rightDrawerOpen"
      side="right"
      behavior="mobile"
      bordered
      style="width: 50vh"
    >
      <!-- <NumbersSquares :databaseStatus="numbersStatus" /> -->
      <div style="justify-content: flex-start; display: flex; padding: 10px">
        <q-btn
          outline
          round
          color="alert"
          icon="close"
          @click="closeRightDrawer"
        />
      </div>
      <NumbersSquares />
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
    <q-dialog v-model="isDialogOpen" persistent>
      <q-card>
        <q-card-section>
          <div class="text-h6">Acceso a AdminPage</div>
        </q-card-section>
        <q-card-section>
          <q-input v-model="formData.username" label="Nombre" outlined />
          <q-input
            v-model="formData.password"
            type="password"
            label="Contraseña"
            outlined
          />
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="negative" @click="closeDialog" />
          <q-btn flat label="Acceder" color="positive" @click="accessAdmin" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-layout>
</template>

<script>
import { defineComponent, ref, onMounted, watch, toRaw } from "vue";
import InfiniteScrollComponent from "components/InfiniteScrollComponent.vue";
import NumbersSquares from "src/components/NumbersSquares.vue";
import { useLayoutStore } from "../stores/layoutStore";
import { useRouter } from "vue-router";
import { useQuasar } from "quasar";
import { api } from "boot/axios";
export default defineComponent({
  name: "MainLayout",
  components: {
    // EssentialLink,
    InfiniteScrollComponent,
    NumbersSquares,
  },

  setup() {
    const $q = useQuasar();
    const layoutStore = useLayoutStore();
    const leftDrawerOpen = ref(false);
    const rightDrawerOpen = ref(false);
    const isDialogOpen = ref(false);
    const formData = ref({
      username: "",
      password: "",
    });
    const countClick = ref([]);
    const router = useRouter();

    // click en la tombola pequeña statica
    // **Asumo que 'countClick' es una referencia reactiva (ej. ref() en Vue o similar)**
    // **y que 'isDialogOpen' también es una referencia reactiva.**

    const handleClick = () => {
      // 1. REGISTRO DEL CLIC:
      // En lugar de guardar '1', guardamos la marca de tiempo actual (en milisegundos)
      const timestampActual = Date.now();
      countClick.value.push(timestampActual);

      // Ejecutamos la comprobación inmediatamente después de un clic,
      // en lugar de esperar al setInterval, para una respuesta más rápida.
      comprobarCountClick();
    };

    const comprobarCountClick = () => {
      const LIMITE_TIEMPO_MS = 5000; // 5 segundos en milisegundos
      const LIMITE_CLICS = 5;

      // Obtener la hora actual para definir el final de la ventana de tiempo
      const tiempoAhora = Date.now();

      // **1. LIMPIEZA:**
      // Filtramos el array para mantener SOLO los clics que ocurrieron
      // dentro de los últimos 5 segundos (LIMITE_TIEMPO_MS).
      // NOTA: Esto no es ideal si countClick.value es una referencia mutada.
      // Una opción más legible y común es reasignar el array filtrado:

      const clicsRecientes = countClick.value.filter((timestamp) => {
        // Un clic es 'reciente' si su marca de tiempo es mayor que
        // (Tiempo Actual - 5000ms)
        return timestamp > tiempoAhora - LIMITE_TIEMPO_MS;
      });

      // Reasignamos el array limpio. Esto implementa la 'ventana deslizante'.
      countClick.value = clicsRecientes;

      // **2. COMPROBACIÓN DEL LÍMITE:**
      // Verificamos si la cantidad de clics recientes supera el límite
      if (countClick.value.length > LIMITE_CLICS) {
        // ¡Límite excedido!
        isDialogOpen.value = true;

        // Opcional: Reiniciamos la cuenta inmediatamente para evitar que
        // se siga abriendo el diálogo en el siguiente clic.
        countClick.value = [];
      }
    };

    // **3. EL TEMPORIZADOR:**
    // El setInterval ahora tiene un propósito secundario:
    // Limpiar periódicamente el array para liberar memoria,
    // aunque la comprobación principal se hace en handleClick.
    // Podemos hacerlo más lento ya que ya no es el motor principal.
    setInterval(comprobarCountClick, 1000); // Se ejecuta cada 1 segundo para limpieza y mantenimiento
    // click al cerrar el dialogo
    const closeDialog = () => {
      isDialogOpen.value = false;
      formData.value.username = "";
      formData.value.password = "";
    };

    const accessAdmin = async () => {
      try {
        // ✅ Usar axios en lugar del mixin
        const response = await api.post("/api/token/", {
          username: formData.value.username,
          password: formData.value.password,
          // cliente_token: "La_mata1985" // ← NO necesario, se agrega AUTOMÁTICAMENTE en el interceptor
        });

        // Verify if the tokens exist
        const { access, refresh } = response.data; // ← response.data con axios
        if (access && refresh) {
          // Store tokens in localStorage
          localStorage.setItem("accessToken", access);
          localStorage.setItem("refreshToken", refresh);

          try {
            console.log(router);
            router.push("/adminpage");
            closeDialog();
          } catch (error) {
            console.error("Navigation failed:", error);
          }
        } else {
          throw new Error("Invalid token response from the server.");
        }
      } catch (error) {
        console.error("Login error:", error);

        // Handle different error statuses
        if (error.response?.status === 401) {
          // ← error.response con axios
          $q.notify({
            type: "negative",
            message:
              "Credenciales incorrectas. Por favor, verifica tu usuario y contraseña.",
          });
        } else if (error.response?.status === 400) {
          $q.notify({
            type: "negative",
            message: "Solicitud incorrecta. Revisa los datos ingresados.",
          });
        } else {
          $q.notify({
            type: "negative",
            message: "Error en el servidor. Intenta nuevamente más tarde.",
          });
        }

        // Clear stored tokens in case of error
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
      }
    };
    const logout = () => {
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
      router.push("/");
    };

    onMounted(() => {
      if (!sessionStorage.getItem("MainLayout")) {
        sessionStorage.setItem("MainLayout", "true");
        location.reload();
      }
    });
    return {
      // bingoImage,
      logout,
      layoutStore,
      accessAdmin,
      closeDialog,
      handleClick,
      countClick,
      formData,
      isDialogOpen,
      leftDrawerOpen,
      toggleLeftDrawer() {
        leftDrawerOpen.value = !leftDrawerOpen.value;
      },

      rightDrawerOpen,
      toggleRightDrawer() {
        rightDrawerOpen.value = !rightDrawerOpen.value;
      },
      closeLeftDrawer() {
        leftDrawerOpen.value = false;
      },
      closeRightDrawer() {
        rightDrawerOpen.value = false;
      },
    };
  },
});
</script>
