"use client";

import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { personalInfo } from "@/data/personal";
import { quickFacts, journeyText } from "@/data/about";

export function AboutCard() {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.1 }}
        className="lg:col-span-2"
      >
        <Card className="h-full bg-gradient-to-br from-amber-950/40 to-amber-900/20 border-amber-700/30">
          <CardHeader>
            <CardTitle className="text-amber-100 text-2xl">My Journey</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4 text-amber-200/80">
            <p>{personalInfo.bio}</p>
            <p>{journeyText.currentWork}</p>
            <p>{journeyText.currentFocus}</p>
          </CardContent>
        </Card>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.2 }}
      >
        <Card className="h-full bg-gradient-to-br from-amber-950/40 to-amber-900/20 border-amber-700/30">
          <CardHeader>
            <CardTitle className="text-amber-100">Quick Facts</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {quickFacts.map((fact, index) => (
              <div key={fact.title}>
                <div className="flex items-start gap-3">
                  {fact.icon}
                  <div>
                    <p className="font-medium text-amber-100">{fact.title}</p>
                    <p className="text-sm text-amber-200/60">{fact.subtitle}</p>
                  </div>
                </div>
                {index < quickFacts.length - 1 && (
                  <Separator className="bg-amber-800/30 mt-4" />
                )}
              </div>
            ))}
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}

