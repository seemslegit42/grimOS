'use client';

import { useEffect } from 'react';
import { SignedIn, SignedOut, RedirectToSignIn } from '@clerk/nextjs';
import { BitBrewDashboard } from './components/BitBrewDashboard';

export default function BitBrewPage() {
  // Set page title
  useEffect(() => {
    document.title = 'BitBrew Intelligence | grimOS';
  }, []);

  return (
    <>
      <SignedIn>
        <BitBrewDashboard />
      </SignedIn>
      <SignedOut>
        <RedirectToSignIn />
      </SignedOut>
    </>
  );
}