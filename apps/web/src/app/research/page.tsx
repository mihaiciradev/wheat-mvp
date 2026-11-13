import type { Metadata } from "next";

import { unlockResearch } from "@/app/research/actions";
import { hasResearchAccess } from "@/lib/research-gate";

import results from "./results.json";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Research",
  robots: { index: false, follow: false },
};

type Region = { name: string; index_mean: number };
type Capture = (typeof results.captures)[number] & {
  false_color?: string;
  scale?: string;
  regions?: Region[];
  nominal_cm_per_px?: number;
  two_metre_px?: number;
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
      <p className="eyebrow">Working notes</p>
      <h1>Research</h1>
      <p className="lede">These notes stay off the public pages. Enter the four-digit PIN.</p>
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
        <button type="submit">Open</button>
      </form>
      {wrong ? (
        <p className="pin-error" role="alert">
          That PIN is not recognized.
        </p>
      ) : null}
    </div>
  );
}

function Report() {
  return (
    <div className="research">
      <p className="eyebrow">Working notes</p>
      <h1>What these frames support.</h1>
      <p className="lede">{results.source}</p>
      <p>
        Excess Green is 2×green − red − blue, scaled to 8-bit, then split with Otsu’s threshold.
        The percentage is the share of that whole photograph. It counts every green thing in the
        frame: crop, grass, and tree canopy. It is not cover of a marked plot, and it does not say
        the plants are wheat.
      </p>
      <p>
        The color picture on the spectral frames is near infrared, red, and green. The rectangles
        were placed by hand. Inside each one, the relative index is (near infrared − red) / (near
        infrared + red), after subtracting the black level stored in the file. The sunlight sensor
        was not applied, so the index is not reflectance. The two survey frames are five seconds
        apart and do not show the same ground.
      </p>
      {results.captures.map((capture) => (
        <CaptureBlock key={capture.id} capture={capture} />
      ))}
    </div>
  );
}

function CaptureBlock({ capture }: { capture: Capture }) {
  const clipped = capture.bands.filter((band) => band.clipped > 0.02);
  return (
    <section className="capture">
      <h2>
        {clock(capture.id)}, {capture.role === "ground_level" ? "reflectance panel" : "survey frame"}
        , {capture.altitude_m.toFixed(capture.role === "ground_level" ? 2 : 1)} m
      </h2>
      <p className="stat">
        {(capture.vegetation_share * 100).toFixed(1)}% of this photograph is above the Excess Green
        threshold.
      </p>
      {clipped.length > 0 ? (
        <p>
          Spectral pixels at the top of the 16-bit range:{" "}
          {clipped.map((band) => `${band.name} ${(band.clipped * 100).toFixed(1)}%`).join(", ")}.
          This panel photo cannot set a reflectance scale.
        </p>
      ) : null}
      <div className="figure-grid">
        <Figure
          name={capture.rgb}
          alt={`Color photograph ${capture.id}`}
          caption="Color camera."
        />
        <Figure
          name={capture.exg}
          alt={`Excess Green mask over ${capture.id}`}
          caption="Green tint: pixels above the Excess Green threshold."
        />
        {capture.false_color != null ? (
          <Figure
            name={capture.false_color}
            alt={`Near-infrared false color of ${capture.id}, with rectangles on green cover and bare soil`}
            caption={regionCaption(capture.regions)}
          />
        ) : null}
        {capture.scale != null ? (
          <Figure
            name={capture.scale}
            alt="Enlarged piece of the survey photograph with a square marking 2 metres on the ground"
            caption={`The yellow square is 2 m on the ground. At ${capture.nominal_cm_per_px?.toFixed(1)} cm per pixel that is ${capture.two_metre_px} pixels on the original photo.`}
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
  if (!regions || regions.length === 0) {
    return "Near infrared is shown as red.";
  }
  const parts = regions.map((region) => `${region.name} ${region.index_mean.toFixed(3)}`);
  return `Yellow and blue rectangles. Relative index: ${parts.join("; ")}.`;
}

function clock(captureId: string): string {
  const stamp = captureId.split("_")[1] ?? "";
  return `${stamp.slice(8, 10)}:${stamp.slice(10, 12)}:${stamp.slice(12, 14)}`;
}
