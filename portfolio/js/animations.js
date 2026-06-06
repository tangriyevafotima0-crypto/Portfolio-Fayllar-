/**
 * Scroll-triggered Animations Module
 * Handles reveal animations, parallax effects, and intersection observers.
 */

class ScrollAnimations {
    constructor() {
        this.animatedElements = [];
        this.parallaxElements = [];
        this.progressBars = [];
        this.observer = null;

        this.init();
    }

    init() {
        this.setupIntersectionObserver();
        this.collectAnimatedElements();
        this.collectParallaxElements();
        this.setupProgressBars();
        this.addScrollListener();
    }

    setupIntersectionObserver() {
        const options = {
            threshold: 0.15,
            rootMargin: '0px 0px -80px 0px',
        };

        this.observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const el = entry.target;
                    const delay = el.dataset.delay || 0;

                    setTimeout(() => {
                        el.classList.add('revealed');
                    }, parseInt(delay));

                    this.observer.unobserve(el);
                }
            });
        }, options);
    }

    collectAnimatedElements() {
        const elements = document.querySelectorAll('[data-animate]');
        elements.forEach(el => {
            el.classList.add('animate-hidden');
            this.observer.observe(el);
        });
    }

    collectParallaxElements() {
        this.parallaxElements = document.querySelectorAll('[data-parallax]');
    }

    setupProgressBars() {
        this.progressBars = document.querySelectorAll('.skill-progress');

        const progressObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const bar = entry.target;
                    const width = bar.dataset.width;
                    setTimeout(() => {
                        bar.style.width = width + '%';
                    }, 300);
                    progressObserver.unobserve(bar);
                }
            });
        }, { threshold: 0.5 });

        this.progressBars.forEach(bar => {
            bar.style.width = '0%';
            progressObserver.observe(bar);
        });
    }

    addScrollListener() {
        let ticking = false;

        window.addEventListener('scroll', () => {
            if (!ticking) {
                requestAnimationFrame(() => {
                    this.updateParallax();
                    ticking = false;
                });
                ticking = true;
            }
        });
    }

    updateParallax() {
        const scrollY = window.pageYOffset;

        this.parallaxElements.forEach(el => {
            const speed = parseFloat(el.dataset.parallax) || 0.5;
            const rect = el.getBoundingClientRect();
            const elementTop = rect.top + scrollY;
            const offset = (scrollY - elementTop) * speed;

            if (rect.top < window.innerHeight && rect.bottom > 0) {
                el.style.transform = `translateY(${offset}px)`;
            }
        });
    }
}


/**
 * Typed text effect for hero section
 */
class TypedEffect {
    constructor(elementId, texts, options = {}) {
        this.element = document.getElementById(elementId);
        if (!this.element) return;

        this.texts = texts;
        this.typeSpeed = options.typeSpeed || 80;
        this.deleteSpeed = options.deleteSpeed || 50;
        this.pauseDelay = options.pauseDelay || 2000;
        this.currentIndex = 0;
        this.currentChar = 0;
        this.isDeleting = false;

        this.type();
    }

    type() {
        const currentText = this.texts[this.currentIndex];

        if (this.isDeleting) {
            this.element.textContent = currentText.substring(0, this.currentChar - 1);
            this.currentChar--;
        } else {
            this.element.textContent = currentText.substring(0, this.currentChar + 1);
            this.currentChar++;
        }

        let timeout = this.isDeleting ? this.deleteSpeed : this.typeSpeed;

        if (!this.isDeleting && this.currentChar === currentText.length) {
            timeout = this.pauseDelay;
            this.isDeleting = true;
        } else if (this.isDeleting && this.currentChar === 0) {
            this.isDeleting = false;
            this.currentIndex = (this.currentIndex + 1) % this.texts.length;
            timeout = 500;
        }

        setTimeout(() => this.type(), timeout);
    }
}


/**
 * Counter animation for stats numbers
 */
class CounterAnimation {
    constructor(selector) {
        this.elements = document.querySelectorAll(selector);
        this.init();
    }

    init() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.animateCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        this.elements.forEach(el => observer.observe(el));
    }

    animateCounter(element) {
        const target = parseInt(element.dataset.count);
        const duration = 2000;
        const step = target / (duration / 16);
        let current = 0;

        const update = () => {
            current += step;
            if (current >= target) {
                element.textContent = target + (element.dataset.suffix || '');
                return;
            }
            element.textContent = Math.floor(current) + (element.dataset.suffix || '');
            requestAnimationFrame(update);
        };

        update();
    }
}


// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    window.scrollAnimations = new ScrollAnimations();

    // Typed effect for hero
    new TypedEffect('typed-text', [
        'Full-Stack Developer',
        'Python Enthusiast',
        'AI Explorer',
        'Creative Problem Solver',
    ]);

    // Counter animations
    new CounterAnimation('[data-count]');
});
