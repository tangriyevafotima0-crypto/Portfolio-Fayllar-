# Portfolio - Personal Developer Portfolio

A modern, responsive portfolio website showcasing three years of coding projects and growth. Features smooth animations, particle effects, dark/light mode, and a professional design that demonstrates advanced frontend development skills.

## Live Features

### Visual Effects
- **Particle Background**: Animated canvas-based particle system with mouse interaction in the hero section
- **Typed Text Effect**: Auto-typing role titles with cursor blink animation
- **Scroll Animations**: Fade-in, slide-in, and scale effects triggered on scroll
- **Progress Bars**: Animated skill bars that fill when scrolled into view
- **Parallax Elements**: Subtle depth effect on scroll

### Interactivity
- **Dark/Light Mode**: Smooth theme toggle with localStorage persistence and OS preference detection
- **Project Filtering**: Filter portfolio projects by year (Year 1, Year 2, Year 3)
- **Smooth Navigation**: Active section highlighting and smooth scroll to sections
- **Contact Form**: Client-side validation with visual feedback
- **Back to Top**: Appears on scroll with smooth animation
- **Scroll Progress**: Top bar showing page scroll percentage
- **Loading Animation**: Professional loader on initial page load

### Design
- **Mobile-First**: Fully responsive from 320px to 4K
- **Custom CSS Properties**: Easy theming with CSS variables
- **Modern Typography**: Inter font family with careful weight hierarchy
- **Accessible**: Semantic HTML, ARIA labels, keyboard-navigable

## Tech Stack

- **HTML5** - Semantic, accessible markup
- **CSS3** - Custom properties, Grid, Flexbox, animations
- **Vanilla JavaScript** - ES6+, classes, modules pattern
- **Canvas API** - Particle system animation
- **Google Fonts** - Inter typeface

## Project Structure

```
portfolio/
├── index.html              # Single-page portfolio
├── css/
│   ├── style.css           # Main styles (500+ lines)
│   └── animations.css      # Keyframes and transitions
├── js/
│   ├── main.js             # App logic, theme, navigation, filtering
│   ├── animations.js       # Scroll animations, typed effect, counters
│   └── particles.js        # Canvas particle system
├── assets/
│   └── .gitkeep            # Placeholder for images
└── README.md
```

## Getting Started

No build tools required. Simply serve the files:

```bash
# Option 1: Python server
cd portfolio
python -m http.server 8000

# Option 2: Node server
npx serve .

# Option 3: VS Code Live Server extension
# Right-click index.html -> Open with Live Server

# Then visit: http://localhost:8000
```

## Deployment

### GitHub Pages
1. Push to a GitHub repository
2. Go to Settings > Pages
3. Select source branch (main)
4. Site will be live at `https://username.github.io/portfolio`

### Netlify
1. Connect your GitHub repository
2. Deploy settings: no build command needed
3. Publish directory: `/portfolio`

### Vercel
1. Import the project
2. Framework: Other
3. Output directory: `.`

## Customization

### Colors
Edit CSS variables in `css/style.css`:
```css
:root {
    --accent-primary: #6366f1;  /* Main brand color */
    --accent-secondary: #8b5cf6; /* Secondary accent */
}
```

### Content
- Update personal information in `index.html`
- Replace placeholder text and project descriptions
- Add actual project links
- Replace photo placeholder with real image
- Update social media links

### Particle Effect
Configure in `js/particles.js`:
```javascript
this.config = {
    particleCount: 80,      // Number of particles
    speed: 0.5,             // Movement speed
    connectionDistance: 120, // Line connection range
};
```

## Browser Support

- Chrome 88+
- Firefox 85+
- Safari 14+
- Edge 88+

## Performance

- No external JavaScript dependencies
- Minimal CSS with no framework overhead
- Canvas animation uses requestAnimationFrame
- IntersectionObserver for efficient scroll detection
- Images lazy-loaded when added

## License

MIT License - This is the capstone project of a 3-year coding portfolio.
