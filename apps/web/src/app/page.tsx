import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Wheat microplot establishment",
  description:
    "A research tool for measuring how wheat has established in small, delimited microplots.",
};

const planned = [
  {
    title: "Plot boundary",
    text: "Locate the microplot, with manual corners when the edge is hard to see.",
  },
  {
    title: "Vegetation cover",
    text: "Estimate how much of the plot is green vegetation. That is not automatically wheat if weeds are present.",
  },
  {
    title: "Rows and gaps",
    text: "Find the planted rows and mark low-vegetation intervals. Lengths in metres require a valid scale.",
  },
];

const withheld = [
  "Disease, stress, lodging, or nitrogen from an ordinary color photo",
  "A plant count before it has been compared with manual counts",
  "Gap lengths or density when the photo has no reliable scale",
  "Video analysis, drone missions, or dependence on a drone vendor",
];

export default function HomePage() {
  return (
    <>
      <p className="eyebrow">Wheat Monitoring MVP</p>
      <h1>How well has this microplot established?</h1>
      <p className="lede">
        A measurement tool for small, clearly delimited wheat plots. It is being built so a
        researcher can see how uniformly the crop has emerged, and where the visible gaps are,
        from still photographs.
      </p>
      <p>
        <Link className="text-link" href="/tech">
          Read the technical notes
        </Link>
      </p>

      <section>
        <h2>Who it is for</h2>
        <p>
          Agronomists reviewing microplots, and field operators who photograph them and correct a
          boundary or a row line. The plots in view are about two metres across, with wheat sown
          in visible rows. Exact length, width, and row spacing stay as data for each plot. They
          are not assumed.
        </p>
      </section>

      <section>
        <h2>What the first version is for</h2>
        <div className="card-grid">
          {planned.map((item) => (
            <article className="card" key={item.title}>
              <h3>{item.title}</h3>
              <p>{item.text}</p>
            </article>
          ))}
        </div>
      </section>

      <section>
        <h2>What it will not claim</h2>
        <ul>
          {withheld.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </section>

      <section className="notice">
        <h2>Where the work stands</h2>
        <p>
          The measurement pipeline is not running on this website. Blur and exposure checks exist
          as an experiment on the local API. Coverage, rows, gaps, plant counts, and physical
          scale are still unavailable. No accuracy figure has been calculated, because there is
          not yet a reviewed set of field photographs.
        </p>
      </section>
    </>
  );
}
