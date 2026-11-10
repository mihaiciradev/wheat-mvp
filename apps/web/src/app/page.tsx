const unavailable = [
  "Vegetation coverage",
  "Row detection",
  "Gap lengths",
  "Plant counts and density",
  "Relative greenness",
  "Physical scale",
];

export default function HomePage() {
  return (
    <main>
      <p className="eyebrow">Wheat Monitoring MVP</p>
      <h1>Microplot establishment</h1>
      <p className="lede">
        This screen is the Phase 0 scaffold for researchers and field operators. It does not
        analyze photographs and it does not show crop measurements.
      </p>
      <section>
        <h2>Available now</h2>
        <ul>
          <li>API process check at <code>/health</code> on port 8000.</li>
          <li>
            Experimental blur and exposure flags at <code>POST /api/v1/images/quality</code>.
            Those flags are not a field-acceptance test.
          </li>
        </ul>
      </section>
      <section>
        <h2>Not measured yet</h2>
        <ul>
          {unavailable.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </section>
    </main>
  );
}
