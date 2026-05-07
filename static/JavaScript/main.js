// Observer unificado con márgenes optimizados
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('active');
            // Descomentar la siguiente línea si deseas que la animación solo ocurra una vez
            // observer.unobserve(entry.target); 
        }
    });
}, { threshold: 0.15, rootMargin: '0px 0px -50px 0px' });

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
document.querySelectorAll('.reveal-blur').forEach(el => observer.observe(el));

// --- Motor de Scroll-Telling de Alto Rendimiento ---
let isScrolling = false;

const handleScrollTelling = () => {
    const scrollSections = document.querySelectorAll('.scroll-telling-section');
    
    scrollSections.forEach(section => {
        const rect = section.getBoundingClientRect();
        // Se calcula el progreso: 0 cuando empieza a entrar, 1 cuando termina de salir
        let progress = (window.innerHeight - rect.top) / rect.height;
        progress = Math.max(0, Math.min(1, progress));
        
        // Inyectar el progreso como variable CSS en el contenedor interactivo
        const stickyViewport = section.querySelector('.sticky-viewport');
        if (stickyViewport) {
            stickyViewport.style.setProperty('--scroll-progress', progress);
        }
    });
    isScrolling = false;
};

// Throttle usando requestAnimationFrame (60 FPS fluidos)
window.addEventListener('scroll', () => {
    if (!isScrolling) {
        window.requestAnimationFrame(handleScrollTelling);
        isScrolling = true;
    }
}, { passive: true }); // passive optimiza el scrolling en navegadores

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