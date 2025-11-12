"use client";

import { useState, useEffect } from "react";
import { MdUploadFile } from "react-icons/md";
import { HeroHeader } from "@/components/header";
import AnimatedBackground from "@/components/ui/AnimatedBackground";

export default function DemoPage() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState("");
  const [loading, setLoading] = useState(false);
  const [emotion, setEmotion] = useState("");
  const [probabilities, setProbabilities] = useState(null);
  const [error, setError] = useState("");
  const [modelOption, setModelOption] = useState("1");

  useEffect(() => {
    if (!file) {
      setPreview("");
      return;
    }
    const url = URL.createObjectURL(file);
    setPreview(url);
    return () => URL.revokeObjectURL(url);
  }, [file]);

  const onFileChange = (e) => {
    setEmotion("");
    setProbabilities(null);
    setError("");
    const f = (e.target.files && e.target.files[0]) || null;
    e.target.value = null;
    if (f) {
      if (!f.type.startsWith("image/")) {
        setError("Please upload an image file.");
        setFile(null);
        return;
      }
      if (f.size > 10 * 1024 * 1024) {
        setError("Image too large. Keep it under 10MB.");
        setFile(null);
        return;
      }
    }
    setFile(f);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setEmotion("");
    setProbabilities(null);

    if (!file) {
      setError("No image selected.");
      return;
    }

    setLoading(true);
    try {
      const fd = new FormData();
      fd.append("file", file);
      fd.append("model_option", modelOption);

      const API_URL =
        process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${API_URL}/predict`, {
        method: "POST",
        body: fd,
      });

      if (!res.ok) {
        throw new Error(`Server error: ${res.status}`);
      }

      const result = await res.json();
      setEmotion(result.emotion);
      setProbabilities(result.probabilities || null);
    } catch (err) {
      setError((err && err.message) || "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen text-foreground relative bg-transparent">
      <AnimatedBackground />
      <div className="absolute inset-0 bg-background/80 backdrop-blur-[2px] -z-10" />
      <HeroHeader />
      <main className="pt-28 px-6 py-12 max-w-3xl mx-auto">
        <h1 className="text-4xl font-bold mb-4">FaceFeel — Live Demo</h1>
        <p className="text-muted-foreground mb-6">
          Upload an image and see the predicted emotion.
        </p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            id="file-input"
            type="file"
            accept="image/*"
            onChange={onFileChange}
            className="hidden"
          />

          <div className="flex items-center gap-3">
            <label
              htmlFor="file-input"
              className="inline-flex items-center gap-2 rounded px-4 py-2 bg-primary text-primary-foreground cursor-pointer select-none"
            >
              Choose File
              <MdUploadFile className="h-5 w-5" />
            </label>

            <span className="text-sm text-muted-foreground truncate max-w-56">
              {file ? file.name : "No file chosen"}
            </span>
          </div>

          {preview && (
            <div className="mt-2">
              <img
                src={preview}
                alt="preview"
                className="w-full max-w-sm rounded-lg border border-border"
              />
            </div>
          )}
          <div className="mt-3">
            <label className="text-sm font-medium mr-2">Model:</label>
            <select
              value={modelOption}
              onChange={(e) => setModelOption(e.target.value)}
              className="border border-border rounded px-2 py-1 bg-background"
            >
              <option value="1">ViT (HuggingFace)</option>
              <option value="2">FER+ ONNX (Emotion Ferplus 8)</option>
            </select>
          </div>

          <div className="flex items-center gap-3">
            <button
              type="submit"
              disabled={loading}
              className="rounded px-4 py-2 bg-primary text-primary-foreground font-semibold disabled:opacity-50 cursor-pointer"
            >
              {loading ? "Analyzing…" : "Predict"}
            </button>

            <button
              type="button"
              onClick={() => {
                setFile(null);
                setEmotion("");
                setError("");
              }}
              className="rounded px-3 py-2 border border-border text-sm cursor-pointer"
            >
              Reset
            </button>
          </div>
        </form>

        <div className="mt-6 space-y-4">
          {error && (
            <div className="rounded-md bg-destructive/10 border border-destructive/20 p-3 text-sm">
              <strong>Error:</strong> {error}
            </div>
          )}

          {emotion && (
            <div className="rounded-md bg-emerald-500/10 border border-emerald-500/20 p-4">
              <div className="text-xl font-semibold text-emerald-600 dark:text-emerald-400">
                Emotion: {emotion}
                {probabilities && (
                  <ul className="mt-3 text-sm text-foreground space-y-1">
                    {Object.entries(probabilities).map(([emo, pct]) => (
                      <li key={emo}>
                        <span className="font-medium">{emo}:</span>{" "}
                        {pct.toFixed(2)}%
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
