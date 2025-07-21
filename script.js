// Cursor trail effect
let mouseX = 0;
let mouseY = 0;
const cursorTrail = document.getElementById('cursorTrail');

document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
    
    cursorTrail.style.left = mouseX - 10 + 'px';
    cursorTrail.style.top = mouseY - 10 + 'px';
    
    // Create sparkle effect on mouse move
    createSparkle(mouseX, mouseY);
});

// Sparkle effect
function createSparkle(x, y) {
    const sparkle = document.createElement('div');
    sparkle.style.position = 'fixed';
    sparkle.style.left = x + 'px';
    sparkle.style.top = y + 'px';
    sparkle.style.width = '6px';
    sparkle.style.height = '6px';
    sparkle.style.background = 'white';
    sparkle.style.borderRadius = '50%';
    sparkle.style.pointerEvents = 'none';
    sparkle.style.zIndex = '9998';
    sparkle.style.animation = 'sparkleAnimation 1s ease-out forwards';
    
    document.body.appendChild(sparkle);
    
    setTimeout(() => {
        document.body.removeChild(sparkle);
    }, 1000);
}

// Add sparkle animation CSS
const sparkleStyle = document.createElement('style');
sparkleStyle.textContent = `
    @keyframes sparkleAnimation {
        0% {
            transform: scale(0) rotate(0deg);
            opacity: 1;
        }
        50% {
            transform: scale(1) rotate(180deg);
            opacity: 0.8;
        }
        100% {
            transform: scale(0) rotate(360deg);
            opacity: 0;
        }
    }
`;
document.head.appendChild(sparkleStyle);

// Particle system
const particlesContainer = document.getElementById('particlesContainer');
let particleCount = 0;
const maxParticles = 50;

function createParticle() {
    if (particleCount >= maxParticles) return;
    
    const particle = document.createElement('div');
    particle.className = 'particle';
    particle.style.left = Math.random() * 100 + '%';
    particle.style.animationDuration = (Math.random() * 3 + 2) + 's';
    particle.style.animationDelay = Math.random() * 2 + 's';
    
    // Random particle colors
    const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3'];
    particle.style.background = colors[Math.floor(Math.random() * colors.length)];
    
    particlesContainer.appendChild(particle);
    particleCount++;
    
    // Remove particle after animation
    setTimeout(() => {
        if (particle.parentNode) {
            particle.parentNode.removeChild(particle);
            particleCount--;
        }
    }, 4000);
}

// Create particles continuously
setInterval(createParticle, 300);

// Button interactions
const colorButton = document.getElementById('colorButton');
const particleButton = document.getElementById('particleButton');
const surpriseButton = document.getElementById('surpriseButton');

// Color theme switcher
const themes = ['theme-purple', 'theme-ocean', 'theme-sunset', 'theme-forest'];
let currentTheme = 0;

colorButton.addEventListener('click', () => {
    // Remove current theme
    document.body.className = document.body.className.replace(/theme-\w+/g, '');
    
    // Add new theme
    document.body.classList.add(themes[currentTheme]);
    currentTheme = (currentTheme + 1) % themes.length;
    
    // Button feedback
    colorButton.classList.add('shake');
    setTimeout(() => colorButton.classList.remove('shake'), 500);
    
    // Create explosion of colored particles
    createColorExplosion();
});

function createColorExplosion() {
    for (let i = 0; i < 15; i++) {
        setTimeout(() => {
            const particle = document.createElement('div');
            particle.style.position = 'fixed';
            particle.style.left = mouseX + 'px';
            particle.style.top = mouseY + 'px';
            particle.style.width = Math.random() * 8 + 4 + 'px';
            particle.style.height = particle.style.width;
            particle.style.borderRadius = '50%';
            particle.style.pointerEvents = 'none';
            particle.style.zIndex = '9997';
            
            const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3'];
            particle.style.background = colors[Math.floor(Math.random() * colors.length)];
            
            const angle = (i / 15) * Math.PI * 2;
            const distance = Math.random() * 100 + 50;
            const endX = mouseX + Math.cos(angle) * distance;
            const endY = mouseY + Math.sin(angle) * distance;
            
            particle.style.transform = `translate(${endX - mouseX}px, ${endY - mouseY}px) scale(0)`;
            particle.style.transition = 'transform 0.8s ease-out, opacity 0.8s ease-out';
            particle.style.opacity = '0';
            
            document.body.appendChild(particle);
            
            setTimeout(() => {
                particle.style.transform = `translate(${endX - mouseX}px, ${endY - mouseY}px) scale(1)`;
                particle.style.opacity = '1';
            }, 10);
            
            setTimeout(() => {
                if (particle.parentNode) {
                    document.body.removeChild(particle);
                }
            }, 800);
        }, i * 50);
    }
}

// Particle burst button
particleButton.addEventListener('click', () => {
    // Create burst of particles
    for (let i = 0; i < 20; i++) {
        setTimeout(createParticle, i * 100);
    }
    
    particleButton.classList.add('shake');
    setTimeout(() => particleButton.classList.remove('shake'), 500);
});

// Surprise button
let surpriseActive = false;

surpriseButton.addEventListener('click', () => {
    if (!surpriseActive) {
        activateSurpriseMode();
    } else {
        deactivateSurpriseMode();
    }
});

function activateSurpriseMode() {
    surpriseActive = true;
    surpriseButton.textContent = '🎉 Остановить веселье!';
    
    // Add rainbow effect to everything
    document.querySelectorAll('.floating-emoji').forEach(emoji => {
        emoji.classList.add('surprise-mode');
    });
    
    document.querySelector('.magic-title').classList.add('surprise-mode');
    
    // Accelerate animations
    document.documentElement.style.setProperty('--animation-speed', '0.5s');
    
    // Create continuous fireworks
    surpriseInterval = setInterval(createFirework, 1000);
    
    // Play with floating emojis
    animateFloatingEmojis();
}

function deactivateSurpriseMode() {
    surpriseActive = false;
    surpriseButton.textContent = '🎉 Сюрприз!';
    
    // Remove rainbow effects
    document.querySelectorAll('.surprise-mode').forEach(element => {
        element.classList.remove('surprise-mode');
    });
    
    // Reset animation speed
    document.documentElement.style.setProperty('--animation-speed', '1s');
    
    // Stop fireworks
    if (surpriseInterval) {
        clearInterval(surpriseInterval);
    }
}

function createFirework() {
    const centerX = Math.random() * window.innerWidth;
    const centerY = Math.random() * window.innerHeight * 0.7;
    
    for (let i = 0; i < 12; i++) {
        const particle = document.createElement('div');
        particle.style.position = 'fixed';
        particle.style.left = centerX + 'px';
        particle.style.top = centerY + 'px';
        particle.style.width = '6px';
        particle.style.height = '6px';
        particle.style.borderRadius = '50%';
        particle.style.pointerEvents = 'none';
        particle.style.zIndex = '9996';
        
        const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3', '#white'];
        particle.style.background = colors[Math.floor(Math.random() * colors.length)];
        
        const angle = (i / 12) * Math.PI * 2;
        const distance = Math.random() * 150 + 100;
        const endX = centerX + Math.cos(angle) * distance;
        const endY = centerY + Math.sin(angle) * distance;
        
        particle.style.transition = 'transform 1.5s ease-out, opacity 1.5s ease-out';
        
        document.body.appendChild(particle);
        
        setTimeout(() => {
            particle.style.transform = `translate(${endX - centerX}px, ${endY - centerY}px)`;
            particle.style.opacity = '0';
        }, 10);
        
        setTimeout(() => {
            if (particle.parentNode) {
                document.body.removeChild(particle);
            }
        }, 1500);
    }
}

function animateFloatingEmojis() {
    const emojis = document.querySelectorAll('.floating-emoji');
    emojis.forEach((emoji, index) => {
        setTimeout(() => {
            emoji.style.transform = 'scale(1.5) rotate(360deg)';
            emoji.style.transition = 'transform 2s ease-in-out';
            
            setTimeout(() => {
                emoji.style.transform = 'scale(1) rotate(0deg)';
            }, 2000);
        }, index * 200);
    });
}

// Click anywhere effect
document.addEventListener('click', (e) => {
    // Create ripple effect
    const ripple = document.createElement('div');
    ripple.style.position = 'fixed';
    ripple.style.left = e.clientX + 'px';
    ripple.style.top = e.clientY + 'px';
    ripple.style.width = '0px';
    ripple.style.height = '0px';
    ripple.style.border = '2px solid rgba(255, 255, 255, 0.6)';
    ripple.style.borderRadius = '50%';
    ripple.style.pointerEvents = 'none';
    ripple.style.zIndex = '9995';
    ripple.style.transition = 'all 0.6s ease-out';
    
    document.body.appendChild(ripple);
    
    setTimeout(() => {
        ripple.style.width = '100px';
        ripple.style.height = '100px';
        ripple.style.left = (e.clientX - 50) + 'px';
        ripple.style.top = (e.clientY - 50) + 'px';
        ripple.style.opacity = '0';
    }, 10);
    
    setTimeout(() => {
        if (ripple.parentNode) {
            document.body.removeChild(ripple);
        }
    }, 600);
});

// Welcome message
setTimeout(() => {
    console.log('🌟 Добро пожаловать в магический мир интерактивности! 🌟');
    console.log('💡 Попробуйте кликнуть на кнопки и подвигать мышкой!');
}, 1000);