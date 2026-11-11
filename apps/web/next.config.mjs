/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
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
