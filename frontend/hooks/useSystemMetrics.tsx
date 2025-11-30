/**
 * Hook for fetching real-time system metrics from homelab
 */

"use client";

import { useState, useEffect } from "react";
import { api } from "@/lib/api";
import { SystemMetrics } from "@/lib/api";
import { SystemMetric } from "@/types";
import { Zap, Cpu, Activity, Clock } from "lucide-react";

const REFRESH_INTERVAL = 30000; // 30 seconds

export function useSystemMetrics() {
  const [metrics, setMetrics] = useState<SystemMetric[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let intervalId: NodeJS.Timeout;

    const fetchMetrics = async () => {
      try {
        const data: SystemMetrics = await api.getSystemMetrics();
        
        // Convert API response to component format
        const formattedMetrics: SystemMetric[] = [
          {
            label: "Model Latency",
            value: data.model_latency_ms > 0 ? `${data.model_latency_ms.toFixed(0)}ms` : "N/A",
            icon: <Zap className="w-4 h-4" />,
            trend: data.model_latency_ms > 0 ? "+5%" : "0%",
          },
          {
            label: "CPU Load",
            value: `${data.cpu_usage.toFixed(1)}%`,
            icon: <Cpu className="w-4 h-4" />,
            trend: data.cpu_usage > 50 ? "+2%" : "-2%",
          },
          {
            label: "RAM Usage",
            value: `${data.ram_usage_gb.toFixed(1)}GB`,
            icon: <Activity className="w-4 h-4" />,
            trend: data.ram_usage_percent > 50 ? "+1%" : "-1%",
          },
          {
            label: "Uptime",
            value: `${data.uptime_percent.toFixed(1)}%`,
            icon: <Clock className="w-4 h-4" />,
            trend: "0%",
          },
        ];

        setMetrics(formattedMetrics);
        setLoading(false);
        setError(null);
      } catch (err) {
        console.error("Failed to fetch system metrics:", err);
        const errorMessage = err instanceof Error ? err.message : "Failed to fetch metrics";
        setError(errorMessage);
        setMetrics([]); // No data on error
        setLoading(false);
      }
    };

    // Fetch immediately
    fetchMetrics();

    // Set up interval for auto-refresh
    intervalId = setInterval(fetchMetrics, REFRESH_INTERVAL);

    return () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    };
  }, []);

  return { metrics, loading, error };
}

