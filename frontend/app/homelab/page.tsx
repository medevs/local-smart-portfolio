"use client";

import { motion } from "framer-motion";
import { Server, Shield } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  homelabOverview,
  journeyMilestones,
  homelabServices,
  securityFeatures,
  homelabPageContent,
} from "@/data/homelab";

/**
 * Homelab Journey Page
 * Route: /homelab
 */
export default function HomelabJourneyPage() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-8"
    >
      <div className="text-center mb-12">
        <h1 className="text-4xl md:text-5xl font-bold text-amber-100 mb-4 flex items-center justify-center gap-3">
          <Server className="w-10 h-10 text-amber-500" />
          {homelabPageContent.title}
        </h1>
        <p className="text-lg text-amber-200/70 max-w-3xl mx-auto">
          {homelabPageContent.subtitle}
        </p>
      </div>

      {/* Overview Card */}
      <Card className="bg-gradient-to-br from-amber-950/40 to-amber-900/20 border-amber-700/30">
        <CardHeader>
          <CardTitle className="text-amber-100 text-2xl">{homelabPageContent.overviewTitle}</CardTitle>
          <CardDescription className="text-amber-200/60">
            {homelabPageContent.overviewDescription}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-amber-100 font-semibold mb-3">Hardware</h3>
              <ul className="space-y-2 text-amber-200/80 text-sm">
                {homelabOverview.hardware.map((item, index) => (
                  <li key={index}>• {item}</li>
                ))}
              </ul>
            </div>
            <div>
              <h3 className="text-amber-100 font-semibold mb-3">Software Stack</h3>
              <ul className="space-y-2 text-amber-200/80 text-sm">
                {homelabOverview.software.map((item, index) => (
                  <li key={index}>• {item}</li>
                ))}
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Journey Timeline */}
      <Card className="bg-gradient-to-br from-amber-950/40 to-amber-900/20 border-amber-700/30">
        <CardHeader>
          <CardTitle className="text-amber-100 text-2xl">{homelabPageContent.timelineTitle}</CardTitle>
          <CardDescription className="text-amber-200/60">
            {homelabPageContent.timelineDescription}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {journeyMilestones.map((milestone, index) => (
              <motion.div
                key={milestone.day}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="flex gap-6"
              >
                <div className="flex flex-col items-center min-w-[80px]">
                  <div className="w-auto min-w-[70px] px-3 py-2 rounded-full bg-amber-700/30 border-2 border-amber-600 flex items-center justify-center text-amber-100 font-bold text-xs whitespace-nowrap">
                    {milestone.day}
                  </div>
                  {index < journeyMilestones.length - 1 && (
                    <div className="w-0.5 h-full bg-amber-700/30 mt-2" />
                  )}
                </div>
                <div className="flex-1 pb-8">
                  <div className="flex items-center gap-2 mb-2">
                    <h3 className="text-xl font-semibold text-amber-100">
                      {milestone.title}
                    </h3>
                    {milestone.badge && (
                      <Badge variant="outline" className="border-amber-700/50 text-amber-300">
                        {milestone.badge}
                      </Badge>
                    )}
                  </div>
                  <p className="text-amber-200/60 mb-2">{milestone.description}</p>
                  {milestone.achievements && (
                    <ul className="list-disc list-inside text-amber-200/60 text-sm space-y-1">
                      {milestone.achievements.map((achievement, i) => (
                        <li key={i}>{achievement}</li>
                      ))}
                    </ul>
                  )}
                </div>
              </motion.div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Services Running */}
      <Card className="bg-gradient-to-br from-amber-950/40 to-amber-900/20 border-amber-700/30">
        <CardHeader>
          <CardTitle className="text-amber-100 text-2xl">{homelabPageContent.servicesTitle}</CardTitle>
          <CardDescription className="text-amber-200/60">
            {homelabPageContent.servicesDescription}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {homelabServices.map((service, index) => (
              <motion.div
                key={service.name}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.1 }}
                className="p-4 rounded-lg bg-amber-950/30 border border-amber-800/30"
              >
                <div className="flex items-center gap-3 mb-2">
                  {service.icon}
                  <h4 className="font-semibold text-amber-100">{service.name}</h4>
                </div>
                <p className="text-sm text-amber-200/60">{service.description}</p>
                {service.port && (
                  <Badge variant="outline" className="mt-2 border-amber-700/50 text-amber-300 text-xs">
                    Port: {service.port}
                  </Badge>
                )}
              </motion.div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Security Features */}
      <Card className="bg-gradient-to-br from-amber-950/40 to-amber-900/20 border-amber-700/30">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-amber-100 text-2xl">
            <Shield className="w-6 h-6 text-amber-500" />
            {homelabPageContent.securityTitle}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {securityFeatures.map((feature, index) => (
              <motion.div
                key={feature.name}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="flex items-start gap-3 p-3 rounded-lg bg-amber-950/30 border border-amber-800/30"
              >
                <div className="text-amber-500 mt-1">{feature.icon}</div>
                <div>
                  <h4 className="font-semibold text-amber-100 mb-1">{feature.name}</h4>
                  <p className="text-sm text-amber-200/60">{feature.description}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}


