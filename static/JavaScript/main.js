const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('active'); // Activa la animación definida en CSS
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

const contactForm = document.getElementById('contactForm');
if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const buttonText = document.getElementById('buttonText');
        const feedback = document.getElementById('feedback');
        
        buttonText.textContent = "Procesando envío...";
        
        try {
            const response = await fetch('/api/contact', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email: document.getElementById('email').value,
                    message: document.getElementById('message').value
                })
            });
            
            if (response.ok) {
                buttonText.textContent = "¡Mensaje enviado!";
                feedback.textContent = "Éxito: Tu mensaje ha sido procesado por el servidor.";
            } else {
                buttonText.textContent = "Reintentar";
                feedback.textContent = "Hubo un error al validar los datos.";
            }
        } catch (error) {
            buttonText.textContent = "Error de conexión";
        }
    });
}