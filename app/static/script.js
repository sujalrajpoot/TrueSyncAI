// Wait for DOM content to load
document.addEventListener('DOMContentLoaded', function() {
    // Loading screen functionality
    const loadingScreen = document.querySelector('.loading-screen');
    
    // Hide loading screen after 2 seconds
    setTimeout(() => {
        loadingScreen.classList.add('hidden');
    }, 2000);
    
    // Mobile menu toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    menuToggle.addEventListener('click', function() {
        navLinks.classList.toggle('active');
    });
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', function(event) {
        const isClickInsideNav = navLinks.contains(event.target);
        const isClickOnToggle = menuToggle.contains(event.target);
        
        if (!isClickInsideNav && !isClickOnToggle && navLinks.classList.contains('active')) {
            navLinks.classList.remove('active');
        }
    });
    
    // Header scroll effect
    const header = document.querySelector('header');
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });
    
    // Animate stats counter
    const stats = document.querySelectorAll('.stat-number');
    
    const animateStats = () => {
        stats.forEach(stat => {
            const target = parseInt(stat.getAttribute('data-target'));
            const count = +stat.innerText;
            const increment = target / 100;
            
            if (count < target) {
                stat.innerText = Math.ceil(count + increment);
                setTimeout(animateStats, 30);
            } else {
                stat.innerText = target;
            }
        });
    };
    
    // Intersection Observer for animations
    const observerOptions = {
        threshold: 0.1
    };
    
    const observer = new IntersectionObserver(function(entries, observer) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                if (entry.target.classList.contains('hero-stats')) {
                    stats.forEach(stat => {
                        stat.innerText = '0';
                    });
                    animateStats();
                }
                entry.target.classList.add('animate');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    observer.observe(document.querySelector('.hero-stats'));
    
    // Feature cards hover effect
    const featureCards = document.querySelectorAll('.feature-card');
    
    featureCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            featureCards.forEach(c => c.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
                
                // Close mobile menu if open
                if (navLinks.classList.contains('active')) {
                    navLinks.classList.remove('active');
                }
                
                // Update active navigation link
                document.querySelectorAll('.nav-links a').forEach(link => {
                    link.classList.remove('active');
                });
                this.classList.add('active');
            }
        });
    });
    
    // Add active class to navigation based on scroll position
    const sections = document.querySelectorAll('section');
    
    window.addEventListener('scroll', function() {
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (window.scrollY >= (sectionTop - 200)) {
                current = section.getAttribute('id');
            }
        });
        
        document.querySelectorAll('.nav-links a').forEach(link => {
            link.classList.remove('active');
            const href = link.getAttribute('href');
            if (href === `#${current}`) {
                link.classList.add('active');
            }
        });
    });
    
    // Modal for demo video
    const demoButton = document.querySelector('.btn-secondary');
    
    if (demoButton) {
        demoButton.addEventListener('click', function() {
            // Create modal elements
            const modal = document.createElement('div');
            modal.className = 'modal';
            
            const modalContent = document.createElement('div');
            modalContent.className = 'modal-content';
            
            const closeButton = document.createElement('span');
            closeButton.className = 'modal-close';
            closeButton.innerHTML = '&times;';
            
            const videoContainer = document.createElement('div');
            videoContainer.className = 'video-container';
            videoContainer.innerHTML = '<div class="video-placeholder"><i class="fas fa-play"></i><p>Demo Video</p></div>';
            
            // Append elements
            modalContent.appendChild(closeButton);
            modalContent.appendChild(videoContainer);
            modal.appendChild(modalContent);
            document.body.appendChild(modal);
            
            // Add styles
            modal.style.display = 'flex';
            modal.style.position = 'fixed';
            modal.style.top = '0';
            modal.style.left = '0';
            modal.style.width = '100%';
            modal.style.height = '100%';
            modal.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
            modal.style.zIndex = '1000';
            modal.style.justifyContent = 'center';
            modal.style.alignItems = 'center';
            
            modalContent.style.backgroundColor = 'white';
            modalContent.style.borderRadius = '8px';
            modalContent.style.width = '80%';
            modalContent.style.maxWidth = '800px';
            modalContent.style.position = 'relative';
            modalContent.style.padding = '20px';
            
            closeButton.style.position = 'absolute';
            closeButton.style.top = '10px';
            closeButton.style.right = '15px';
            closeButton.style.fontSize = '28px';
            closeButton.style.fontWeight = 'bold';
            closeButton.style.cursor = 'pointer';
            
            videoContainer.style.width = '100%';
            videoContainer.style.padding = '56.25% 0 0 0';
            videoContainer.style.position = 'relative';
            
            const videoPlaceholder = videoContainer.querySelector('.video-placeholder');
            videoPlaceholder.style.position = 'absolute';
            videoPlaceholder.style.top = '0';
            videoPlaceholder.style.left = '0';
            videoPlaceholder.style.width = '100%';
            videoPlaceholder.style.height = '100%';
            videoPlaceholder.style.backgroundColor = '#f3f4f6';
            videoPlaceholder.style.display = 'flex';
            videoPlaceholder.style.flexDirection = 'column';
            videoPlaceholder.style.justifyContent = 'center';
            videoPlaceholder.style.alignItems = 'center';
            videoPlaceholder.style.color = '#4f46e5';
            
            const playIcon = videoPlaceholder.querySelector('i');
            playIcon.style.fontSize = '48px';
            playIcon.style.marginBottom = '10px';
            
            // Close modal functionality
            closeButton.addEventListener('click', function() {
                document.body.removeChild(modal);
            });
            
            // Close when clicking outside modal content
            modal.addEventListener('click', function(event) {
                if (event.target === modal) {
                    document.body.removeChild(modal);
                }
            });
        });
    }
    
    // Form submission for newsletter
    const newsletterForm = document.querySelector('.newsletter');
    
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const emailInput = this.querySelector('input[type="email"]');
            const email = emailInput.value.trim();
            
            if (email && isValidEmail(email)) {
                // Create toast notification
                const toast = document.createElement('div');
                toast.className = 'toast';
                toast.innerHTML = '<i class="fas fa-check-circle"></i> Thank you for subscribing!';
                
                // Add styles to toast
                toast.style.position = 'fixed';
                toast.style.bottom = '20px';
                toast.style.right = '20px';
                toast.style.backgroundColor = '#10b981';
                toast.style.color = 'white';
                toast.style.padding = '12px 20px';
                toast.style.borderRadius = '4px';
                toast.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
                toast.style.display = 'flex';
                toast.style.alignItems = 'center';
                toast.style.gap = '8px';
                toast.style.zIndex = '1000';
                toast.style.opacity = '0';
                toast.style.transform = 'translateY(20px)';
                toast.style.transition = 'opacity 0.3s, transform 0.3s';
                
                document.body.appendChild(toast);
                
                // Show toast
                setTimeout(() => {
                    toast.style.opacity = '1';
                    toast.style.transform = 'translateY(0)';
                }, 10);
                
                // Hide toast after 3 seconds
                setTimeout(() => {
                    toast.style.opacity = '0';
                    toast.style.transform = 'translateY(20px)';
                    
                    // Remove toast from DOM after animation
                    setTimeout(() => {
                        document.body.removeChild(toast);
                    }, 300);
                }, 3000);
                
                // Reset form
                emailInput.value = '';
            } else {
                // Invalid email handling
                emailInput.style.borderColor = '#ef4444';
                emailInput.style.boxShadow = '0 0 0 2px rgba(239, 68, 68, 0.2)';
                
                // Reset styles after 2 seconds
                setTimeout(() => {
                    emailInput.style.borderColor = '';
                    emailInput.style.boxShadow = '';
                }, 2000);
            }
        });
    }
    
    // Email validation function
    function isValidEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    }
    
    // Add button ripple effect
    const buttons = document.querySelectorAll('button');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const x = e.clientX - e.target.getBoundingClientRect().left;
            const y = e.clientY - e.target.getBoundingClientRect().top;
            
            const ripple = document.createElement('span');
            ripple.className = 'ripple';
            ripple.style.left = `${x}px`;
            ripple.style.top = `${y}px`;
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
});

// Add CSS for ripple effect
(function() {
    const style = document.createElement('style');
    style.textContent = `
        button {
            position: relative;
            overflow: hidden;
        }
        
        .ripple {
            position: absolute;
            border-radius: 50%;
            background-color: rgba(255, 255, 255, 0.7);
            transform: scale(0);
            animation: ripple 0.6s linear;
            pointer-events: none;
        }
        
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
        
        .modal {
            animation: fadeIn 0.3s ease;
        }
        
        .modal-content {
            animation: scaleIn 0.3s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes scaleIn {
            from { transform: scale(0.9); opacity: 0; }
            to { transform: scale(1); opacity: 1; }
        }
    `;
    document.head.appendChild(style);
})();