/**
 * Shared TypeScript types and interfaces for the portfolio application.
 */

import { ReactNode } from "react";

// ============================================================================
// Chat Types
// ============================================================================

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

export interface StreamChunk {
  chunk: string;
  done: boolean;
  sources?: string[];
}

// ============================================================================
// Portfolio Data Types
// ============================================================================

export interface Project {
  title: string;
  description: string;
  image: string;
  tags: string[];
  github?: string;
  live?: string;
}

export interface Skill {
  name: string;
  icon: ReactNode;
  level: number;
}

export interface SystemMetric {
  label: string;
  value: string;
  icon: ReactNode;
  trend?: string;
}

export interface Benchmark {
  model: string;
  speed: string;
  quality: number;
  memory: string;
}

export interface TimelineItem {
  year: string;
  title: string;
  description: string;
}

// ============================================================================
// Navigation Types
// ============================================================================

export type TabType = "home" | "projects" | "about" | "contact";

// ============================================================================
// API Types
// ============================================================================

export interface HealthResponse {
  status: string;
  version: string;
  timestamp: string;
  services: {
    ollama: string;
    chromadb: string;
  };
}

export interface DocumentMetadata {
  id: string;
  filename: string;
  file_type: string;
  file_size: number;
  chunk_count: number;
  uploaded_at: string;
}

