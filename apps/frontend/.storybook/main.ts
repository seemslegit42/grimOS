import type { StorybookConfig } from '@storybook/react-vite';

const config: StorybookConfig = {
  stories: [
    '../stories/**/*.mdx',
    '../stories/**/*.stories.@(js|jsx|mjs|ts|tsx)',
    '../components/ui/**/*.stories.@(js|jsx|mjs|ts|tsx)', // Add this line to include stories within component directories
  ],
  addons: [
    '@storybook/addon-links',
    '@storybook/addon-essentials',
    '@storybook/addon-onboarding',
    '@storybook/addon-interactions',
  ],
  framework: {
    name: '@storybook/react-vite',
    options: {},
  },
  docs: {
    autodocs: 'tag',
  },
  // Add this section to resolve aliases if you are using them in your project
  // and to potentially configure Tailwind CSS if needed.
  // If you have a vite.config.ts file, you might want to import and merge
  // its configuration here.
  // viteFinal: async (config) => {
  //   // Merge with your vite.config.ts or add custom configurations
  //   return config;
  // },
};
export default config;