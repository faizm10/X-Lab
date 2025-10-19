import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  
  // Enable standalone output for Docker production builds
  output: 'standalone',
};

export default nextConfig;
