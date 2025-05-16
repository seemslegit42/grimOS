/// <reference types="next" />
/// <reference types="next/image-types/global" />

// NOTE: This file should not be edited
// see https://nextjs.org/docs/app/api-reference/config/typescript for more information.
declare namespace NodeJS {
  interface ProcessEnv {
    NEXT_PUBLIC_N8N_BASE_URL: string | undefined;
    N8N_API_KEY: string | undefined;
  }
}
