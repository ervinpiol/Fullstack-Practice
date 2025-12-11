import { createBrowserClient } from "@supabase/ssr";
// eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ6eXh3c3dydGNkYXR1d3l2aG12Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQ4NjU3NjksImV4cCI6MjA4MDQ0MTc2OX0.ONCSKcA9EypNPd2ajiF3KGU5HetxEB3Hhdi-aXaoRIs

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!
  );
}
