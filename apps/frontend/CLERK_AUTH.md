# Clerk Authentication Setup for grimOS

This project uses [Clerk](https://clerk.com/) for authentication with Next.js App Router.

## Setup Instructions

1. Sign up for a Clerk account at [clerk.com](https://clerk.com/)
2. Create a new application in Clerk dashboard
3. Get your API keys from Clerk dashboard
4. Add them to your `.env.local` file:

```
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_publishable_key
CLERK_SECRET_KEY=your_secret_key
```

5. Install Clerk dependencies: 
   ```bash
   pnpm add @clerk/nextjs@latest
   ```

6. The middleware and other necessary files are already set up in this project.

## Authentication Flow

- Authentication is managed by Clerk middleware
- Most pages in the Dashboard section require authentication
- Sign-in/Sign-up pages are customized with grimOS UI
- User profile information can be accessed at the `/profile` route

## Protected Routes

The following routes are protected and require authentication:
- `/dashboard/*`
- `/profile`

## Authentication UI Components

The following Clerk components are used:
- `<SignInButton>` - Renders a sign-in button
- `<SignUpButton>` - Renders a sign-up button
- `<UserButton>` - Renders the user button to manage account
- `<SignedIn>` - Only renders content if user is signed in
- `<SignedOut>` - Only renders content if user is not signed in

## Custom Authentication Pages

- `/sign-in` - Custom sign-in page
- `/sign-up` - Custom sign-up page

## Additional Resources

- [Clerk Documentation](https://clerk.com/docs)
- [Clerk Next.js Documentation](https://clerk.com/docs/quickstarts/nextjs)
