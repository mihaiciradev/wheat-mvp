import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Technical notes",
  description: "How the wheat microplot MVP measures a photograph, and what it refuses to invent.",
};

const stages = [
  {
    title: "Photograph",
    text: "One or more still RGB images from a phone, preferably from above the plot. The original file and its metadata are kept. Video is out of scope.",
  },
  {
    title: "Quality",
    text: "Flag likely blur, poor exposure, and geometry that cannot support a measurement. A flagged image is a warning, not a crop score. The current thresholds are provisional.",
  },
  {
    title: "Scale",
    text: "Known plot length and width, plus corners a person can correct, can estimate scale and straighten perspective. A visible border alone is not a calibration. If that step fails, metres and density stay unavailable.",
  },
  {
    title: "Vegetation",
    text: "Compare simple color methods, starting with Excess Green, HSV, and adaptive thresholding, on a small set of reviewed masks. The result is vegetation cover. It is wheat cover only after weeds are excluded.",
  },
  {
    title: "Rows and gaps",
    text: "Detect the planted lines and the stretches with little vegetation. A gap is a candidate interval, not proof that a seed is missing. Row spacing is used only when it was supplied for that plot.",
  },
];

export default function TechPage() {
  return (
    <>
      <p className="eyebrow">Technical notes</p>
      <h1>What the MVP actually does</h1>
      <p className="lede">
        The product is a checkable measurement, not a model demonstration. Classical image
        processing comes first. A learned model is added only after those methods are shown to be
        insufficient on real photographs.
      </p>

      <section>
        <h2>From photo to measurement</h2>
        <ol className="stages">
          {stages.map((stage) => (
            <li key={stage.title}>
              <h3>{stage.title}</h3>
              <p>{stage.text}</p>
            </li>
          ))}
        </ol>
      </section>

      <section>
        <h2>Counting is separate</h2>
        <p>
          A wheat plant, a leaf, a tiller, vegetation cover, and plant density are different
          quantities. Seedlings overlap, and one plant can produce several tillers. Counting stays
          experimental until it is compared with manual counts, and the system must be allowed to
          abstain when the growth stage makes plants impossible to separate.
        </p>
      </section>

      <section>
        <h2>How the software is split</h2>
        <ul>
          <li>
            <code>apps/web</code> is this Next.js site. It explains the product and will later show
            results. It does not compute coverage in the browser.
          </li>
          <li>
            <code>apps/api</code> is a FastAPI service for uploads, records, and corrections.
          </li>
          <li>
            <code>packages/vision</code> is the image pipeline. It runs without the website, a
            database, or a cloud account. The first libraries are OpenCV, NumPy, Pillow, and
            scikit-image, on CPU.
          </li>
        </ul>
        <p>
          Photographs stay out of Git. Human corrections are stored beside automatic results, not
          written over them.
        </p>
      </section>

      <section className="notice">
        <h2>Running today</h2>
        <p>
          Locally, the API can report health and experimental blur and exposure flags. This
          deployed site is only the explanation. The analysis service is not part of the first
          hosting step.
        </p>
        <p>
          <Link className="text-link" href="/">
            Back to the overview
          </Link>
        </p>
      </section>
    </>
  );
}
