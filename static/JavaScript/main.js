const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('active'); // Activa la animación definida en CSS
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

// Dentro de tu evento submit:
const buttonText = document.getElementById('buttonText');

// Antes del fetch:
buttonText.textContent = "Procesando envío...";

// Después de recibir respuesta ok:
buttonText.textContent = "¡Mensaje enviado!";
feedback.textContent = "Éxito: Tu mensaje ha sido procesado por el servidor.";