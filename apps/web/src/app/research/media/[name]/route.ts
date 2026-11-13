import { readFile } from "node:fs/promises";
import path from "node:path";

import { hasResearchAccess } from "@/lib/research-gate";

import results from "../../results.json";

export const dynamic = "force-dynamic";

const ALLOWED = new Set<string>();
collectNames(results, ALLOWED);

function collectNames(value: unknown, into: Set<string>): void {
  if (typeof value === "string") {
    if (value.endsWith(".jpg")) {
      into.add(value);
    }
    return;
  }
  if (Array.isArray(value)) {
    for (const item of value) {
      collectNames(item, into);
    }
    return;
  }
  if (value !== null && typeof value === "object") {
    for (const item of Object.values(value)) {
      collectNames(item, into);
    }
  }
}

export async function GET(
  _request: Request,
  context: { params: Promise<{ name: string }> },
): Promise<Response> {
  const { name } = await context.params;
  if (!ALLOWED.has(name)) {
    return new Response("Not found", { status: 404 });
  }
  if (!(await hasResearchAccess())) {
    return new Response("PIN required", { status: 401 });
  }
  const bytes = await readFile(path.join(process.cwd(), "research-media", name));
  return new Response(bytes, {
    headers: {
      "Content-Type": "image/jpeg",
      "Cache-Control": "private, no-store",
      "X-Content-Type-Options": "nosniff",
    },
  });
}
