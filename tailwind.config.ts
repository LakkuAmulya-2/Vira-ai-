import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./app/**/*.{js,ts,jsx,tsx,mdx}', './components/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: {
    extend: {
      colors: {
        ink: '#111111',
        paper: '#F8F7F4',
        accent: '#5E5CE6',
        mint: '#DDF7EB',
        lilac: '#EEEAFE',
      },
      boxShadow: {
        soft: '0 20px 60px rgba(17, 17, 17, 0.08)',
      },
      borderRadius: {
        '4xl': '2rem',
      },
    },
  },
  plugins: [],
};
export default config;
