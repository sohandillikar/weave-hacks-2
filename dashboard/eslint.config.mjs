import { FlatCompat } from "@eslint/eslintrc";

const compat = new FlatCompat({ baseDirectory: import.meta.dirname });

const eslintConfig = [
  // Global ignores - these patterns are excluded from linting
  {
    ignores: [".next/", "node_modules/", "dist/", "build/", "*.tsbuildinfo", "next-env.d.ts"]
  },
  ...compat.config({ extends: ["next/core-web-vitals", "next/typescript", "prettier"] }),
  { rules: { "no-console": "warn" } }
];

export default eslintConfig;
