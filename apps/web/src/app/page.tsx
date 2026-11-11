import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Fenia",
  description: "Photographs of research plots, turned into measurements you can check.",
};

const signals = [
  { label: "See", text: "Cover, rows, and gaps." },
  { label: "Trust", text: "No number when a photo cannot support it." },
  { label: "Extend", text: "One method, ready for more crops." },
];

export default function HomePage() {
  return (
    <div className="hero">
      <p className="eyebrow">Field intelligence</p>
      <h1>Measurements from the photograph.</h1>
      <p className="lede">Fenia reads research plots and returns numbers a researcher can check.</p>
      <ul className="signals">
        {signals.map((item) => (
          <li key={item.label}>
            <span>{item.label}</span>
            {item.text}
          </li>
        ))}
      </ul>
      <Link className="approach-link" href="/approach">
        Technical approach
      </Link>
    </div>
  );
}
