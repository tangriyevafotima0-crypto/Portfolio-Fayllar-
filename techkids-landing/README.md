# TechKids Landing Page

A modern, responsive landing page for a kids coding school. Built with Tailwind CSS and vanilla JavaScript, featuring smooth animations, an interactive FAQ, and a clean professional design.

## Live Sections

- **Hero** - Bold headline with CTA buttons and code snippet preview
- **Features** - 4 benefit cards with icons (Fun Learning, Expert Teachers, Small Groups, Certificates)
- **Curriculum** - Course cards organized by age group (Scratch, Python, Web Dev, AI)
- **Testimonials** - 3 parent testimonials with ratings and avatars
- **Pricing** - 3-tier pricing cards (Basic, Pro, Premium) with feature comparison
- **FAQ** - 5 expandable questions with accordion functionality
- **Contact** - Form with validation + contact info and social links
- **Footer** - Site links, course links, social links, copyright

## Tech Stack

- **HTML5** - Semantic markup with accessibility considerations
- **Tailwind CSS** - Utility-first CSS via CDN with custom color configuration
- **Custom CSS** - Scroll animations, FAQ transitions, custom scrollbar
- **JavaScript** - Vanilla JS for all interactions (no dependencies)

## Features

- Fully responsive (mobile-first design)
- Smooth scroll navigation with active section highlighting
- Scroll-triggered fade-in animations (IntersectionObserver)
- FAQ accordion with smooth expand/collapse
- Mobile hamburger menu with animated toggle
- Contact form with client-side validation
- Navbar shadow on scroll
- Custom scrollbar styling

## Getting Started

Simply open `index.html` in a browser. No build step required.

```bash
# Quick start
open index.html

# Or use a local server
python -m http.server 8000
# Then visit http://localhost:8000
```

## Customization

Colors and theme are configured in the Tailwind config within `index.html`:

```javascript
tailwind.config = {
    theme: {
        extend: {
            colors: {
                primary: '#6C63FF',
                secondary: '#FF6584',
                accent: '#43B97F',
            }
        }
    }
}
```

## Browser Support

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## License

MIT License - Built as a learning project.
