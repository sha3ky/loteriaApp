import { api } from "./../boot/axios";
import BASE_URL from "../variosJs/config";

export const getPosts = async () => {
  const productData = []; // Aquí se cargarán los datos de la API

  try {
    // Solicitar datos de los productos desde la API
    const response = await api.get(`${BASE_URL}/api/getproductos/`);

    if (response.status === 200) {
      productData.push(...response.data);
    } else {
      console.error("Error al obtener los datos de los productos.");
    }
  } catch (error) {
    console.error("Error al obtener los datos de productos:", error);
  }

  // Asociar productos con las rutas completas de sus imágenes
  const posts = productData.map((product) => {
    return {
      nombre: product.nombre, // Nombre del producto
      descripcion: product.descripcion, // Descripción del producto
      price: product.precio, // Precio del producto
      cantidad: product.cantidad, // Cantidad disponible
      imagen: product.imagen_base64, // Construir la URL completa de la imagen
    };
  });

  return posts;
};
