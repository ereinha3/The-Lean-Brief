# The Lean Brief - Frontend 🎨

> **Modern React Interface for Market Intelligence**

A beautiful, responsive React TypeScript frontend for The Lean Brief that displays AI-processed financial news in an intuitive, organized interface.

![React](https://img.shields.io/badge/React-18.2.0-blue)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4.0-blue)

## 🎯 Features

- **📱 Responsive Design** - Works perfectly on desktop, tablet, and mobile
- **⚡ Real-time Updates** - Live data fetching with manual refresh capability
- **🎨 Modern UI** - Beautiful interface with smooth animations and transitions
- **🔍 Interactive Navigation** - Drill-down from sectors to topics to detailed views
- **📊 Visual Hierarchy** - Clear information architecture with importance scoring
- **♿ Accessibility** - WCAG compliant with keyboard navigation support

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React App     │    │   TypeScript    │    │   Tailwind CSS  │
│                 │    │                 │    │                 │
│ • Components    │───▶│ • Type Safety   │◀───│ • Utility First │
│ • State Mgmt    │    │ • Interfaces    │    │ • Responsive    │
│ • Routing       │    │ • Error Handling│    │ • Dark Mode     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📋 Prerequisites

- **Node.js 16+** - [Download here](https://nodejs.org/)
- **npm 8+** or **yarn 1.22+**
- **Backend API** - The Lean Brief backend running on port 5000

## 🚀 Quick Start

### 1. Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Or using yarn
yarn install
```

### 2. Configuration

The frontend automatically connects to the backend API at `http://localhost:5000`. If your backend is running on a different URL, update the API endpoint in `src/App.tsx`:

```typescript
// In src/App.tsx, line ~25
const response = await fetch('http://localhost:5000/api/summarize_news', {
```

### 3. Development Server

```bash
# Start development server
npm start

# Or using yarn
yarn start
```

The application will open at [http://localhost:3000](http://localhost:3000).

### 4. Build for Production

```bash
# Create optimized production build
npm run build

# Or using yarn
yarn build
```

## 📁 Project Structure

```
frontend/
├── public/                 # Static assets
│   ├── index.html         # Main HTML template
│   ├── favicon.ico        # App icon
│   └── manifest.json      # PWA manifest
├── src/                   # Source code
│   ├── App.tsx           # Main React component
│   ├── index.tsx         # React entry point
│   ├── types.ts          # TypeScript type definitions
│   ├── index.css         # Global styles
│   └── reportWebVitals.ts # Performance monitoring
├── package.json          # Dependencies and scripts
├── tsconfig.json         # TypeScript configuration
└── README.md            # This file
```

## 🎨 UI Components

### Main Layout
- **Header** - App title and refresh button
- **Main Content** - Dynamic content area
- **Footer** - Copyright and links

### Sector Cards
- **Landing Page** - Overview of all market sectors
- **Interactive Cards** - Click to explore sector details
- **Visual Indicators** - Importance and activity levels

### Topic Views
- **Sector Detail** - List of topics within a sector
- **Topic Cards** - Individual topic information
- **Importance Scoring** - Visual importance indicators

### Modal Dialogs
- **Topic Details** - Comprehensive topic information
- **Source Links** - Direct links to original articles
- **Responsive Design** - Works on all screen sizes

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the frontend directory:

```env
# Backend API URL
REACT_APP_API_URL=http://localhost:5000

# Environment
REACT_APP_ENV=development

# Analytics (optional)
REACT_APP_GA_TRACKING_ID=your-ga-id
```

### TypeScript Configuration

The project uses strict TypeScript configuration:

```json
{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noFallthroughCasesInSwitch": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx"
  }
}
```

## 🚀 Deployment

### Build Process

```bash
# Create production build
npm run build

# The build folder will contain:
# - index.html
# - static/css/ (minified CSS)
# - static/js/ (minified JavaScript)
# - static/media/ (optimized assets)
```

### Static Hosting

#### Netlify

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
netlify deploy --prod --dir=build
```

#### Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

#### GitHub Pages

```bash
# Add homepage to package.json
{
  "homepage": "https://yourusername.github.io/theleanbrief"
}

# Install gh-pages
npm install --save-dev gh-pages

# Add deploy script to package.json
{
  "scripts": {
    "deploy": "gh-pages -d build"
  }
}

# Deploy
npm run deploy
```

### Docker Deployment

```dockerfile
# Multi-stage build
FROM node:16-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

```bash
# Build and run
docker build -t theleanbrief-frontend .
docker run -p 80:80 theleanbrief-frontend
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm test -- --coverage
```

### Test Structure

```typescript
// Example test
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders app title', () => {
  render(<App />);
  const titleElement = screen.getByText(/The Lean Brief/i);
  expect(titleElement).toBeInTheDocument();
});
```

## 📊 Performance

### Optimization Features

- **Code Splitting** - Automatic code splitting with React.lazy()
- **Tree Shaking** - Unused code elimination
- **Minification** - Compressed production builds
- **Caching** - Optimized asset caching
- **Lazy Loading** - Components loaded on demand

### Performance Monitoring

```typescript
// reportWebVitals.ts
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

const reportWebVitals = (onPerfEntry?: any) => {
  if (onPerfEntry && onPerfEntry instanceof Function) {
    getCLS(onPerfEntry);
    getFCP(onPerfEntry);
    getLCP(onPerfEntry);
    getTTFB(onPerfEntry);
  }
};

export default reportWebVitals;
```

## 🔒 Security

### Best Practices

1. **HTTPS Only** - Force HTTPS in production
2. **Content Security Policy** - Implement CSP headers
3. **Input Sanitization** - Validate all user inputs
4. **Dependency Scanning** - Regular security audits

### Security Headers

```html
<!-- In public/index.html -->
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline';">
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta http-equiv="X-Frame-Options" content="DENY">
```

## 🐛 Troubleshooting

### Common Issues

#### Build Errors
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### TypeScript Errors
```bash
# Check TypeScript configuration
npx tsc --noEmit

# Fix type issues
npm run build
```

#### API Connection Issues
```bash
# Check backend is running
curl http://localhost:5000/

# Check CORS configuration
# Ensure backend has CORS enabled for frontend domain
```

### Debug Mode

```bash
# Enable React DevTools
npm install -g react-devtools

# Start DevTools
react-devtools
```

## 📱 Responsive Design

### Breakpoints

```css
/* Tailwind CSS breakpoints */
sm: 640px   /* Small devices */
md: 768px   /* Medium devices */
lg: 1024px  /* Large devices */
xl: 1280px  /* Extra large devices */
2xl: 1536px /* 2X large devices */
```

### Mobile Optimization

- Touch-friendly interface
- Optimized loading times
- Reduced bundle size
- Progressive Web App features

## 🎨 Styling

### Tailwind CSS

The project uses Tailwind CSS for styling:

```css
/* Custom styles in index.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom component classes */
@layer components {
  .btn-primary {
    @apply px-4 py-2 bg-indigo-500 text-white rounded-lg hover:bg-indigo-600;
  }
}
```

### Design System

- **Colors**: Indigo primary, gray secondary
- **Typography**: Inter font family
- **Spacing**: Consistent 4px grid system
- **Shadows**: Subtle elevation system

## 🔄 State Management

### React Hooks

```typescript
// Example state management
const [newsData, setNewsData] = useState<NewsData | null>(null);
const [loading, setLoading] = useState<boolean>(true);
const [error, setError] = useState<string | null>(null);
```

### Data Flow

1. **API Calls** → Fetch data from backend
2. **State Updates** → Update React state
3. **UI Re-renders** → Display updated data
4. **User Interactions** → Trigger new API calls

## 📈 Analytics

### Google Analytics

```typescript
// Add to index.tsx
import ReactGA from 'react-ga';

ReactGA.initialize('GA_TRACKING_ID');
ReactGA.pageview(window.location.pathname);
```

### Custom Events

```typescript
// Track user interactions
const handleSectorClick = (sectorName: string) => {
  ReactGA.event({
    category: 'Navigation',
    action: 'Sector Click',
    label: sectorName
  });
  setSelectedSector(sectorName);
};
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Guidelines

- Follow TypeScript best practices
- Use functional components with hooks
- Maintain consistent code style
- Add proper error handling
- Write meaningful commit messages

## 📝 License

This project is licensed under the MIT License.

---

**For more information, see the main [README.md](../README.md)**
