// Filepath: /home/brylow/grimOS/apps/frontend/middleware.ts
import type { NextRequest } from 'next/server';
import { NextResponse } from 'next/server';

// This function can be marked `async` if using `await` inside
export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Attempt to retrieve the persisted auth state directly from cookies if possible,
  // or make a decision based on a simple cookie flag set upon login.
  // Direct localStorage access is not available in middleware.
  // For this example, we'll assume a cookie named 'grimos-auth-status' is set to 'true' on login.
  // A more robust solution might involve a session cookie that is validated by a quick backend check.
  const isAuthenticatedCookie = request.cookies.get('grimos-auth-status');

  // Define public paths that don't require authentication
  const publicPaths = ['/login', '/register', '/']; // Add other public paths like /about, /pricing etc.

  // Check if the current path is public
  const isPublicPath = publicPaths.some(path => pathname === path || (path !== '/' && pathname.startsWith(path)));

  // If trying to access a protected route and not authenticated, redirect to login
  if (!isPublicPath && isAuthenticatedCookie?.value !== 'true') {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // If authenticated and trying to access login/register, redirect to a default authenticated page (e.g., dashboard)
  // This is optional and depends on desired UX
  if ((pathname === '/login' || pathname === '/register') && isAuthenticatedCookie?.value === 'true') {
    return NextResponse.redirect(new URL('/dashboard', request.url)); // Adjust '/dashboard' as needed
  }

  return NextResponse.next();
}

// See "Matching Paths" below to learn more
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - assets (static assets folder if you have one at root or in public)
     * - images (static images folder if you have one at root or in public)
     */
    '/((?!api|_next/static|_next/image|favicon.ico|assets|images).*)',
  ],
};
