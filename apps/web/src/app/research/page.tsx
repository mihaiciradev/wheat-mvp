import type { Metadata } from "next";

import { unlockResearch } from "@/app/research/actions";
import { hasResearchAccess } from "@/lib/research-gate";

import results from "./results.json";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Cercetare",
  robots: { index: false, follow: false },
};

type Region = { name: string; index_mean: number };
type RawBand = { key: string; file: string };
type Capture = (typeof results.captures)[number] & {
  false_color?: string;
  scale?: string;
  regions?: Region[];
  raw_bands: RawBand[];
  nominal_cm_per_px?: number;
  two_metre_px?: number;
};

const BAND_LABEL: Record<string, string> = {
  G: "verde, 560±16 nm",
  R: "roșu, 650±16 nm",
  RE: "red edge, 730±16 nm",
  NIR: "infraroșu apropiat, 860±26 nm",
};

export default async function ResearchPage({
  searchParams,
}: {
  searchParams: Promise<{ error?: string }>;
}) {
  const open = await hasResearchAccess();
  if (!open) {
    const params = await searchParams;
    return <Gate wrong={params.error === "1"} />;
  }
  return <Report />;
}

function Gate({ wrong }: { wrong: boolean }) {
  return (
    <div className="research">
      <p className="eyebrow">Note de lucru</p>
      <h1>Cercetare</h1>
      <p className="lede">Notele astea nu sunt pe paginile publice. Introdu PIN-ul din patru cifre.</p>
      <form className="pin-form" action={unlockResearch}>
        <label htmlFor="pin">PIN</label>
        <input
          id="pin"
          name="pin"
          type="password"
          inputMode="numeric"
          autoComplete="off"
          minLength={4}
          maxLength={4}
          pattern="[0-9]{4}"
          required
        />
        <button type="submit">Deschide</button>
      </form>
      {wrong ? (
        <p className="pin-error" role="alert">
          PIN-ul nu este recunoscut.
        </p>
      ) : null}
    </div>
  );
}

function Report() {
  return (
    <div className="research">
      <p className="eyebrow">Note de lucru</p>
      <h1>Ce putem citi din aceste cadre.</h1>
      <p className="lede">
        Trei declanșări din exemplul Pix4D pentru DJI Mavic 3 Multispectral: orz de toamnă, 5
        aprilie 2024. Nu sunt parcelele noastre.
      </p>
      <p>
        La fiecare cadru sunt trei părți. Intrarea este ce a scris camera. La mijloc este ce a
        rulat codul. Ieșirea este imaginea și numărul care au rezultat. Procentul este din toată
        fotografia, nu dintr-o parcelă marcată, și verdele nu este numit grâu.
      </p>
      {results.captures.map((capture) => (
        <CaptureBlock key={capture.id} capture={capture} />
      ))}
    </div>
  );
}

function CaptureBlock({ capture }: { capture: Capture }) {
  const aerial = capture.role !== "ground_level";
  const clipped = capture.bands.filter((band) => band.clipped > 0.02);
  return (
    <section className="capture">
      <h2>
        {clock(capture.id)} · {aerial ? "cadru de zbor" : "panou de reflectanță"} ·{" "}
        {ro(capture.altitude_m, aerial ? 1 : 2)} m
      </h2>

      <h3>Intrare</h3>
      <p>
        Un declanșator, cinci fișiere. Fotografia color este JPEG, 5280×3956. Fiecare bandă
        spectrală este un TIFF separat, 2592×1944, 16 biți, o singură valoare pe pixel. Benzile
        sunt arătate în gri, cu contrastul întins, doar ca să se vadă pe ecran.
      </p>
      <div className="figure-grid">
        <Figure
          name={capture.rgb}
          alt={`Fotografia color originală ${capture.id}`}
          caption="Intrare. Camera color, fișierul JPEG."
        />
      </div>
      <div className="figure-grid band-grid">
        {capture.raw_bands.map((band) => (
          <Figure
            key={band.file}
            name={band.file}
            alt={`Banda spectrală ${BAND_LABEL[band.key] ?? band.key} din ${capture.id}`}
            caption={`Intrare. ${BAND_LABEL[band.key] ?? band.key}. TIFF pe 16 biți, contrast întins pentru ecran.`}
          />
        ))}
      </div>

      <h3>Ce a făcut codul</h3>
      <ul>
        <li>
          Pe fotografia color: Excess Green = 2×verde − roșu − albastru. Valorile au fost aduse la
          8 biți și tăiate cu pragul lui Otsu. Pixelii peste prag sunt colorați verde.
        </li>
        {aerial ? (
          <li>
            Pe benzile spectrale: a scăzut nivelul de negru din fișier (3200), a suprapus benzile
            cu matricea scrisă în fiecare fișier, apoi a calculat (infraroșu apropiat − roșu) /
            (infraroșu apropiat + roșu) în două dreptunghiuri puse de mână. Senzorul de lumină nu a
            intrat în calcul, deci indicele nu este reflectanță.
          </li>
        ) : (
          <li>
            Pe benzile spectrale nu s-a calculat un indice. Pixelii de la capătul de sus al
            intervalului de 16 biți sunt{" "}
            {clipped.map((band) => `${BAND_LABEL[band.key] ?? band.name} ${ro(band.clipped * 100, 1)}%`).join(", ")}.
            Cadrul ăsta nu poate fixa scara de reflectanță.
          </li>
        )}
      </ul>

      <h3>Ieșire</h3>
      <p className="stat">
        {ro(capture.vegetation_share * 100, 1)}% din fotografia color este peste pragul Excess
        Green.
      </p>
      <div className="figure-grid">
        <Figure
          name={capture.exg}
          alt={`Masca Excess Green peste ${capture.id}`}
          caption="Ieșire. Verdele marcat este peste prag. Lângă el, sus, este fotografia din care a ieșit."
        />
        {capture.false_color != null ? (
          <Figure
            name={capture.false_color}
            alt={`Culoare falsă din infraroșu apropiat pentru ${capture.id}`}
            caption={regionCaption(capture.regions)}
          />
        ) : null}
        {capture.scale != null ? (
          <Figure
            name={capture.scale}
            alt="Fragment mărit din fotografia de zbor, cu un pătrat de 2 metri"
            caption={`Ieșire. Pătratul galben are 2 m pe teren. La ${ro(capture.nominal_cm_per_px ?? 0, 1)} cm pe pixel înseamnă ${capture.two_metre_px} de pixeli în fotografia originală. De aici nu se numără rânduri sau plante.`}
          />
        ) : null}
      </div>
    </section>
  );
}

function Figure({ name, alt, caption }: { name: string; alt: string; caption: string }) {
  return (
    <figure>
      {/* The file is served only after the PIN cookie is set. next/image would publish it. */}
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img src={`/research/media/${name}`} alt={alt} />
      <figcaption>{caption}</figcaption>
    </figure>
  );
}

function regionCaption(regions: Region[] | undefined): string {
  const named = new Map((regions ?? []).map((region) => [region.name, region.index_mean]));
  const cover = named.get("green cover");
  const soil = named.get("bare soil");
  if (cover == null || soil == null) {
    return "Ieșire. Infraroșu apropiat desenat ca roșu.";
  }
  return `Ieșire. Infraroșu apropiat desenat ca roșu, lângă benzile gri de mai sus. Dreptunghi galben, acoperire verde: ${ro(cover, 3)}. Dreptunghi albastru, sol gol: ${ro(soil, 3)}.`;
}

function clock(captureId: string): string {
  const stamp = captureId.split("_")[1] ?? "";
  return `${stamp.slice(8, 10)}:${stamp.slice(10, 12)}:${stamp.slice(12, 14)}`;
}

function ro(value: number, digits: number): string {
  return value.toFixed(digits).replace(".", ",");
}
