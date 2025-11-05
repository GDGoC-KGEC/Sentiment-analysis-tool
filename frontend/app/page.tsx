"use client";
import { HeroHeader } from "@/components/header";
import HeroSection from "@/components/hero-section";

export default function Home() {
  return (
    <div className="min-h-screen bg-black text-white relative overflow-hidden">
      <HeroHeader/>
      <HeroSection/>
    </div>
  );
}
