<template>
  <q-page class="q-pa-md">
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
        <q-card-section>
          <div class="text-h6">Editar Participante</div>
        </q-card-section>
        <q-card-section>
          <q-input v-model="editableRow.nombre" label="Nombre" dense></q-input>
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
          <q-input v-model="editableRow.correo" label="Correo" dense></q-input>
          <!-- <q-input
            v-model="editableRow.numero_seleccionado"
            label="Número Seleccionado"
            dense
            type="number"
          ></q-input> -->
          <q-input
            v-model="editableRow.descripcion"
            label="Descripción"
            dense
            type="textarea"
          />
          <q-input
            v-model="editableRow.comentarios"
            label="Comentarios"
            dense
            type="textarea"
          />
          <div style="text-align: center; padding: 5px">
            <q-btn
              class="glossy"
              rounded
              color="deep-orange"
              label="Eliminar"
              @click="eliminarPersonaTabla"
            />
          </div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="negative" @click="closeDialog" />
          <q-btn
            flat
            label="Guardar"
            color="positive"
            @click="updateRowTabla"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
    <div class="container">
      <div class="form-wrapper">
        <h5 style="margin: 5px">Subir Producto</h5>
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
            <input type="file" @change="handleImageUpload" />
          </label>
          <div style="text-align: center">
            <button style="margin: 0px" type="submit">Subir Producto</button>
          </div>
        </form>
      </div>
    </div>
    <div>
      <h5 style="margin: 5px">Lista de Productos</h5>
      <ul>
        <li
          v-for="product in products"
          :key="product.id"
          style="display: inline-grid"
        >
          <div style="display: block">
            <div style="text-align: center">{{ product.nombre }}</div>
            <div style="text-align: center">{{ product.descripcion }}</div>
          </div>

          <div style="text-align: center">
            <button @click="deleteProduct(product.id)">Eliminar</button>
          </div>

          <img
            style="height: 100px; width: 100px"
            :src="product.imagen_base64"
            alt="Imagen del producto"
          />
        </li>
      </ul>
    </div>
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
import { ref, onMounted, onUnmounted, reactive } from "vue";
import BASE_URL from "../variosJs/config";
// import { toRaw } from "vue";
import { useRouter } from "vue-router";
import { api } from "./../boot/axios";
import { useQuasar } from "quasar";
// import { getPosts } from "../variosJs/post-loader";
import axios from "axios";

export default {
  name: "EditableTable",
  setup() {
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
    let intervalId = null;
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
        width: "15px",
      },
      {
        name: "correo",
        label: "Correo",
        align: "left",
        field: "correo",
      },
      {
        name: "descripcion",
        label: "Descripción",
        align: "left",
        field: "descripcion",
      },
      {
        name: "comentarios",
        label: "Comentarios",
        align: "left",
        field: "comentarios",
      },
    ];
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
            const response = await axios.delete(
              `${BASE_URL}/api/productos/${productId}/`
            );
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
        const response = await axios.get(`${BASE_URL}/api/getproductos/`);
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
        const response = await axios.post(`${BASE_URL}/api/productos/`, {
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

    const updateRowTabla = async () => {
      try {
        const response = await api.put(
          `${BASE_URL}/api/personas/${editableRow.value.id}/`,
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
        const response = await fetch(`${BASE_URL}/api/get-allData/`);

        if (response.ok) {
          const updatedStatus = await response.json();
          allDataTable.value = updatedStatus;
        } else {
          console.error("Error al obtener el estado de los números.");
        }
      } catch (error) {
        console.error("Error al actualizar el estado:", error);
      }
    };

    //eliminar persona de la tabla

    const eliminarPersonaTabla = async () => {
      try {
        const response = await fetch(
          `${BASE_URL}/api/delete-user/${editableRow.value.id}/`,
          {
            method: "DELETE",
          }
        );

        if (response.ok) {
          const deletedStatus = await response.json();
          if (deletedStatus) {
            $q.notify({
              type: "positive",
              message: "Usuario eliminado.",
            });
          }
          isDialogOpen.value = false;
        } else {
          console.error("Error al obtener el estado de los números.");
        }
      } catch (error) {
        console.error("Error al actualizar el estado:", error);
      }
    };

    onMounted(async () => {
      if (!sessionStorage.getItem("adminPageLoaded")) {
        sessionStorage.setItem("adminPageLoaded", "true");
        location.reload();
      }
      loadProductosBBDD();
      loadPersonasTabla(); // Llamada inicial
      intervalId = setInterval(loadPersonasTabla, updateInterval);
    });

    onUnmounted(() => {
      if (intervalId) clearInterval(intervalId);
    });

    return {
      baseUrl: BASE_URL,
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
</style>

<style scoped>
/* Contenedor principal */
</style>
