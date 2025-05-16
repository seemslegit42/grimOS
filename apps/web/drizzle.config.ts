
import type { Config } from "drizzle-kit";

export default {
  schema: "./packages/shared/schema.ts",
  out: "./drizzle",
} satisfies Config;
