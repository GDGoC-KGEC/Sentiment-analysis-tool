"use client";
import React from "react";

/**
 * Subtle animated ambient blobs background.
 * Safe, cheap, works in both dark/light because blobs use mix-blend and low opacity.
 */
export default function AnimatedBackground() {
  return (
    <>
      <div aria-hidden className="absolute inset-0 -z-10 pointer-events-none overflow-hidden">
        <div className="relative w-full h-full">
          <div className="blob blob-1" />
          <div className="blob blob-2" />
          <div className="blob blob-3" />
        </div>
      </div>

      <style jsx>{`
        .blob {
          position: absolute;
          filter: blur(60px);
          opacity: 0.55;
          width: 40vmax;
          height: 40vmax;
          border-radius: 50%;
          transform-origin: center;
          mix-blend-mode: screen;
        }

        /* individual colors & starting positions */
        .blob-1 {
          background: radial-gradient(circle at 30% 30%, rgba(72, 187, 120, 0.95), rgba(72,187,120,0.3) 40%, transparent 60%);
          left: -10%;
          top: -25%;
          animation: move1 18s ease-in-out infinite;
        }

        .blob-2 {
          background: radial-gradient(circle at 70% 40%, rgba(79, 70, 229, 0.95), rgba(79,70,229,0.28) 40%, transparent 60%);
          right: -22%;
          top: -10%;
          animation: move2 22s ease-in-out infinite;
        }

        .blob-3 {
          background: radial-gradient(circle at 50% 60%, rgba(6, 182, 212, 0.92), rgba(6,182,212,0.22) 40%, transparent 60%);
          left: 10%;
          bottom: -30%;
          animation: move3 26s ease-in-out infinite;
        }

        /* subtle different motion patterns */
        @keyframes move1 {
          0% { transform: translate3d(0,0,0) scale(1) rotate(0deg); }
          50% { transform: translate3d(6vw, 4vh, 0) scale(1.05) rotate(6deg); }
          100% { transform: translate3d(0,0,0) scale(1) rotate(0deg); }
        }
        @keyframes move2 {
          0% { transform: translate3d(0,0,0) scale(1) rotate(0deg); }
          50% { transform: translate3d(-8vw, 6vh, 0) scale(1.08) rotate(-8deg); }
          100% { transform: translate3d(0,0,0) scale(1) rotate(0deg); }
        }
        @keyframes move3 {
          0% { transform: translate3d(0,0,0) scale(1) rotate(0deg); }
          50% { transform: translate3d(10vw, -6vh, 0) scale(1.06) rotate(4deg); }
          100% { transform: translate3d(0,0,0) scale(1) rotate(0deg); }
        }

        /* reduce intensity on small screens */
        @media (max-width: 640px) {
          .blob { filter: blur(48px); width: 80vmax; height: 80vmax; opacity: 0.45; }
        }
      `}</style>
    </>
  );
}
