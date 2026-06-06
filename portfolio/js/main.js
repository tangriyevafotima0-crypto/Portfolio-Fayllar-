/**
 * Portfolio Main JavaScript
 * Handles: theme toggle, navigation, project filtering, form validation,
 * loading animation, back-to-top button, and smooth scrolling.
 */

(function () {
    'use strict';

    // Theme Management
    const ThemeManager = {
        storageKey: 'portfolio-theme',
        body: document.body,
        toggleBtn: null,

        init() {
            this.toggleBtn = document.getElementById('theme-toggle');
            const savedTheme = localStorage.getItem(this.storageKey);
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

            if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
                this.setDark();
            } else {
                this.setLight();
            }

            if (this.toggleBtn) {
                this.toggleBtn.addEventListener('click', () => this.toggle());
            }
        },

        toggle() {
            if (this.body.classList.contains('dark-mode')) {
                this.setLight();
            } else {
                this.setDark();
            }
        },

        setDark() {
            this.body.classList.add('dark-mode');
            this.body.classList.remove('light-mode');
            localStorage.setItem(this.storageKey, 'dark');
            this.updateIcon('dark');
            if (window.particleSystem) {
                window.particleSystem.updateTheme(true);
            }
        },

        setLight() {
            this.body.classList.add('light-mode');
            this.body.classList.remove('dark-mode');
            localStorage.setItem(this.storageKey, 'light');
            this.updateIcon('light');
            if (window.particleSystem) {
                window.particleSystem.updateTheme(false);
            }
        },

        updateIcon(theme) {
            if (!this.toggleBtn) return;
            const icon = this.toggleBtn.querySelector('.theme-icon');
            if (icon) {
                icon.textContent = theme === 'dark' ? '☀️' : '🌙';
            }
        },
    };

    // Navigation Management
    const Navigation = {
        navbar: null,
        links: [],
        sections: [],
        mobileBtn: null,
        mobileMenu: null,

        init() {
            this.navbar = document.getElementById('nav');
            this.links = document.querySelectorAll('.nav-link');
            this.sections = document.querySelectorAll('section[id]');
            this.mobileBtn = document.getElementById('mobile-nav-btn');
            this.mobileMenu = document.getElementById('nav-mobile');

            this.setupScrollSpy();
            this.setupSmoothScroll();
            this.setupMobileMenu();
            this.setupNavbarShadow();
        },

        setupScrollSpy() {
            window.addEventListener('scroll', () => {
                let current = '';
                const navHeight = this.navbar ? this.navbar.offsetHeight : 80;

                this.sections.forEach(section => {
                    const sectionTop = section.offsetTop - navHeight - 100;
                    if (window.pageYOffset >= sectionTop) {
                        current = section.getAttribute('id');
                    }
                });

                this.links.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${current}`) {
                        link.classList.add('active');
                    }
                });
            });
        },

        setupSmoothScroll() {
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', (e) => {
                    const targetId = anchor.getAttribute('href');
                    if (targetId === '#') return;

                    const target = document.querySelector(targetId);
                    if (!target) return;

                    e.preventDefault();
                    const navHeight = this.navbar ? this.navbar.offsetHeight : 80;
                    const targetPos = target.offsetTop - navHeight - 20;

                    window.scrollTo({ top: targetPos, behavior: 'smooth' });

                    // Close mobile menu
                    if (this.mobileMenu) {
                        this.mobileMenu.classList.remove('open');
                    }
                });
            });
        },

        setupMobileMenu() {
            if (!this.mobileBtn || !this.mobileMenu) return;

            this.mobileBtn.addEventListener('click', () => {
                this.mobileMenu.classList.toggle('open');
                this.mobileBtn.classList.toggle('active');
            });
        },

        setupNavbarShadow() {
            window.addEventListener('scroll', () => {
                if (!this.navbar) return;
                if (window.scrollY > 50) {
                    this.navbar.classList.add('nav-scrolled');
                } else {
                    this.navbar.classList.remove('nav-scrolled');
                }
            });
        },
    };

    // Project Filtering
    const ProjectFilter = {
        buttons: [],
        cards: [],

        init() {
            this.buttons = document.querySelectorAll('.filter-btn');
            this.cards = document.querySelectorAll('.project-card');

            this.buttons.forEach(btn => {
                btn.addEventListener('click', () => this.filter(btn));
            });
        },

        filter(activeBtn) {
            const category = activeBtn.dataset.filter;

            this.buttons.forEach(btn => btn.classList.remove('active'));
            activeBtn.classList.add('active');

            this.cards.forEach(card => {
                const cardCategory = card.dataset.category;

                if (category === 'all' || cardCategory === category) {
                    card.style.display = '';
                    card.style.animation = 'fadeInUp 0.5s ease forwards';
                } else {
                    card.style.display = 'none';
                }
            });
        },
    };

    // Contact Form
    const ContactForm = {
        form: null,

        init() {
            this.form = document.getElementById('contact-form');
            if (!this.form) return;

            this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        },

        handleSubmit(e) {
            e.preventDefault();

            const fields = this.form.querySelectorAll('[required]');
            let valid = true;

            fields.forEach(field => {
                if (!field.value.trim()) {
                    valid = false;
                    field.classList.add('error');
                } else {
                    field.classList.remove('error');
                }
            });

            const emailField = this.form.querySelector('[type="email"]');
            if (emailField && !this.isValidEmail(emailField.value)) {
                valid = false;
                emailField.classList.add('error');
            }

            if (valid) {
                const btn = this.form.querySelector('button[type="submit"]');
                btn.textContent = 'Message Sent!';
                btn.classList.add('success');
                setTimeout(() => {
                    btn.textContent = 'Send Message';
                    btn.classList.remove('success');
                    this.form.reset();
                }, 3000);
            }
        },

        isValidEmail(email) {
            return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
        },
    };

    // Back to Top Button
    const BackToTop = {
        button: null,

        init() {
            this.button = document.getElementById('back-to-top');
            if (!this.button) return;

            window.addEventListener('scroll', () => {
                if (window.pageYOffset > 500) {
                    this.button.classList.add('visible');
                } else {
                    this.button.classList.remove('visible');
                }
            });

            this.button.addEventListener('click', () => {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
        },
    };

    // Loading Animation
    const Loader = {
        init() {
            const loader = document.getElementById('loader');
            if (!loader) return;

            window.addEventListener('load', () => {
                setTimeout(() => {
                    loader.classList.add('hidden');
                    document.body.classList.remove('loading');
                }, 800);
            });
        },
    };

    // Scroll Indicator
    const ScrollIndicator = {
        init() {
            const indicator = document.getElementById('scroll-progress');
            if (!indicator) return;

            window.addEventListener('scroll', () => {
                const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
                const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
                const scrolled = (winScroll / height) * 100;
                indicator.style.width = scrolled + '%';
            });
        },
    };

    // Initialize everything when DOM is ready
    document.addEventListener('DOMContentLoaded', () => {
        Loader.init();
        ThemeManager.init();
        Navigation.init();
        ProjectFilter.init();
        ContactForm.init();
        BackToTop.init();
        ScrollIndicator.init();
    });
})();
