"use client";

import { motion } from "framer-motion";
import { BarChart3 } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { benchmarks } from "@/data/metrics";

export function BenchmarksCard() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.6 }}
    >
      <Card className="bg-gradient-to-br from-amber-950/40 to-amber-900/20 border-amber-700/30">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-amber-100">
            <BarChart3 className="w-5 h-5 text-amber-500" />
            LLM Performance Benchmarks
          </CardTitle>
          <CardDescription className="text-amber-200/60">
            Comparative analysis of local models on my homelab
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-amber-800/30">
                  <th className="text-left py-3 px-4 text-amber-200">Model</th>
                  <th className="text-left py-3 px-4 text-amber-200">Speed</th>
                  <th className="text-left py-3 px-4 text-amber-200">Quality</th>
                  <th className="text-left py-3 px-4 text-amber-200">Memory</th>
                </tr>
              </thead>
              <tbody>
                {benchmarks.map((bench, index) => (
                  <motion.tr
                    key={bench.model}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.1 * index }}
                    className="border-b border-amber-800/20 hover:bg-amber-900/20 transition-colors"
                  >
                    <td className="py-3 px-4 text-amber-100 font-medium">
                      {bench.model}
                    </td>
                    <td className="py-3 px-4 text-amber-200/80">{bench.speed}</td>
                    <td className="py-3 px-4">
                      <div className="flex items-center gap-2">
                        <Progress
                          value={bench.quality}
                          className="h-2 w-20 bg-amber-950/50"
                        />
                        <span className="text-amber-200/80 text-sm">
                          {bench.quality}%
                        </span>
                      </div>
                    </td>
                    <td className="py-3 px-4 text-amber-200/80">{bench.memory}</td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}

