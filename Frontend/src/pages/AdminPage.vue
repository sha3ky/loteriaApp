<template>
  <q-page class="q-pa-md">
    <div class="q-gutter-y-md" style="display: flex; justify-content: center">
      <q-tabs v-model="tab" class="text-gray">
        <q-tab name="participants" icon="people" label="Participantes" />
        <q-tab name="settings" icon="settings" label="Configuración" />
        <q-tab name="products" icon="inventory" label="Productos" />
      </q-tabs>
    </div>

    <q-tab-panels v-model="tab" animated>
      <!-- TAB CONFIGURACIÓN -->
      <q-tab-panel name="settings">
        <q-toggle
          v-model="configuracion.mostrar_boton_demo"
          color="green"
          label="Mostrar botón demo"
          @update:model-value="guardarConfiguracion"
        />

        <q-toggle
          v-model="configuracion.auto_girar_ruleta"
          color="green"
          label="Auto-girar ruleta"
          @update:model-value="guardarConfiguracion"
        />
        <q-input
          v-model="fechaFinalCountdown"
          label="Fecha y hora final del countdown"
          filled
          readonly
          @click="showDateTimePicker = true"
        />

        <q-dialog v-model="showDateTimePicker">
          <q-card style="max-width: 90vw; text-align: center">
            <q-card-section>
              <div class="row items-center justify-between q-col-gutter-md">
                <!-- Fecha - ocupa toda la fila en móvil, mitad en desktop -->

                <div class="col-12 col-md-6 q-pa-sm">
                  <q-date
                    v-model="fechaTemp"
                    mask="YYYY-MM-DD HH:mm"
                    today-btn
                    style="max-width: 100%"
                  />
                </div>

                <!-- Hora - ocupa toda la fila en móvil, mitad en desktop -->
                <div class="col-12 col-md-6 q-pa-sm">
                  <q-time
                    v-model="fechaTemp"
                    mask="YYYY-MM-DD HH:mm"
                    format24h
                    style="max-width: 100%"
                  />
                </div>
              </div>
            </q-card-section>

            <q-card-actions align="right">
              <q-btn label="Cancelar" color="red" v-close-popup />
              <q-btn
                label="OK"
                color="green"
                @click="confirmDateTime"
                v-close-popup
              />
            </q-card-actions>
          </q-card>
        </q-dialog>
        <!-- Para los textos usa inputs -->
        <q-input
          v-model="configuracion.texto_countdown"
          label="Texto del countdown"
          filled
          @update:model-value="guardarConfiguracion"
        />

        <q-input
          v-model="configuracion.texto_ganador"
          label="Texto del ganador"
          filled
          @update:model-value="guardarConfiguracion"
        />

        <q-input
          v-model="configuracion.texto_intentar_otra_vez"
          label="Texto intentar otra vez"
          filled
          @update:model-value="guardarConfiguracion"
        />

        <q-input
          v-model="configuracion.texto_boton_demo"
          label="Texto botón demo"
          filled
          @update:model-value="guardarConfiguracion"
        />

        <!-- Para colores usa color picker -->
        <q-input
          v-model="configuracion.color_principal"
          label="Color principal"
          filled
          @update:model-value="guardarConfiguracion"
        >
          <template v-slot:append>
            <q-icon name="colorize" class="cursor-pointer">
              <q-popup-proxy>
                <q-color v-model="configuracion.color_principal" />
              </q-popup-proxy>
            </q-icon>
          </template>
        </q-input>

        <q-input
          v-model="configuracion.color_secundario"
          label="Color secundario"
          filled
          @update:model-value="guardarConfiguracion"
        >
          <template v-slot:append>
            <q-icon name="colorize" class="cursor-pointer">
              <q-popup-proxy>
                <q-color v-model="configuracion.color_secundario" />
              </q-popup-proxy>
            </q-icon>
          </template>
        </q-input>

        <!-- Para números -->
        <q-input
          v-model="configuracion.horas_extension_countdown"
          label="Horas extensión countdown"
          type="number"
          filled
          @update:model-value="guardarConfiguracion"
        />

        <q-input
          v-model="configuracion.intervalo_auto_girar"
          label="Intervalo auto-girar (segundos)"
          type="number"
          filled
          @update:model-value="guardarConfiguracion"
        />
      </q-tab-panel>

      <!-- TAB PRODUCTOS -->
      <q-tab-panel name="products">
        <div class="admin-container">
          <!-- Columna del Formulario -->
          <div class="form-column">
            <div class="form-wrapper">
              <h5>Añadir Producto</h5>
              <form @submit.prevent="uploadProduct">
                <label>
                  Nombre:
                  <input v-model="product.nombre" type="text" required />
                </label>
                <label>
                  Descripción:
                  <textarea v-model="product.descripcion" required></textarea>
                </label>
                <label>
                  Precio:
                  <input v-model="product.precio" type="number" />
                </label>
                <label>
                  Cantidad:
                  <input v-model="product.cantidad" type="number" />
                </label>
                <label>
                  Imagen:
                  <input
                    type="file"
                    @change="handleImageUpload"
                    id="miFileInput"
                  />
                </label>
                <div class="button-container">
                  <button type="submit">Subir Producto</button>
                </div>
              </form>
            </div>
          </div>

          <!-- Columna de Productos -->
          <div class="products-column">
            <h5>Lista de Productos</h5>
            <div class="products-grid">
              <div
                v-for="product in products"
                :key="product.id"
                class="product-card"
              >
                <img
                  :src="product.imagen_base64"
                  alt="Imagen del producto"
                  class="product-image"
                />
                <div class="product-info">
                  <h6>{{ product.nombre }}</h6>
                  <p>{{ product.descripcion }}</p>
                  <div class="product-actions">
                    <button @click="deleteProduct(product.id)">Eliminar</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </q-tab-panel>

      <!-- TAB PARTICIPANTES -->
      <q-tab-panel name="participants">
        <q-table
          :dense="$q.screen.lt.md"
          title="Participantes"
          :rows="allDataTable"
          :columns="columns"
          row-key="id"
          flat
          bordered
          class="q-pa-md q-table"
          style="table-layout: fixed; width: 100%"
          :separator="separator"
          v-model:pagination="pagination"
          :rows-per-page-options="[5, 10, 20, 50, 99]"
          :rows-per-page="10"
          @row-click="openEditDialog"
        >
          <template v-slot:body="props">
            <q-tr :props="props" @click="openEditDialog(props.row)">
              <q-td v-for="col in columns" :key="col.name" :props="props">
                {{ props.row[col.field] }}
              </q-td>
            </q-tr>
          </template>
        </q-table>
        <q-dialog v-model="isDialogOpen" persistent>
          <q-card style="width: 400px">
            <q-card-section style="background-color: firebrick">
              <div>
                <h5 style="margin: 0px; padding: 0px">
                  <span style="color: white">Participante</span>
                </h5>
              </div>
            </q-card-section>
            <q-card-section>
              <q-input
                v-model="editableRow.nombre"
                label="Nombre"
                dense
              ></q-input>
              <q-input
                v-model="editableRow.apellido"
                label="Apellido"
                dense
              ></q-input>
              <q-input
                v-model="editableRow.telefono"
                label="Teléfono"
                dense
              ></q-input>
              <q-input
                v-model="editableRow.correo"
                label="Correo"
                dense
              ></q-input>
              <!--   <q-input
            v-model="editableRow.numero_seleccionado"
            label="Número Seleccionado"
            dense
            type="number"
          ></q-input> -->
              <!--  <q-input
            v-model="editableRow.descripcion"
            label="Descripción"
            dense
            type="textarea"
          /> -->
              <q-input
                v-model="editableRow.comentarios"
                label="Comentarios"
                dense
                type="textarea"
              />
              <div style="text-align: center; padding: 5px">
                <q-btn
                  style="color: firebrick"
                  label="Eliminar"
                  @click="eliminarPersonaTabla"
                />
              </div>
            </q-card-section>
            <q-card-actions align="right">
              <q-btn label="Cancelar" color="negative" @click="closeDialog" />
              <q-btn label="Guardar" color="positive" @click="updateRowTabla" />
            </q-card-actions>
          </q-card>
        </q-dialog>
      </q-tab-panel>
    </q-tab-panels>

    <div style="text-align: center">
      <q-btn
        flat
        icon="logout"
        label="Salir"
        color="negative"
        @click="logout"
        class="q-ml-auto"
        style="font-weight: bold; margin-right: 15px"
      />
    </div>
  </q-page>
</template>

<script>
import { ref, onMounted, onUnmounted, reactive, computed, watch } from "vue";
/* import BASE_URL from "../variosJs/config"; */
// import { toRaw } from "vue";
import { useRouter } from "vue-router";
import { api } from "boot/axios";
import { useQuasar } from "quasar";

export default {
  name: "EditableTable",
  setup() {
    const showDateTimePicker = ref(false);
    const fechaTemp = ref("");

    const fechaFinalCountdown = computed({
      get: () => {
        if (!configuracion.value.fecha_final_countdown) return "";

        const fecha = new Date(configuracion.value.fecha_final_countdown);
        const year = fecha.getUTCFullYear();
        const month = String(fecha.getUTCMonth() + 1).padStart(2, "0");
        const day = String(fecha.getUTCDate()).padStart(2, "0");
        const hours = String(fecha.getUTCHours()).padStart(2, "0");
        const minutes = String(fecha.getUTCMinutes()).padStart(2, "0");

        return `${day}/${month}/${year} ${hours}:${minutes}`;
      },
      set: (newValue) => {
        // No necesitamos setter si usamos el diálogo
      },
    });

    const confirmDateTime = () => {
      if (fechaTemp.value) {
        // Convertir a formato ISO para la base de datos
        const [fechaPart, horaPart] = fechaTemp.value.split(" ");
        const [year, month, day] = fechaPart.split("-");
        const [hours, minutes] = horaPart.split(":");

        // Crear fecha en UTC (para España UTC+1, ajustamos)
        const fechaUTC = new Date(
          Date.UTC(year, month - 1, day, hours, minutes)
        );
        configuracion.value.fecha_final_countdown = fechaUTC.toISOString();

        guardarConfiguracion();
      }
      showDateTimePicker.value = false;
    };
    const configuracion = ref({});
    const tab = ref("participants");
    const product = reactive({
      nombre: "",
      descripcion: "",
      precio: null,
      cantidad: null,
      imagen: null, // Archivo de imagen
    });
    const products = ref([]);
    const $q = useQuasar();
    const pagination = ref({
      page: 1,
      rowsPerPage: 0, // Muestra todos los registros en una sola página
    });
    const separator = ref("cell");
    const allDataTable = ref([]);
    const updateInterval = 5000; // 5 segundos
    const router = useRouter();
    const isDialogOpen = ref(false); // Controls dialog visibility
    const editableRow = ref({}); // Stores the row data being edited
    const selectedRowId = ref(null); // Stores the ID of the selected row
    const columns = [
      {
        name: "nombre",
        label: "Nombre",
        align: "left",
        sortable: true,
        field: "nombre",
      },
      {
        name: "apellido",
        label: "Apellido",
        align: "left",
        sortable: true,
        field: "apellido",
      },
      {
        name: "telefono",
        label: "Teléfono",
        align: "left",
        field: "telefono",
        sortable: true,
      },
      {
        name: "creado_en",
        label: "Creado En Fecha",
        align: "center",
        field: "creado_en",
      },
      {
        name: "numero_seleccionado",
        label: "Número Seleccionado",
        align: "center",
        field: "numero_seleccionado",
        sortable: true,
        width: "10px",
      },
      {
        name: "correo",
        label: "Correo",
        align: "left",
        field: "correo",
      },
      /*   {
        name: "descripcion",
        label: "Descripción",
        align: "left",
        field: "descripcion",
      }, */
      {
        name: "comentarios",
        label: "Comentarios",
        align: "left",
        field: "comentarios",
      },
    ];
    let timeoutId = null;
    let intervalId = null;
    const guardando = ref(false);

    //imagenes------------------------------------------

    //eliminamos un producto de la base de datos

    const deleteProduct = async (productId) => {
      $q.dialog({
        title: "Confirmar Eliminación",
        message: "¿Estás seguro de que deseas eliminar este producto?",
        cancel: true, // Muestra el botón de cancelar
        persistent: true, // Evita cerrar el diálogo haciendo clic fuera
      })
        .onOk(async () => {
          // Si el usuario confirma, elimina el producto
          try {
            const response = await api.delete(`/api/productos/${productId}/`);
            if (response.status === 200) {
              $q.notify({
                type: "positive",
                message: "Producto eliminado con éxito.",
              });
              // Actualizar la lista de productos eliminando el producto borrado
              products.value = products.value.filter(
                (product) => product.id !== productId
              );
            }
          } catch (error) {
            console.error("Error al eliminar el producto:", error);
            $q.notify({
              type: "negative",
              message: "Hubo un error al eliminar el producto.",
            });
          }
        })
        .onCancel(() => {
          // Si el usuario cancela, puedes mostrar una notificación opcional
          $q.notify({
            type: "info",
            message: "Eliminación cancelada.",
          });
        });
    };

    // cargamos todos los productos que estan en la bbdd

    const loadProductosBBDD = async () => {
      try {
        const response = await api.get("/api/getproductos/");
        if (response.status === 200) {
          products.value = response.data; // Cargar productos en la lista
        }
      } catch (error) {
        console.error("Error al obtener los productos:", error);
      }
    };

    // Captura el archivo seleccionado

    const handleImageUpload = (event) => {
      product.imagen = event.target.files[0];
    };

    //  convertimos la imagen en base64 para la bbdd

    const convertToBase64 = (file) => {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = (error) => reject(error);
      });
    };

    // subimos un producto a la base de datos

    const uploadProduct = async () => {
      try {
        const base64Image = await convertToBase64(product.imagen);
        const response = await api.post("/api/productos/", {
          nombre: product.nombre,
          descripcion: product.descripcion,
          cantidad: product.cantidad,
          precio: product.precio,
          imagen_base64: base64Image,
        });

        if (response.status === 201) {
          $q.notify({
            type: "positive",
            message: "Producto subido Ok.",
          });
          // Limpia el formulario o actualiza la lista de productos
          resetForm();
          await loadProductosBBDD();
        }
      } catch (error) {
        // Identifica si el error proviene del servidor o de la red
        if (error.response) {
          // Respuesta del servidor con código de error
          console.error("Error en el servidor:", error.response.data);
          $q.notify({
            type: "negative",
            message: `Error al subir el producto: ${
              error.response.data.detail || "Error desconocido en el servidor."
            }`,
          });
        } else if (error.request) {
          // La solicitud fue hecha pero no se recibió respuesta
          console.error(
            "Error en la red o sin respuesta del servidor:",
            error.request
          );
          $q.notify({
            type: "negative",
            message:
              "No se pudo conectar al servidor. Verifica tu conexión a internet.",
          });
        } else {
          // Error inesperado
          console.error("Error inesperado:", error.message);
          $q.notify({
            type: "negative",
            message:
              "Ocurrió un error inesperado. Por favor, intenta nuevamente.",
          });
        }
      }
    };

    // reseteamos el formulario al subir el producto en la bbdd

    const resetForm = () => {
      product.nombre = "";
      product.descripcion = "";
      product.precio = null;
      product.cantidad = null;
      product.imagen = "";
      let fileInput = document.getElementById("miFileInput");
      if (fileInput) {
        fileInput.value = "";
      }
    };

    //imagenes------------------------------------------

    //Abrimos el dialogo para editar persona en la tabla

    const openEditDialog = (row) => {
      editableRow.value = { ...row }; // Clonamos los datos para editarlos
      isDialogOpen.value = true; // Abre el diálogo
    };

    // Cerrar el dialogo

    const closeDialog = () => {
      isDialogOpen.value = false;
    };

    // Function para hacer el update a la tabla
    const cargarConfiguracion = async () => {
      debugger;
      try {
        const response = await api.get("/api/configuracion-cliente/");
        configuracion.value = response.data;
      } catch (error) {
        console.error("❌ Error completo:", error.response?.data);
        // Muestra el mensaje específico del backend
      }
    };

    const guardarConfiguracion = () => {
      if (timeoutId) clearTimeout(timeoutId);

      // Mostrar notificación simple sin números
      $q.notify({
        message: "Guardando automáticamente...",
        timeout: 2500, // Se cierra sola después de 2.5 segundos
        type: "warning",
        position: "bottom",
      });

      // Guardar después del tiempo
      timeoutId = setTimeout(() => {
        ejecutarGuardado();
      }, 3000);
    };

    const ejecutarGuardado = async () => {
      guardando.value = true;

      /* const notificacion = $q.notify({
        message: "Guardando configuración...",
        spinner: true,
        timeout: 0,
        type: "info",
        position: "bottom",
      }); */
      debugger;
      try {
        // ✅ Enviar token como parámetro (igual que el GET)
        await api.post("/api/guardar-configuracion/", configuracion.value);

        // ✅ Cerrar notificación ANTES de crear la nueva
        /*    notificacion(); */
        $q.notify({
          message: "✅ Configuración guardada",
          spinner: false,
          type: "positive",
          timeout: 2000,
        });
      } catch (error) {
        // ✅ Cerrar notificación ANTES de crear la nueva
        /*   notificacion(); */
        $q.notify({
          message: "❌ Error guardando configuración",
          spinner: false,
          type: "negative",
          timeout: 3000,
        });
        console.error("Error 403 details:", error.response?.data);
      } finally {
        guardando.value = false;
      }
    };

    const updateRowTabla = async () => {
      try {
        const response = await api.put(
          `/api/personas/${editableRow.value.id}/`,
          editableRow.value
        );
        if (response.status === 200) {
          // Update the table data locally
          const updatedIndex = allDataTable.value.findIndex(
            (item) => item.id === editableRow.value.id
          );
          if (updatedIndex !== -1) {
            allDataTable.value[updatedIndex] = { ...editableRow.value };
          }
          isDialogOpen.value = false; // Close the dialog
          $q.notify({
            type: "positive",
            message: "Datos actualizados con éxito.",
          });
        } else {
          $q.notify({
            type: "negative",
            message: "Error al actualizar los datos.",
          });
        }
      } catch (error) {
        console.error("Error while updating row:", error);
        $q.notify({
          type: "negative",
          message: "Ocurrió un error al actualizar los datos.",
        });
      }
    };

    // eliminar datos al cerrar session

    const logout = () => {
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
      router.push("/");
    };

    // Navegar a la ruta raíz

    const volverHome = () => {
      router.push("/");
      logout();
    };

    // cargar personas para la tabla

    const loadPersonasTabla = async () => {
      try {
        const response = await api.get("/api/get-allData/");
        allDataTable.value = response.data;
      } catch (error) {
        console.error("Error al actualizar el estado:", error);
      }
    };

    //eliminar persona de la tabla

    const eliminarPersonaTabla = async () => {
      try {
        // ❌ ERROR: usabas api.get con method: "DELETE"
        // ✅ CORRECTO: usa api.delete directamente
        const response = await api.delete(
          `/api/delete-user/${editableRow.value.id}/`
        );

        if (response.status === 200) {
          $q.notify({
            type: "positive",
            message: "Usuario eliminado.",
          });
          isDialogOpen.value = false;
          loadPersonasTabla(); // Recargar la lista
        }
      } catch (error) {
        console.error("Error eliminando usuario:", error);
        $q.notify({
          type: "negative",
          message: "Error al eliminar usuario.",
        });
      }
    };

    onMounted(async () => {
      if (!sessionStorage.getItem("adminPageLoaded")) {
        sessionStorage.setItem("adminPageLoaded", "true");
        location.reload();
      }
      loadProductosBBDD();
      loadPersonasTabla(); // Llamada inicial
      /* intervalId = setInterval(loadPersonasTabla, updateInterval); */
      cargarConfiguracion();
    });

    onUnmounted(() => {
      if (intervalId) clearInterval(intervalId);
    });

    watch(showDateTimePicker, (newVal) => {
      if (newVal && configuracion.value.fecha_final_countdown) {
        // Convertir de UTC a hora local para España
        const fecha = new Date(configuracion.value.fecha_final_countdown);
        const year = fecha.getUTCFullYear();
        const month = String(fecha.getUTCMonth() + 1).padStart(2, "0");
        const day = String(fecha.getUTCDate()).padStart(2, "0");
        const hours = String(fecha.getUTCHours()).padStart(2, "0");
        const minutes = String(fecha.getUTCMinutes()).padStart(2, "0");

        fechaTemp.value = `${year}-${month}-${day} ${hours}:${minutes}`;
      } else if (newVal && !configuracion.value.fecha_final_countdown) {
        // Si no hay fecha, usar la actual
        const now = new Date();
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, "0");
        const day = String(now.getDate()).padStart(2, "0");
        const hours = String(now.getHours()).padStart(2, "0");
        const minutes = String(now.getMinutes()).padStart(2, "0");

        fechaTemp.value = `${year}-${month}-${day} ${hours}:${minutes}`;
      }
    });
    return {
      resetForm,
      deleteProduct,
      loadProductosBBDD,
      products,
      product,
      uploadProduct,
      handleImageUpload,
      editableRow,
      selectedRowId,
      isDialogOpen,
      openEditDialog,
      updateRowTabla,
      closeDialog,
      logout,
      allDataTable,
      columns,
      separator,
      loadPersonasTabla,
      pagination,
      volverHome,
      eliminarPersonaTabla,
      tab,
      configuracion,
      guardarConfiguracion,
      showDateTimePicker,
      fechaTemp,
      confirmDateTime,
      fechaFinalCountdown,
    };
  },
};
</script>

<style scoped>
.q-table .q-td,
.q-table .q-th {
  white-space: nowrap; /* Evita que el texto salte a una nueva línea */
  overflow: hidden; /* Oculta el contenido que excede el ancho */
  text-overflow: ellipsis; /* Añade puntos suspensivos si el contenido es demasiado largo */
}
form label {
  display: block; /* Stack labels and inputs vertically */
  margin-bottom: 15px; /* Add space between fields */
  font-size: 14px;
  color: #333;

  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Add a subtle shadow */
  text-align: left;
}

form input,
form textarea {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
}

/* Style for the button */
form button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

form button:hover {
  background-color: #45a049;
}

/* añadir productos css */

.admin-container {
  display: grid;
  grid-template-columns: 1fr 2fr; /* Form 33%, Products 66% */
  gap: 20px;
  height: 100vh;
  padding: 20px;
  box-sizing: border-box;
}

/* Columna del Formulario */
.form-column {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
}

.form-wrapper {
  height: 100%;
}

.form-wrapper h5 {
  margin: 0 0 20px 0;
  text-align: center;
  color: #333;
}

.form-wrapper form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-wrapper label {
  display: flex;
  flex-direction: column;
  gap: 5px;
  font-weight: 500;
  color: #555;
}

.form-wrapper input,
.form-wrapper textarea {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.form-wrapper textarea {
  min-height: 80px;
  resize: vertical;
}

.button-container {
  text-align: center;
  margin-top: 10px;
}

.form-wrapper button {
  padding: 12px 30px;
  background: #1976d2;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

/* Columna de Productos */
.products-column {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  overflow-y: auto;
}

.products-column h5 {
  margin: 0 0 20px 0;
  color: #333;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
}

.product-card {
  background: white;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.product-image {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 4px;
  margin-bottom: 10px;
}

.product-info h6 {
  margin: 0 0 8px 0;
  color: #333;
}

.product-info p {
  margin: 0 0 10px 0;
  color: #666;
  font-size: 14px;
}

.product-actions button {
  padding: 8px 16px;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

/* Responsive */
@media (max-width: 768px) {
  .admin-container {
    grid-template-columns: 1fr;
    height: auto;
    padding: 10px;
  }

  .products-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }
}
</style>
