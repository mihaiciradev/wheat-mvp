import { cookies } from "next/headers";

/** Server-side gate for /research. Do not import this from a client component. */
export const RESEARCH_PIN = "1113";
export const RESEARCH_COOKIE = "fenia_research";
export const RESEARCH_VALUE = "granted";

export async function hasResearchAccess(): Promise<boolean> {
  const jar = await cookies();
  return jar.get(RESEARCH_COOKIE)?.value === RESEARCH_VALUE;
}
