// Función para mostrar u ocultar elementos según el ancho de la pantalla
function toggleElements() {
    const windowWidth = window.innerWidth;

    const cardContainer = document.querySelector('.card-container');
    const tableDesktop = document.querySelector('.table-desktop');

    if (windowWidth <= 1000) {
      cardContainer.style.display = 'block';
      tableDesktop.style.display = 'none';
    } else {
      cardContainer.style.display = 'none';
      tableDesktop.style.display = 'table';
    }
  }

  // Ejecutar la función al cargar la página y al redimensionar la ventana
  window.addEventListener('load', toggleElements);
  window.addEventListener('resize', toggleElements);