document.addEventListener("DOMContentLoaded", () => {
  fetch("http://localhost:5000/obtener_campeones")
    .then((response) => response.json())
    .then((campeones) => {
      const pickSelect = document.getElementById("pick-campeon");
      const banSelect = document.getElementById("ban-campeon");

      campeones.forEach((campeon) => {
        // Crear opción para pick
        const optionPick = document.createElement("div");
        optionPick.textContent = campeon.name;
        const imgPick = document.createElement("img");
        imgPick.src = campeon.image;
        optionPick.prepend(imgPick);
        optionPick.addEventListener("click", () => {
          document.getElementById("pick-btn").textContent = campeon.name;
          pickSelect.style.display = "none";
        });
        pickSelect.appendChild(optionPick);

        // Crear opción para ban
        const optionBan = document.createElement("div");
        optionBan.textContent = campeon.name;
        const imgBan = document.createElement("img");
        imgBan.src = campeon.image;
        optionBan.prepend(imgBan);
        optionBan.addEventListener("click", () => {
          document.getElementById("ban-btn").textContent = campeon.name;
          banSelect.style.display = "none";
        });
        banSelect.appendChild(optionBan);
      });
    })
    .catch((error) => console.error("Error al cargar los campeones:", error));
});

function enviarSeleccion() {
  const campeonPick = document.getElementById("pick-btn").textContent;
  const campeonBan = document.getElementById("ban-btn").textContent;

  if (
    campeonPick === "Campeón a Pickear" ||
    campeonBan === "Campeón a Banear"
  ) {
    console.error("Debe seleccionar un campeón para pick y ban.");
    return;
  }

  fetch(
    `http://127.0.0.1:5000/seleccion?campeon_pick=${campeonPick}&campeon_ban=${campeonBan}`,
    { method: "GET" }
  )
    .then((response) => response.json())
    .then((data) => {
      if (data.status === "success") {
        console.log(
          `Campeones seleccionados: Pick - ${campeonPick}, Ban - ${campeonBan}`
        );
      } else {
        console.error(`Error: ${data.message}`);
      }
    })
    .catch((error) => console.error("Error al enviar la selección:", error));
}

// Muestra el dropdown al hacer clic en el botón correcto
document.getElementById("pick-btn").addEventListener("click", function () {
  const dropdownContent = document.getElementById("pick-campeon");
  dropdownContent.style.display =
    dropdownContent.style.display === "block" ? "none" : "block";
});

document.getElementById("ban-btn").addEventListener("click", function () {
  const dropdownContent = document.getElementById("ban-campeon");
  dropdownContent.style.display =
    dropdownContent.style.display === "block" ? "none" : "block";
});

// Cierra los dropdowns si el usuario hace clic fuera de ellos
window.onclick = function (event) {
  if (!event.target.matches(".dropbtn")) {
    document.querySelectorAll(".dropdown-content").forEach((dropdown) => {
      dropdown.style.display = "none";
    });
  }
};
