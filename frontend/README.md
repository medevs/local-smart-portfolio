# Portfolio Frontend

Modern Next.js 15 portfolio website with TypeScript, TailwindCSS, and shadcn/ui.

## 🚀 Getting Started

### Prerequisites

- Node.js 18+
- pnpm (recommended) or npm

### Installation

```bash
# Install dependencies
pnpm install

# Run development server
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) to view the portfolio.

## 📁 Project Structure

```
frontend/
├── app/                  # Next.js app router pages
│   ├── page.tsx         # Home page
│   ├── about/           # About page
│   ├── projects/        # Projects page
│   ├── contact/         # Contact page
│   ├── homelab/         # Homelab journey page
│   └── admin/           # Admin dashboard
│
├── components/          # React components
│   ├── ui/              # shadcn/ui components
│   ├── sections/        # Page sections
│   ├── layout/          # Layout components
│   └── chat/            # Chat components
│
├── data/                # Static data files
│   ├── personal.ts      # Personal information
│   ├── projects.ts      # Projects data
│   ├── timeline.ts      # Timeline data
│   └── ...
│
└── lib/                 # Utilities
    ├── api.ts           # API client
    └── utils.ts         # Helper functions
```

## 🎨 Customization

### Update Your Data

All personal data is centralized in `data/` directory:

- **Personal Info**: Edit `data/personal.ts`
- **Projects**: Edit `data/projects.ts`
- **Timeline**: Edit `data/timeline.ts`
- **Skills**: Edit `data/skills.tsx`
- **Page Content**: Edit `data/pageContent.ts`

### Styling

The portfolio uses TailwindCSS with a custom amber/gold theme. Customize colors in:
- `app/globals.css` - Global styles and CSS variables
- Component files - Tailwind utility classes

## 🛠️ Available Scripts

```bash
# Development
pnpm dev              # Start dev server

# Production
pnpm build            # Build for production
pnpm start            # Start production server

# Code Quality
pnpm lint             # Run ESLint
pnpm type-check       # TypeScript type checking
```

## 📦 Dependencies

### Core
- **Next.js 15.5.5** - React framework
- **TypeScript** - Type safety
- **TailwindCSS 4.0** - Styling
- **Framer Motion** - Animations

### UI Components
- **shadcn/ui** - Component library
- **Radix UI** - Accessible primitives
- **Lucide React** - Icons
- **React Icons** - Additional icons

### State & Data
- **Zustand** - State management
- **Axios** - HTTP client

## 🔗 Environment Variables

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📱 Pages

- `/` - Home page with hero, skills, and featured projects
- `/about` - About page with timeline and tech stack
- `/projects` - All projects showcase
- `/contact` - Contact form
- `/homelab` - Homelab journey and infrastructure
- `/admin` - Admin dashboard (requires API key)

## 🎯 Features

- ✅ Responsive design (mobile-first)
- ✅ Dark theme with amber accents
- ✅ Smooth animations with Framer Motion
- ✅ Real-time system metrics display
- ✅ LLM performance benchmarks
- ✅ Chat interface integration
- ✅ SEO optimized

## 📄 License

MIT License
