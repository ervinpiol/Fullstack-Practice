// "use client";

// import {
//   createContext,
//   useContext,
//   useEffect,
//   useState,
//   ReactNode,
// } from "react";
// import axios from "axios";
// import { useRouter, usePathname } from "next/navigation";

// interface AuthContextType {
//   user: any;
//   loading: boolean;
// }

// const AuthContext = createContext<AuthContextType>({
//   user: null,
//   loading: true,
// });

// export const AuthProvider = ({ children }: { children: ReactNode }) => {
//   const [user, setUser] = useState<any>(null);
//   const [loading, setLoading] = useState(true);

//   const router = useRouter();
//   const pathname = usePathname();

//   const publicRoutes = ["/auth/login", "/auth/signup"];

//   useEffect(() => {
//     async function checkAuth() {
//       // Skip redirect for public pages
//       if (publicRoutes.includes(pathname)) {
//         setLoading(false);
//         return;
//       }

//       try {
//         const res = await axios.get("http://localhost:8000/users/me", {
//           withCredentials: true,
//         });
//         setUser(res.data);
//       } catch (error) {
//         router.replace("/auth/login");
//       } finally {
//         setLoading(false);
//       }
//     }

//     checkAuth();
//   }, [pathname, router]);

//   // Show nothing or a loader while checking auth
//   if (loading) {
//     return (
//       <div className="flex items-center justify-center min-h-screen">
//         Loading...
//       </div>
//     );
//   }

//   return (
//     <AuthContext.Provider value={{ user, loading }}>
//       {children}
//     </AuthContext.Provider>
//   );
// };

// export function useAuth() {
//   return useContext(AuthContext);
// }

"use client";

import {
  createContext,
  useContext,
  useEffect,
  useState,
  ReactNode,
} from "react";
import axios from "axios";
import { useRouter, usePathname } from "next/navigation";

interface AuthContextType {
  user: any;
  loading: boolean;
  authenticated: boolean;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  loading: true,
  authenticated: false,
});

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();
  const pathname = usePathname();

  const publicRoutes = ["/auth/login", "/auth/signup"];

  useEffect(() => {
    async function checkAuth() {
      try {
        const res = await axios.get("http://localhost:8000/users/me", {
          withCredentials: true,
        });
        setUser(res.data);

        // If logged-in user visits login/signup → redirect to home
        if (publicRoutes.includes(pathname)) {
          router.replace("/products");
        }
      } catch {
        // Not logged in
        setUser(null);

        // If trying to access protected route → redirect
        if (!publicRoutes.includes(pathname)) {
          router.replace("/auth/login");
        }
      } finally {
        setLoading(false);
      }
    }

    checkAuth();
  }, [pathname, router]);

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        authenticated: !!user,
      }}
    >
      {!loading && children}
    </AuthContext.Provider>
  );
};

export function useAuth() {
  return useContext(AuthContext);
}
