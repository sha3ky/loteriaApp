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

    <q-drawer v-model="leftDrawerOpen" side="left" behavior="mobile" elevated style="width: 50vh;">
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
          <h5 style="padding: 0; margin: 0;text-align: center;">Cesta de Regalos</h5>
        </q-item-label>
        <InfiniteScrollComponent />
      </q-list>
    </q-drawer>

    <q-drawer v-model="rightDrawerOpen" side="right" behavior="mobile" bordered style="width: 50vh;">
      <!-- <NumbersSquares :databaseStatus="numbersStatus" /> -->
      <div
        style="
          justify-content: flex-start;
          display: flex;
          padding: 10px;
        "
      >
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
import { api } from "./../boot/axios";
import { useRouter } from "vue-router";
import { useQuasar } from "quasar";
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
    const countClick = ref(0);
    const router = useRouter();

    // click en la tombola pequeña statica
    const handleClick = () => {
      countClick.value++;
      if (countClick.value === 5) {
        isDialogOpen.value = true;
        countClick.value = 0;
      }
    };
    // click al cerrar el dialogo
    const closeDialog = () => {
      isDialogOpen.value = false;
      formData.value.username = "";
      formData.value.password = "";
    };

    const accessAdmin = async () => {
      try {
        // Start login request
        const response = await api.post("/api/token/", {
          username: formData.value.username,
          password: formData.value.password,
        });

        // Verify if the tokens exist
        const { access, refresh } = response.data;
        if (access && refresh) {
          // Store tokens in localStorage
          localStorage.setItem("accessToken", access);
          localStorage.setItem("refreshToken", refresh);
          // Redirect to the admin page

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
