# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Essential Commands

```bash
# Install dependencies
npm install

# Run development server (http://localhost:3000)
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linting
npm run lint

# Type checking
npm run typecheck
```

## Architecture Overview

This is a Next.js 15 starter template with TypeScript, Tailwind CSS, and Supabase integration. Perfect for creating modern landing pages, SaaS applications, or any web project requiring:

- **Next.js 15.3.3** with App Router
- **TypeScript** with strict mode enabled
- **Tailwind CSS** with custom design system
- **Framer Motion** for animations
- **Supabase** integration ready
- **Email capture** with analytics

### Key Architectural Decisions

1. **Component Architecture**: All components in `src/components/` are client-side (`'use client'`) React functional components with TypeScript. Each component is self-contained with animations and styling.

2. **Design System**: Custom CSS variables defined in `globals.css`:
   - Primary color: `rgb(218, 50, 41)` (customizable)
   - Secondary color: `rgb(92, 38, 35)` (customizable)
   - Accent color: `rgb(224, 57, 47)` (customizable)
   - Dark theme: `rgb(23, 23, 23)`
   - Custom utilities: `btn-primary`, `btn-secondary`, `gradient-text`, `glass-effect`

3. **Path Aliases**: `@/*` maps to `./src/*` for cleaner imports

4. **Page Structure**: Modular landing page composed of reusable sections:
   - Navigation
   - Hero with animated text
   - Video Preview
   - Features section
   - Tech Stack showcase
   - Testimonials
   - Instructor/Team section
   - Pricing tiers
   - FAQ accordion
   - Email capture
   - Call-to-action
   - Footer

## Customization Guide

### 1. Branding & Colors

Update the CSS variables in `src/app/globals.css`:

```css
:root {
  --brand-primary: 218 50 41;    /* Your primary color */
  --brand-secondary: 92 38 35;   /* Your secondary color */
  --brand-accent: 224 57 47;     /* Your accent color */
}
```

### 2. Logo & Assets

Replace the placeholder logos in `/public/assets/logos/`:
- `logo-light.svg` - Full logo for light theme
- `logo-dark.svg` - Full logo for dark theme  
- `icon-light.svg` - Icon only for mobile (light theme)
- `icon-dark.svg` - Icon only for mobile (dark theme)

### 3. Content Updates

Main content files to customize:
- `src/components/HeroOptimized.tsx` - Hero section with rotating text
- `src/components/Features.tsx` - Product features
- `src/components/Pricing.tsx` - Pricing tiers
- `src/components/Testimonials.tsx` - Customer testimonials
- `src/components/FAQ.tsx` - Frequently asked questions

### 4. Environment Variables

Required for production (create `.env.local`):

```bash
# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key

# Email Integrations (optional)
KIT_API_KEY=your_kit_v4_api_key
SENDGRID_API_KEY=your_sendgrid_api_key
SENDGRID_TEMPLATE_ID=your_sendgrid_template_id

# Analytics (optional)
NEXT_PUBLIC_MICROSOFT_CLARITY_ID=your_clarity_project_id
```

## Template Features

### ✅ Included Components
- Responsive navigation with theme toggle
- Animated hero section with rotating text
- Video preview placeholder
- Feature showcase with expandable cards
- Technology stack display
- Testimonials carousel
- Pricing comparison table
- FAQ accordion
- Email capture form
- Call-to-action sections
- Footer with links

### ✅ Technical Features
- Dark/light mode with system preference detection
- Fully responsive design (mobile-first)
- TypeScript with strict mode
- ESLint + Prettier configuration
- Framer Motion animations
- Supabase integration setup
- Email marketing integration ready
- SEO optimization
- Performance optimized

### ✅ Developer Experience
- Hot reload development server
- TypeScript IntelliSense
- Component testing setup
- Automated code formatting
- Git pre-commit hooks ready

## Getting Started

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Update Branding**
   - Replace logos in `/public/assets/logos/`
   - Update colors in `src/app/globals.css`
   - Customize content in component files

3. **Configure Integrations**
   - Set up Supabase project
   - Add environment variables
   - Configure email services (optional)

4. **Start Development**
   ```bash
   npm run dev
   ```

5. **Customize Content**
   - Update hero text and messaging
   - Add your features and pricing
   - Customize testimonials and FAQ

## Deployment

This template is optimized for deployment on:
- **Vercel** (recommended)
- **Netlify**
- **AWS Amplify**
- Any Node.js hosting provider

Build command: `npm run build`
Start command: `npm start`

## Support

For issues or questions about this template:
1. Check the component documentation
2. Review the example implementations
3. Consult the Next.js and Tailwind CSS docs
4. Open an issue in your project repository

---

**Note**: This is a starter template. Customize it to match your brand and requirements. All placeholder content should be replaced with your actual content.