"use client";

import { motion } from "framer-motion";
import { Coffee, Download, ChevronRight, Database, Cpu } from "lucide-react";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { personalInfo } from "@/data/personal";
import { heroContent } from "@/data/pageContent";
import { 
  SiPostgresql, 
  SiMongodb, 
  SiDocker, 
  SiNextdotjs, 
  SiTypescript,
  SiReact,
  SiFastapi,
  SiLinux,
  SiPython
} from "react-icons/si";

export function Hero() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-amber-900/20 via-amber-800/10 to-amber-950/20 border border-amber-700/30"
    >
      <div className="pattern-grid absolute inset-0 opacity-30" />

      <div className="relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12">
          {/* Left Side - Profile Section */}
          <div className="p-8 md:p-10 lg:p-12">
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="flex items-start gap-6 mb-6"
            >
              <div className="relative flex-shrink-0">
                <div className="relative w-28 h-28 md:w-36 md:h-36 lg:w-40 lg:h-40 rounded-full overflow-hidden border-4 border-amber-600/60 shadow-2xl shadow-amber-900/50 ring-4 ring-amber-900/30">
                  <img
                    src="/profile-placeholder.svg"
                    alt={personalInfo.name}
                    className="w-full h-full object-cover"
                  />
                  <div className="absolute inset-0 bg-gradient-to-br from-amber-600/10 to-transparent" />
                </div>
                <div className="absolute bottom-1 right-1 w-4 h-4 md:w-5 md:h-5 bg-green-500 rounded-full border-3 md:border-4 border-amber-950 shadow-lg" />
              </div>

              <div className="flex-1 pt-2">
                <h1 className="text-3xl md:text-4xl lg:text-5xl xl:text-6xl font-bold mb-2 bg-gradient-to-r from-amber-200 via-amber-100 to-amber-300 bg-clip-text text-transparent leading-tight">
                  {personalInfo.name}
                </h1>
                <p className="text-lg md:text-xl lg:text-2xl text-amber-200/90">
                  {heroContent.subtitle}
                </p>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="mb-6"
            >
              <p className="text-base md:text-lg text-amber-100/80 leading-relaxed">
                {heroContent.bio}
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="flex flex-wrap items-center gap-4 mb-6 text-sm text-amber-200/70"
            >
            </motion.div>

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
              className="mb-6"
            >
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-amber-900/40 border border-amber-700/50">
                <Coffee className="w-4 h-4 text-amber-500" />
                <span className="text-sm text-amber-200 font-medium">
                  {heroContent.availabilityText}
                </span>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
              className="flex flex-wrap gap-3"
            >
              <Button
                size="lg"
                className="bg-amber-700 hover:bg-amber-600 text-white px-6"
              >
                <Download className="w-4 h-4 mr-2" />
                {heroContent.downloadResumeText}
              </Button>
              <Link href="/projects">
                <Button
                  size="lg"
                  variant="outline"
                  className="border-amber-700/50 text-amber-200 hover:bg-amber-900/30 px-6"
                >
                  {heroContent.viewProjectsText}
                  <ChevronRight className="w-4 h-4 ml-2" />
                </Button>
              </Link>
            </motion.div>
          </div>

          {/* Right Side - Crisp AI Stack */}
          <div className="relative min-h-[400px] lg:min-h-[500px] flex items-center justify-center p-8 md:p-10 lg:p-12">
            <div className="relative w-full h-full flex items-center justify-center">
              <CrispAIStack />
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}

// Crisp AI Stack with Better Spacing
function CrispAIStack() {
  return (
    <div className="relative w-full h-full flex items-center justify-center">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.8, delay: 0.2 }}
        className="relative w-full max-w-xl"
      >
        {/* Architecture Grid with Better Spacing */}
        <div className="relative flex flex-col items-center justify-center gap-5 md:gap-6">
          
          {/* Row 1: Data Layer */}
          <motion.div 
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4, type: "spring" }}
            className="flex items-center gap-4 md:gap-5"
          >
            <CrispIconCard icon={<SiPostgresql />} label="PostgreSQL" color="#4169E1" delay={0.5} />
            <CrispIconCard icon={<Database strokeWidth={1.5} />} label="Vector DB" color="#F59E0B" delay={0.6} />
            <CrispIconCard icon={<SiMongodb />} label="MongoDB" color="#47A248" delay={0.7} />
          </motion.div>

          {/* Row 2: Core AI Infrastructure */}
          <div className="flex items-center gap-4 md:gap-5">
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.8, type: "spring" }}
            >
              <CrispIconCard icon={<SiPython />} label="LangChain" color="#3776AB" delay={0.8} />
            </motion.div>
            
            {/* Central LLM - Hero Element */}
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.9, type: "spring", stiffness: 150 }}
              className="relative"
            >
              <motion.div
                animate={{
                  y: [0, -5, 0],
                }}
                transition={{
                  duration: 5,
                  repeat: Infinity,
                  ease: "easeInOut",
                }}
                className="relative"
              >
                <motion.div
                  animate={{
                    boxShadow: [
                      "0 10px 40px rgba(217, 119, 6, 0.4)",
                      "0 20px 60px rgba(217, 119, 6, 0.7)",
                      "0 10px 40px rgba(217, 119, 6, 0.4)",
                    ],
                  }}
                  transition={{
                    duration: 3,
                    repeat: Infinity,
                    ease: "easeInOut",
                  }}
                  className="w-36 h-36 md:w-40 md:h-40 bg-gradient-to-br from-amber-600 via-amber-700 to-amber-800 border-[3px] border-amber-400 rounded-2xl flex flex-col items-center justify-center p-3 shadow-2xl relative overflow-hidden"
                >
                  {/* Animated shine effect */}
                  <motion.div
                    animate={{
                      x: ["-200%", "200%"],
                    }}
                    transition={{
                      duration: 3,
                      repeat: Infinity,
                      repeatDelay: 2,
                      ease: "easeInOut",
                    }}
                    className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent skew-x-12"
                  />
                  
                  {/* Icon */}
                  <motion.div
                    animate={{
                      rotate: [0, 5, -5, 0],
                      scale: [1, 1.05, 1],
                    }}
                    transition={{
                      duration: 4,
                      repeat: Infinity,
                      ease: "easeInOut",
                    }}
                    className="relative text-amber-50 mb-2"
                  >
                    <Cpu className="w-14 h-14 md:w-16 md:h-16" strokeWidth={1.5} />
                  </motion.div>
                  
                  {/* Labels */}
                  <div className="relative text-center z-10">
                    <div className="text-lg md:text-xl font-bold text-amber-50 mb-1">
                      Local LLM
                    </div>
                    <div className="text-xs text-amber-200 font-semibold">Self-Hosted</div>
                  </div>
                  
                  {/* Animated Status Indicators */}
                  <div className="relative flex gap-1.5 mt-2 z-10">
                    {[0, 0.15, 0.3].map((delay, i) => (
                      <motion.div
                        key={i}
                        animate={{
                          scale: [1, 1.3, 1],
                          opacity: [0.7, 1, 0.7],
                        }}
                        transition={{
                          duration: 1.5,
                          repeat: Infinity,
                          delay,
                          ease: "easeInOut",
                        }}
                        className="w-2 h-2 bg-green-400 rounded-full shadow-lg shadow-green-400/60"
                      />
                    ))}
                  </div>
                </motion.div>

                {/* Animated Privacy Badge */}
                <motion.div
                  initial={{ opacity: 0, scale: 0, rotate: -45 }}
                  animate={{ opacity: 1, scale: 1, rotate: 0 }}
                  transition={{ delay: 1.3, type: "spring", stiffness: 200 }}
                  className="absolute -top-2 -right-2 z-20"
                >
                  <motion.div
                    animate={{
                      rotate: [0, -5, 5, 0],
                    }}
                    transition={{
                      duration: 3,
                      repeat: Infinity,
                      ease: "easeInOut",
                    }}
                    className="bg-green-600 text-white text-[10px] font-bold px-2.5 py-1 rounded-full border-2 border-green-400/60 shadow-xl"
                  >
                    100% Private
                  </motion.div>
                </motion.div>

                {/* Animated Cost Badge */}
                <motion.div
                  initial={{ opacity: 0, scale: 0, rotate: 45 }}
                  animate={{ opacity: 1, scale: 1, rotate: 0 }}
                  transition={{ delay: 1.5, type: "spring", stiffness: 200 }}
                  className="absolute -bottom-2 -left-2 z-20"
                >
                  <motion.div
                    animate={{
                      scale: [1, 1.1, 1],
                    }}
                    transition={{
                      duration: 2,
                      repeat: Infinity,
                      ease: "easeInOut",
                    }}
                    className="bg-amber-600 text-white text-[10px] font-bold px-2.5 py-1 rounded-full border-2 border-amber-400/60 shadow-xl"
                  >
                    90% Cost ↓
                  </motion.div>
                </motion.div>
              </motion.div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 1.0, type: "spring" }}
            >
              <CrispIconCard 
                icon={
                  <svg viewBox="0 0 24 24" fill="currentColor" className="w-7 h-7 md:w-8 md:h-8">
                    <path d="M13 13v6a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1v-6H4a1 1 0 0 1-1-1v-2a1 1 0 0 1 1-1h5V4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v5h5a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1h-5z"/>
                  </svg>
                } 
                label="RAG" 
                color="#F59E0B" 
                delay={1.0} 
              />
            </motion.div>
          </div>

          {/* Row 3: Backend & Infrastructure */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.1, type: "spring" }}
            className="flex items-center gap-4 md:gap-5"
          >
            <CrispIconCard icon={<SiFastapi />} label="FastAPI" color="#009688" delay={1.2} />
            <CrispIconCard icon={<SiDocker />} label="Docker" color="#2496ED" delay={1.3} />
            <CrispIconCard icon={<SiLinux />} label="Linux" color="#FCC624" delay={1.4} />
          </motion.div>

          {/* Row 4: Frontend Stack */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 1.5, type: "spring" }}
            className="flex items-center gap-4 md:gap-5"
          >
            <CrispIconCard icon={<SiNextdotjs />} label="Next.js" color="#FFFFFF" delay={1.6} />
            <CrispIconCard icon={<SiTypescript />} label="TypeScript" color="#3178C6" delay={1.7} />
            <CrispIconCard icon={<SiReact />} label="React" color="#61DAFB" delay={1.8} />
          </motion.div>
        </div>

        {/* Animated Connection Lines */}
        <svg
          className="absolute inset-0 w-full h-full pointer-events-none"
          style={{ zIndex: 1 }}
          viewBox="0 0 100 100"
          preserveAspectRatio="none"
        >
          <defs>
            <linearGradient id="lineGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#F59E0B" stopOpacity="0.5" />
              <stop offset="100%" stopColor="#D97706" stopOpacity="0.7" />
            </linearGradient>
          </defs>
          
          {/* Animated connecting lines */}
          {[
            { x1: 50, y1: 18, x2: 50, y2: 38 },
            { x1: 50, y1: 62, x2: 50, y2: 82 },
            { x1: 28, y1: 50, x2: 43, y2: 50 },
            { x1: 57, y1: 50, x2: 72, y2: 50 },
          ].map((line, i) => (
            <motion.line
              key={i}
              x1={line.x1}
              y1={line.y1}
              x2={line.x2}
              y2={line.y2}
              stroke="url(#lineGrad)"
              strokeWidth="1.5"
              strokeDasharray="4 4"
              initial={{ pathLength: 0, opacity: 0 }}
              animate={{ 
                pathLength: 1, 
                opacity: [0.4, 0.7, 0.4],
              }}
              transition={{ 
                pathLength: { duration: 1.5, delay: 2 + i * 0.2 },
                opacity: { duration: 2, repeat: Infinity, ease: "easeInOut" }
              }}
            />
          ))}
        </svg>

        {/* Flowing Data Particles */}
        {[
          { start: { x: 50, y: 18 }, end: { x: 50, y: 50 }, delay: 0 },
          { start: { x: 50, y: 50 }, end: { x: 50, y: 82 }, delay: 0.8 },
          { start: { x: 28, y: 50 }, end: { x: 50, y: 50 }, delay: 1.6 },
          { start: { x: 72, y: 50 }, end: { x: 50, y: 50 }, delay: 2.4 },
        ].map((flow, i) => (
          <motion.div
            key={i}
            className="absolute w-2 h-2 rounded-full shadow-lg"
            style={{
              left: `${flow.start.x}%`,
              top: `${flow.start.y}%`,
              background: "linear-gradient(135deg, #FCD34D, #F59E0B)",
            }}
            animate={{
              left: [`${flow.start.x}%`, `${flow.end.x}%`],
              top: [`${flow.start.y}%`, `${flow.end.y}%`],
              opacity: [0, 1, 1, 0],
              scale: [0.5, 1.3, 1.2, 0.5],
            }}
            transition={{
              duration: 2.5,
              repeat: Infinity,
              delay: flow.delay + 3,
              ease: "easeInOut",
            }}
          />
        ))}

        {/* Orbiting particles */}
        {[0, 120, 240].map((angle, i) => (
          <motion.div
            key={`orbit-${i}`}
            className="absolute w-1.5 h-1.5 bg-amber-400 rounded-full shadow-lg shadow-amber-400/70"
            style={{
              left: "50%",
              top: "50%",
            }}
            animate={{
              x: [
                Math.cos((angle * Math.PI) / 180) * 90,
                Math.cos(((angle + 360) * Math.PI) / 180) * 90,
              ],
              y: [
                Math.sin((angle * Math.PI) / 180) * 70,
                Math.sin(((angle + 360) * Math.PI) / 180) * 70,
              ],
              opacity: [0.3, 0.8, 0.3],
            }}
            transition={{
              duration: 8,
              repeat: Infinity,
              delay: i * 0.5 + 3,
              ease: "linear",
            }}
          />
        ))}

        {/* Enhanced Background Glow */}
        <motion.div
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.2, 0.3, 0.2],
          }}
          transition={{
            duration: 4,
            repeat: Infinity,
            ease: "easeInOut",
          }}
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-gradient-radial from-amber-500/30 via-amber-600/15 to-transparent blur-3xl rounded-full pointer-events-none"
        />
      </motion.div>
    </div>
  );
}

// Crisp Icon Card with Solid Background
function CrispIconCard({ 
  icon, 
  label, 
  color, 
  delay 
}: { 
  icon: React.ReactNode; 
  label: string; 
  color: string;
  delay: number;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.7, y: 20 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      transition={{ 
        delay, 
        type: "spring",
        stiffness: 200,
        damping: 12
      }}
      whileHover={{ 
        scale: 1.1, 
        y: -4,
        transition: { duration: 0.3 }
      }}
      className="relative group cursor-default"
    >
      <motion.div
        animate={{
          y: [0, -3, 0],
        }}
        transition={{
          duration: 3,
          repeat: Infinity,
          ease: "easeInOut",
          delay: delay * 0.5,
        }}
        className="w-18 h-18 md:w-20 md:h-20 bg-gradient-to-br from-amber-600 to-amber-800 border-2 border-amber-400 rounded-xl flex flex-col items-center justify-center shadow-lg shadow-amber-900/40 hover:shadow-amber-700/60 transition-all relative overflow-hidden"
      >
        {/* Hover shine effect */}
        <motion.div
          initial={{ x: "-100%" }}
          whileHover={{ x: "100%" }}
          transition={{ duration: 0.6 }}
          className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent skew-x-12"
        />
        
        {/* Icon - crisp rendering */}
        <motion.div
          animate={{
            rotate: [0, 3, -3, 0],
          }}
          transition={{
            duration: 4,
            repeat: Infinity,
            ease: "easeInOut",
            delay: delay * 0.3,
          }}
          className="relative mb-0.5 flex items-center justify-center"
          style={{ 
            color: color,
            filter: "drop-shadow(0 2px 4px rgba(0,0,0,0.4))",
          }}
        >
          <div className="text-2xl md:text-3xl flex items-center justify-center" style={{
            WebkitFontSmoothing: "antialiased",
            MozOsxFontSmoothing: "grayscale",
          }}>
            {icon}
          </div>
        </motion.div>
        
        {/* Label */}
        <span className="relative text-[9px] md:text-[10px] text-amber-50 font-bold text-center px-1 leading-tight">
          {label}
        </span>
      </motion.div>
    </motion.div>
  );
}
