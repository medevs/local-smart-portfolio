"use client";

import { motion } from "framer-motion";
import { Activity, Loader2 } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { useSystemMetrics } from "@/hooks/useSystemMetrics";

export function SystemMetricsCard() {
  const { metrics, loading, error } = useSystemMetrics();

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}
    >
      <Card className="h-full bg-gradient-to-br from-amber-950/40 to-amber-900/20 border-amber-700/30 hover:border-amber-600/50 transition-all">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-amber-100">
            <Activity className="w-5 h-5 text-amber-500" />
            Live System Status
          </CardTitle>
          <CardDescription className="text-amber-200/60">
            {loading ? "Loading metrics..." : error ? "Unable to fetch metrics" : "Homelab metrics in real-time"}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {loading ? (
            <div className="flex items-center justify-center py-8">
              <Loader2 className="w-6 h-6 text-amber-500 animate-spin" />
            </div>
          ) : error ? (
            <div className="flex flex-col items-center justify-center py-8 text-center">
              <Activity className="w-8 h-8 text-amber-500/50 mb-2" />
              <p className="text-amber-200/60 text-sm">{error}</p>
              <p className="text-amber-300/40 text-xs mt-1">Make sure the backend is running</p>
            </div>
          ) : metrics.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-8 text-center">
              <Activity className="w-8 h-8 text-amber-500/50 mb-2" />
              <p className="text-amber-200/60 text-sm">No metrics available</p>
            </div>
          ) : (
            metrics.map((metric, index) => (
              <motion.div
                key={metric.label}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.1 * index }}
                className="flex items-center justify-between p-3 rounded-lg bg-amber-950/30 border border-amber-800/30"
              >
                <div className="flex items-center gap-3">
                  <div className="text-amber-500">{metric.icon}</div>
                  <div>
                    <p className="text-sm text-amber-200/60">{metric.label}</p>
                    <p className="text-lg font-semibold text-amber-100">
                      {metric.value}
                    </p>
                  </div>
                </div>
                {metric.trend && (
                  <Badge
                    variant="outline"
                    className="border-amber-700/50 text-amber-300"
                  >
                    {metric.trend}
                  </Badge>
                )}
              </motion.div>
            ))
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
}

