"use client";

import { motion } from "framer-motion";
import { Sparkles } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { skills } from "@/data/skills";

export function SkillsCard() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.1 }}
      className="lg:col-span-2"
    >
      <Card className="h-full bg-gradient-to-br from-amber-950/40 to-amber-900/20 border-amber-700/30 hover:border-amber-600/50 transition-all">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-amber-100">
            <Sparkles className="w-5 h-5 text-amber-500" />
            Core Expertise
          </CardTitle>
          <CardDescription className="text-amber-200/60">
            Specialized in AI infrastructure and full-stack development
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {skills.map((skill, index) => (
            <motion.div
              key={skill.name}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 * index }}
              className="space-y-2"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="text-amber-500">{skill.icon}</div>
                  <span className="font-medium text-amber-100">
                    {skill.name}
                  </span>
                </div>
                <span className="text-sm text-amber-300">{skill.level}%</span>
              </div>
              <Progress value={skill.level} className="h-2 bg-amber-950/50" />
            </motion.div>
          ))}
        </CardContent>
      </Card>
    </motion.div>
  );
}

