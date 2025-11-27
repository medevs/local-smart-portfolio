"use client";

import { motion } from "framer-motion";
import { Activity } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { systemMetrics } from "@/data/metrics";

export function SystemMetricsCard() {
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
            Homelab metrics in real-time
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {systemMetrics.map((metric, index) => (
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
          ))}
        </CardContent>
      </Card>
    </motion.div>
  );
}

