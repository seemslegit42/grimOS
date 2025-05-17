// Replace Clerk's useUser hook with a simple placeholder
// Will need to be replaced with a real authentication solution in the future

export interface User {
  id: string;
  firstName?: string;
  lastName?: string;
  fullName?: string;
  username?: string;
  emailAddresses: {
    emailAddress: string;
  }[];
}

export function useUser() {
  // Placeholder for a user object
  const user: User = {
    id: "temp-user-id",
    firstName: "Demo",
    lastName: "User",
    fullName: "Demo User",
    username: "demo_user",
    emailAddresses: [{ emailAddress: "demo@example.com" }],
  };

  return {
    isLoaded: true,
    isSignedIn: true,
    user,
  };
}
