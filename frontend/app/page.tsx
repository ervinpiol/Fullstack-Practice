"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    // Redirect the user to /auth/login immediately upon mounting
    router.replace("/auth/login");
  }, [router]);

  // You can return a null or a loading indicator while the redirect happens
  return (
    <div>
      <p>Redirecting to login...</p>
    </div>
  );
}
