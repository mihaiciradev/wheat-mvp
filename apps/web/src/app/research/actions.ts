"use server";

import { cookies } from "next/headers";
import { redirect } from "next/navigation";

import { RESEARCH_COOKIE, RESEARCH_PIN, RESEARCH_VALUE } from "@/lib/research-gate";

export async function unlockResearch(formData: FormData): Promise<void> {
  const pin = String(formData.get("pin") ?? "");
  if (pin !== RESEARCH_PIN) {
    redirect("/research?error=1");
  }
  const jar = await cookies();
  jar.set(RESEARCH_COOKIE, RESEARCH_VALUE, {
    httpOnly: true,
    sameSite: "lax",
    path: "/",
    secure: process.env.NODE_ENV === "production",
    maxAge: 60 * 60 * 24 * 14,
  });
  redirect("/research");
}
