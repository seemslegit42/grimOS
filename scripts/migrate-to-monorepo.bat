@echo off
echo Starting migration to Turborepo monorepo structure...

REM Create necessary directories if they don't exist
mkdir apps\frontend\app 2>nul
mkdir apps\frontend\components 2>nul
mkdir apps\frontend\public 2>nul
mkdir apps\frontend\styles 2>nul
mkdir apps\backend\app 2>nul
mkdir packages\shared\src 2>nul

REM Move Next.js frontend files
echo Moving Next.js frontend files...
xcopy /Y app\layout.tsx apps\frontend\app\
xcopy /Y app\page.tsx apps\frontend\app\
xcopy /Y /E styles\* apps\frontend\styles\
xcopy /Y /E components\* apps\frontend\components\
xcopy /Y /E public\* apps\frontend\public\ 2>nul
xcopy /Y next.config.ts apps\frontend\next.config.js
xcopy /Y tsconfig.json apps\frontend\
xcopy /Y postcss.config.js apps\frontend\
xcopy /Y tailwind.config.js apps\frontend\

REM Move FastAPI backend files
echo Moving FastAPI backend files...
xcopy /Y /E app\fastapi-backend\backend\* apps\backend\
xcopy /Y /E app\fastapi-backend\backend\app\* apps\backend\app\

REM Install dependencies
echo Installing dependencies...
call pnpm install

REM Build shared package
echo Building shared package...
call pnpm --filter @bitbrew/shared build

echo Migration completed successfully!
echo Please review the new structure in the apps/ and packages/ directories.
echo You can now run 'pnpm dev' to start the development servers.