import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Technical approach",
  description: "How Fenia measures sunflower and wheat plots from photographs.",
};

export default function ApproachPage() {
  return (
    <article className="approach">
      <p className="eyebrow">Technical approach</p>
      <h1>Sunflower and wheat, from the same kind of photograph.</h1>
      <p className="lede">
        Fenia starts with those two crops. Still images of small research plots are read with
        classical computer vision: vegetation cover, row geometry, and visible gaps.
      </p>
      <p>
        Lengths in metres need a known plot size and a usable view. When that is missing, the
        measurement stays unavailable. A learned model is added only where the simpler method is
        not enough. Further crops can follow the same path.
      </p>
    </article>
  );
}
