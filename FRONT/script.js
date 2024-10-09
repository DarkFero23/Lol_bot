document.addEventListener('DOMContentLoaded', async () => {
  // Obtener la lista de campeones
  const response = await fetch('http://127.0.0.1:5000/campeones');
  const campeones = await response.json();

  // Llenar los select con los campeones
  const campeonPickSelect = document.getElementById('campeon_pick');
  const campeonBanSelect = document.getElementById('campeon_ban');

  campeones.forEach(campeon => {
      const optionPick = document.createElement('option');
      optionPick.value = campeon;
      optionPick.textContent = campeon;
      campeonPickSelect.appendChild(optionPick);

      const optionBan = document.createElement('option');
      optionBan.value = campeon;
      optionBan.textContent = campeon;
      campeonBanSelect.appendChild(optionBan);
  });
});

// Función para manejar el envío del formulario
document.getElementById('form').addEventListener('submit', async (e) => {
  e.preventDefault(); // Evitar el envío del formulario por defecto

  const campeonPick = document.getElementById('campeon_pick').value;
  const campeonBan = document.getElementById('campeon_ban').value;

  // Enviar la selección al servidor Flask
  const response = await fetch('http://127.0.0.1:5000/ejecutar_seleccion', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ campeon_pick: campeonPick, campeon_ban: campeonBan }),
  });

  // Manejar la respuesta del servidor
  const result = await response.json();
  document.getElementById('resultado').innerText = result.message || 'Proceso completado.';
});
