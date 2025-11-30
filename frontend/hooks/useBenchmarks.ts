/**
 * Hook for fetching LLM performance benchmarks from homelab
 */

import { useState, useEffect } from "react";
import { api } from "@/lib/api";
import { BenchmarksResponse, BenchmarkResult } from "@/lib/api";
import { Benchmark } from "@/types";

const REFRESH_INTERVAL = 300000; // 5 minutes (benchmarks are expensive)

export function useBenchmarks() {
  const [benchmarks, setBenchmarks] = useState<Benchmark[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let intervalId: NodeJS.Timeout;

    const fetchBenchmarks = async () => {
      try {
        const data: BenchmarksResponse = await api.getBenchmarks();
        
        // Convert API response to component format
        const formattedBenchmarks: Benchmark[] = data.benchmarks.map((bench: BenchmarkResult) => ({
          model: bench.model,
          speed: bench.speed_display,
          quality: bench.quality_score,
          memory: bench.memory_display,
        }));

        setBenchmarks(formattedBenchmarks);
        setLoading(false);
        setError(null);
      } catch (err) {
        console.error("Failed to fetch benchmarks:", err);
        const errorMessage = err instanceof Error ? err.message : "Failed to fetch benchmarks";
        setError(errorMessage);
        setBenchmarks([]); // No data on error
        setLoading(false);
      }
    };

    // Fetch immediately
    fetchBenchmarks();

    // Set up interval for auto-refresh
    intervalId = setInterval(fetchBenchmarks, REFRESH_INTERVAL);

    return () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    };
  }, []);

  return { benchmarks, loading, error };
}

