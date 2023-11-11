function generatePdfBtn(razon_social, servicio_id) {
  
  var element = document.getElementById("sheet0");

  html2pdf(element, {
    margin: 5,
    filename: razon_social+" - "+servicio_id+".pdf",
    image: { type: "jpeg", quality: 0.98 },
    html2canvas: { scale: 2 },
    jsPDF: { unit: "mm", format: "a2", orientation: "portrait" },
  });
}

function previewFirma() {
  var input = document.getElementById("formFile");
  var preview = document.getElementById("firmaPreview");

  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      preview.src = e.target.result;
    };

    reader.readAsDataURL(input.files[0]);
  }
  var btn = document.getElementById("guardarFirma")
  btn.classList.remove('d-none')
}
