"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { href: "/approach", label: "Technical approach" },
  { href: "/research", label: "Research" },
];

export function SiteHeader() {
  const pathname = usePathname();

  return (
    <header className="site-header">
      <Link className="brand" href="/">
        Fenia
      </Link>
      <nav aria-label="Site">
        {links.map((link) => {
          const current = pathname === link.href;
          return (
            <Link key={link.href} href={link.href} aria-current={current ? "page" : undefined}>
              {link.label}
            </Link>
          );
        })}
      </nav>
    </header>
  );
}
