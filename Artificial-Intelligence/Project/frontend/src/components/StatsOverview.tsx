"use client";

import React from "react";
import { 
  ChartDonut, 
  TrendUp, 
  Brain, 
  CheckCircle 
} from "@phosphor-icons/react";
import { cn } from "@/lib/utils";
import type { DiagnosisResponse } from "@/lib/types";

interface StatsOverviewProps {
  results: DiagnosisResponse | null;
}

export function StatsOverview({ results }: StatsOverviewProps) {
  const stats = [
    {
      label: "Prediction Confidence",
      value: results ? `${(results.ml_prediction.confidence * 100).toFixed(1)}%` : "—",
      subtext: results ? "Current prediction confidence" : "No analysis yet",
      icon: ChartDonut,
      color: "cyan" as const,
      progress: results ? results.ml_prediction.confidence * 100 : 0,
    },
    {
      label: "Risk Score",
      value: results ? results.combined_recommendation.composite_risk_score.toFixed(1) : "—",
      subtext: results ? results.combined_recommendation.final_risk_category : "No analysis",
      icon: TrendUp,
      color: results && results.combined_recommendation.composite_risk_score > 50 ? "orange" as const : "cyan" as const,
      progress: results ? results.combined_recommendation.composite_risk_score : 0,
    },
    {
      label: "Rules Fired",
      value: results ? results.expert_analysis.rules_fired.length.toString() : "—",
      subtext: results ? "Expert system rules" : "No analysis",
      icon: Brain,
      color: "purple" as const,
    },
    {
      label: "Analysis Status",
      value: results ? "Complete" : "Ready",
      subtext: results ? "View results" : "Upload image",
      icon: CheckCircle,
      color: results ? "green" as const : "cyan" as const,
    },
  ];

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      {stats.map((stat, idx) => (
        <StatCard key={idx} {...stat} />
      ))}
    </div>
  );
}

interface StatCardProps {
  label: string;
  value: string;
  subtext: string;
  icon: React.ElementType;
  color: "cyan" | "purple" | "orange" | "green";
  progress?: number;
}

function StatCard({ label, value, subtext, icon: Icon, color, progress }: StatCardProps) {
  const colorClasses = {
    cyan: {
      text: "text-accent-cyan",
      bg: "bg-accent-cyan/10",
      ring: "stroke-accent-cyan",
    },
    purple: {
      text: "text-accent-purple",
      bg: "bg-accent-purple/10",
      ring: "stroke-accent-purple",
    },
    orange: {
      text: "text-accent-orange",
      bg: "bg-accent-orange/10",
      ring: "stroke-accent-orange",
    },
    green: {
      text: "text-success",
      bg: "bg-success/10",
      ring: "stroke-success",
    },
  };

  return (
    <div className="stat-card rounded-xl p-5">
      <div className="flex items-start justify-between mb-4">
        <div className={cn("p-2 rounded-lg", colorClasses[color].bg)}>
          <Icon size={20} className={colorClasses[color].text} />
        </div>
        {progress !== undefined && (
          <MiniDonut progress={progress} color={colorClasses[color].ring} />
        )}
      </div>
      <div className={cn("text-2xl font-bold mb-1", colorClasses[color].text)}>
        {value}
      </div>
      <div className="text-sm text-muted-foreground">{label}</div>
      <div className="text-xs text-muted-foreground/60 mt-1">{subtext}</div>
    </div>
  );
}

function MiniDonut({ progress, color }: { progress: number; color: string }) {
  const radius = 16;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (progress / 100) * circumference;

  return (
    <svg width="40" height="40" className="transform -rotate-90">
      <circle
        cx="20"
        cy="20"
        r={radius}
        fill="none"
        stroke="currentColor"
        strokeWidth="4"
        className="text-muted/30"
      />
      <circle
        cx="20"
        cy="20"
        r={radius}
        fill="none"
        strokeWidth="4"
        strokeDasharray={circumference}
        strokeDashoffset={offset}
        strokeLinecap="round"
        className={color}
      />
    </svg>
  );
}

