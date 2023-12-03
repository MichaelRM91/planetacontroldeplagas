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

//Buscar para tabla
$(document).ready(function () {
  $("#search-input").on("keyup", function () {
    var value = $(this).val().toLowerCase();
    $("table tbody tr").filter(function () {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
    });
  });
});
//Buscar para tarjetas
$(document).ready(function () {
  $("#search-input").on("keyup", function () {
    var value = $(this).val().toLowerCase();
    $(".card-container .card").filter(function () {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
    });
  });
});