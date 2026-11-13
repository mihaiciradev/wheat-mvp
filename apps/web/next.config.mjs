/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  outputFileTracingIncludes: {
    "/research/media/[name]": ["./research-media/**/*.jpg"],
  },
  async redirects() {
    return [
      {
        source: "/tech",
        destination: "/approach",
        permanent: true,
      },
    ];
  },
};

export default nextConfig;
