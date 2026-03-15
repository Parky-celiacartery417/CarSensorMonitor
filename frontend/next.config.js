/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "ccsrpcma.carsensor.net",
      },
      {
        protocol: "https",
        hostname: "ccsrpcml.carsensor.net",
      },
    ],
  },
};

module.exports = nextConfig;
