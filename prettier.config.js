module.exports = {
  plugins: ['prettier-plugin-tailwindcss'],
  trailingComma: 'es5',
  tabWidth: 2,
  printWidth: 120,
  semi: false,
  singleQuote: true,
  jsxSingleQuote: false,
  bracketSpacing: true,
  bracketSameLine: false,
  arrowParens: 'always',
  endOfLine: 'lf',
  overrides: [
    {
      files: '*.{json,md}',
      options: {
        tabWidth: 2,
      },
    },
    {
      files: '*.py',
      options: {
        tabWidth: 4,
      },
    },
  ],
  tailwindConfig: './tailwind.config.ts',
  tailwindFunctions: ['cn', 'clsx', 'cva'],
}
