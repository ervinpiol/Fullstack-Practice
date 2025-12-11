import { NextRequest, NextResponse } from "next/server";
import { createClient } from "@/lib/supabase/server";

/* NextJS is annoying and makes use a separate function for 
each request type >:( */

export async function GET(
  request: NextRequest,
  { params }: { params: { path: string[] } }
) {
  return handleRequest(request, params.path);
}

export async function POST(
  request: NextRequest,
  { params }: { params: { path: string[] } }
) {
  return handleRequest(request, params.path);
}

export async function PUT(
  request: NextRequest,
  { params }: { params: { path: string[] } }
) {
  return handleRequest(request, params.path);
}

export async function PATCH(
  request: NextRequest,
  { params }: { params: { path: string[] } }
) {
  return handleRequest(request, params.path);
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: { path: string[] } }
) {
  return handleRequest(request, params.path);
}

export async function HEAD(
  request: NextRequest,
  { params }: { params: { path: string[] } }
) {
  return handleRequest(request, params.path);
}

// async function handleRequest(request: NextRequest, path: string[]) {
//   try {
//     const supabase = await createClient();

//     // You can add more routes here dynamically based on `path`
//     return NextResponse.json(
//       { message: "Route not implemented" },
//       { status: 404 }
//     );
//   } catch (error: unknown) {
//     console.error("Supabase proxy error:", error);
//     return NextResponse.json(
//       {
//         message: "Supabase proxy error",
//         error: error instanceof Error ? error.message : "Unknown error",
//       },
//       { status: 500 }
//     );
//   }
// }

export async function handleRequest(request: NextRequest, path: string[]) {
  try {
    const supabase = await createClient();
    const method = request.method?.toUpperCase();

    // Parse request body if applicable
    let body: any = null;
    if (method && !["GET", "HEAD"].includes(method)) {
      try {
        body = await request.json();
      } catch {
        body = null;
      }
    }

    // Example: handle table operations: /table/users
    if (path[0] === "table") {
      const tableName = path[1];
      if (!tableName) {
        return NextResponse.json(
          { error: "Table name is required" },
          { status: 400 }
        );
      }

      switch (method) {
        case "GET": {
          // Optional: filter query params
          const urlParams = new URLSearchParams(request.url.split("?")[1]);
          let query = supabase.from(tableName).select("*");
          urlParams.forEach((value, key) => {
            query = query.eq(key, value);
          });
          const { data, error } = await query;
          if (error) throw error;
          return NextResponse.json(data);
        }

        case "POST": {
          if (!body)
            return NextResponse.json(
              { error: "Missing request body" },
              { status: 400 }
            );
          const { data, error } = await supabase.from(tableName).insert(body);
          if (error) throw error;
          return NextResponse.json(data);
        }

        case "PATCH":
        case "PUT": {
          if (!body?.id)
            return NextResponse.json(
              { error: "Missing id for update" },
              { status: 400 }
            );
          const { data, error } = await supabase
            .from(tableName)
            .update(body)
            .eq("id", body.id);
          if (error) throw error;
          return NextResponse.json(data);
        }

        case "DELETE": {
          if (!body?.id)
            return NextResponse.json(
              { error: "Missing id for delete" },
              { status: 400 }
            );
          const { data, error } = await supabase
            .from(tableName)
            .delete()
            .eq("id", body.id);
          if (error) throw error;
          return NextResponse.json(data);
        }

        default:
          return NextResponse.json(
            { error: "Method not allowed" },
            { status: 405 }
          );
      }
    }

    // Example: handle RPC calls: /rpc/my_function
    if (path[0] === "rpc") {
      const functionName = path[1];
      if (!functionName) {
        return NextResponse.json(
          { error: "RPC function name is required" },
          { status: 400 }
        );
      }
      const { data, error } = await supabase.rpc(functionName, body || {});
      if (error) throw error;
      return NextResponse.json(data);
    }

    // Route not implemented
    return NextResponse.json(
      { message: "Route not implemented" },
      { status: 404 }
    );
  } catch (error: unknown) {
    console.error("Supabase proxy error:", error);
    return NextResponse.json(
      {
        message: "Supabase proxy error",
        error: error instanceof Error ? error.message : "Unknown error",
      },
      { status: 500 }
    );
  }
}
