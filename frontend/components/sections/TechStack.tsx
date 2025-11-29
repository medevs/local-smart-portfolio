"use client";

import { motion } from "framer-motion";
import { Layers } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { skillCategories } from "@/data/personal";

const stacks = [
  {
    title: skillCategories[0].category,
    items: skillCategories[0].skills,
  },
  {
    title: skillCategories[1].category,
    items: skillCategories[1].skills,
  },
  {
    title: skillCategories[2].category,
    items: skillCategories[2].skills,
  },
  {
    title: skillCategories[3].category,
    items: skillCategories[3].skills,
  },
  {
    title: skillCategories[4].category,
    items: skillCategories[4].skills,
  },
  {
    title: skillCategories[5].category,
    items: skillCategories[5].skills,
  },
];

export function TechStack() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.4 }}
    >
      <Card className="bg-gradient-to-br from-amber-950/40 to-amber-900/20 border-amber-700/30">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-amber-100 text-2xl">
            <Layers className="w-6 h-6 text-amber-500" />
            Tech Stack Architecture
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {stacks.map((stack) => (
              <div
                key={stack.title}
                className="p-4 rounded-lg bg-amber-950/30 border border-amber-800/30"
              >
                <h4 className="font-semibold text-amber-100 mb-3">
                  {stack.title}
                </h4>
                <div className="space-y-2 text-sm text-amber-200/80">
                  {stack.items.map((item) => (
                    <p key={item}>• {item}</p>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}

