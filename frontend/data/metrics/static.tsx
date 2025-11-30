/**
 * Static fallback metrics (used when API fails)
 */

import { Zap, Cpu, Activity, Clock } from "lucide-react";
import { SystemMetric, Benchmark } from "@/types";

export const staticSystemMetrics: SystemMetric[] = [
  {
    label: "Model Latency",
    value: "45ms",
    icon: <Zap className="w-4 h-4" />,
    trend: "+5%",
  },
  {
    label: "CPU Load",
    value: "32%",
    icon: <Cpu className="w-4 h-4" />,
    trend: "-2%",
  },
  {
    label: "RAM Usage",
    value: "8.2GB",
    icon: <Activity className="w-4 h-4" />,
    trend: "+1%",
  },
  {
    label: "Uptime",
    value: "99.8%",
    icon: <Clock className="w-4 h-4" />,
    trend: "0%",
  },
];

export const staticBenchmarks: Benchmark[] = [
  { model: "Llama 3 8B", speed: "42 tok/s", quality: 92, memory: "8.5GB" },
  { model: "Mistral 7B", speed: "58 tok/s", quality: 88, memory: "7.2GB" },
  { model: "Phi-3.5", speed: "75 tok/s", quality: 85, memory: "4.8GB" },
];

