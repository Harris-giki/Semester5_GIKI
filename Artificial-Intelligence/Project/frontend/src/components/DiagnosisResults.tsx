"use client";

import React from "react";
import {
  ShieldCheck,
  ShieldWarning,
  Lightning,
  Brain,
  ChartLine,
  ListChecks,
  Clock,
  CaretRight,
} from "@phosphor-icons/react";
import { motion } from "motion/react";
import { cn, getRiskColor, getRiskLabel, formatConfidence } from "@/lib/utils";
import type { DiagnosisResponse } from "@/lib/types";

interface DiagnosisResultsProps {
  results: DiagnosisResponse;
}

export function DiagnosisResults({ results }: DiagnosisResultsProps) {
  const { ml_prediction, expert_analysis, fuzzy_analysis, combined_recommendation } = results;
  
  const isMalignant = ml_prediction.predicted_class === "malignant";
  const isUrgent = combined_recommendation.needs_immediate_attention;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-6"
    >
      {/* Main Result Card */}
      <div
        className={cn(
          "glass-card rounded-xl overflow-hidden",
          isUrgent && "ring-2 ring-danger pulse-urgent"
        )}
      >
        {/* Status bar */}
        <div className={cn("h-1", isMalignant ? "bg-danger" : "bg-success")} />
        
        <div className="p-6">
          <div className="flex items-start justify-between mb-6">
            <div className="flex items-center gap-4">
              <div className={cn(
                "w-14 h-14 rounded-xl flex items-center justify-center",
                isMalignant ? "bg-danger/10" : "bg-success/10"
              )}>
                {isMalignant ? (
                  <ShieldWarning size={32} className="text-danger" weight="fill" />
                ) : (
                  <ShieldCheck size={32} className="text-success" weight="fill" />
                )}
              </div>
              <div>
                <h2 className={cn(
                  "text-2xl font-bold",
                  isMalignant ? "text-danger" : "text-success"
                )}>
                  {isMalignant ? "Malignant Detected" : "Benign Result"}
                </h2>
                <p className="text-muted-foreground mt-1">
                  {combined_recommendation.summary}
                </p>
              </div>
            </div>
            
            <div className={cn(
              "px-4 py-2 rounded-full text-sm font-medium border",
              getRiskColor(combined_recommendation.final_risk_category)
            )}>
              {getRiskLabel(combined_recommendation.final_risk_category)}
            </div>
          </div>

          {/* Score Cards */}
          <div className="grid grid-cols-3 gap-4 mb-6">
            <ScoreCard
              label="ML Confidence"
              value={ml_prediction.confidence * 100}
              format={(v) => `${v.toFixed(1)}%`}
              color={ml_prediction.confidence > 0.8 ? "cyan" : "orange"}
            />
            <ScoreCard
              label="Severity Score"
              value={ml_prediction.severity_score}
              format={(v) => v.toFixed(1)}
              color={ml_prediction.severity_score > 70 ? "red" : ml_prediction.severity_score > 40 ? "orange" : "green"}
            />
            <ScoreCard
              label="Composite Risk"
              value={combined_recommendation.composite_risk_score}
              format={(v) => v.toFixed(1)}
              color={combined_recommendation.composite_risk_score > 70 ? "red" : combined_recommendation.composite_risk_score > 40 ? "orange" : "green"}
            />
          </div>

          {/* Probability Bar */}
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-success font-medium">
                Benign: {formatConfidence(ml_prediction.probabilities.benign)}
              </span>
              <span className="text-danger font-medium">
                Malignant: {formatConfidence(ml_prediction.probabilities.malignant)}
              </span>
            </div>
            <div className="relative h-3 rounded-full overflow-hidden bg-muted">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${ml_prediction.probabilities.benign * 100}%` }}
                transition={{ duration: 0.8, ease: "easeOut" }}
                className="absolute left-0 top-0 h-full bg-gradient-to-r from-success to-success/80 rounded-full"
              />
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${ml_prediction.probabilities.malignant * 100}%` }}
                transition={{ duration: 0.8, ease: "easeOut" }}
                className="absolute right-0 top-0 h-full bg-gradient-to-l from-danger to-danger/80 rounded-full"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Recommendations */}
      <div className="glass-card rounded-xl p-6">
        <h3 className="text-lg font-semibold text-foreground mb-4 flex items-center gap-2">
          <ListChecks size={22} className="text-accent-cyan" />
          Recommendations
        </h3>
        <div className="space-y-3">
          {combined_recommendation.top_recommendations.map((rec, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: idx * 0.1 }}
              className="flex items-start gap-3 p-4 rounded-lg bg-muted/30 border border-border hover:border-accent-cyan/30 transition-colors"
            >
              <CaretRight size={18} className="text-accent-cyan mt-0.5 flex-shrink-0" />
              <span className="text-sm text-foreground/90">{rec}</span>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Analysis Grid */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Expert System */}
        <div className="glass-card rounded-xl p-6">
          <h3 className="text-lg font-semibold text-foreground mb-4 flex items-center gap-2">
            <Brain size={22} className="text-accent-purple" />
            Expert System
          </h3>
          
          <div className="space-y-4">
            <div>
              <h4 className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-3">
                Top Rules Activated
              </h4>
              <div className="space-y-2">
                {expert_analysis.rules_fired.slice(0, 3).map((rule) => (
                  <div
                    key={rule.id}
                    className="p-3 rounded-lg bg-muted/30 border border-border"
                  >
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-[10px] px-1.5 py-0.5 rounded bg-accent-purple/10 text-accent-purple">
                        {rule.id}
                      </span>
                      <span className="text-sm font-medium text-foreground">{rule.name}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="pt-4 border-t border-border">
              <div className="flex items-center gap-2 text-sm">
                <Clock size={16} className="text-muted-foreground" />
                <span className="text-muted-foreground">Follow-up:</span>
                <span className="font-medium text-foreground">
                  {expert_analysis.follow_up.description}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Fuzzy Logic */}
        <div className="glass-card rounded-xl p-6">
          <h3 className="text-lg font-semibold text-foreground mb-4 flex items-center gap-2">
            <ChartLine size={22} className="text-accent-orange" />
            Fuzzy Logic Analysis
          </h3>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 rounded-lg bg-muted/30 border border-border">
              <span className="text-sm text-muted-foreground">Fuzzy Risk Score</span>
              <span className="text-3xl font-bold text-accent-orange">
                {fuzzy_analysis.fuzzy_risk_score.toFixed(1)}
              </span>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-sm text-muted-foreground">Uncertainty Level</span>
              <span
                className={cn(
                  "text-sm font-medium px-3 py-1 rounded-full",
                  fuzzy_analysis.uncertainty_level === "high"
                    ? "bg-danger/10 text-danger"
                    : fuzzy_analysis.uncertainty_level === "moderate"
                    ? "bg-warning/10 text-warning"
                    : "bg-success/10 text-success"
                )}
              >
                {fuzzy_analysis.uncertainty_level.charAt(0).toUpperCase() +
                  fuzzy_analysis.uncertainty_level.slice(1)}
              </span>
            </div>

            <p className="text-sm text-muted-foreground italic pt-2 border-t border-border">
              {fuzzy_analysis.interpretation}
            </p>
          </div>
        </div>
      </div>

      {/* Urgency Alert */}
      {isUrgent && (
        <motion.div
          initial={{ scale: 0.95, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="p-5 rounded-xl bg-danger/10 border-2 border-danger flex items-center gap-4"
        >
          <div className="w-12 h-12 rounded-xl bg-danger/20 flex items-center justify-center flex-shrink-0">
            <Lightning size={28} className="text-danger" weight="fill" />
          </div>
          <div>
            <h4 className="font-semibold text-danger text-lg">Immediate Attention Required</h4>
            <p className="text-sm text-danger/80 mt-1">
              Based on the analysis, this case requires urgent medical consultation.
              Please contact a healthcare provider as soon as possible.
            </p>
          </div>
        </motion.div>
      )}
    </motion.div>
  );
}

interface ScoreCardProps {
  label: string;
  value: number;
  format: (value: number) => string;
  color: "cyan" | "green" | "orange" | "red";
}

function ScoreCard({ label, value, format, color }: ScoreCardProps) {
  const colorClasses = {
    cyan: "text-accent-cyan",
    green: "text-success",
    orange: "text-accent-orange",
    red: "text-danger",
  };

  const bgClasses = {
    cyan: "bg-accent-cyan",
    green: "bg-success",
    orange: "bg-accent-orange",
    red: "bg-danger",
  };

  return (
    <div className="p-4 rounded-lg bg-muted/30 border border-border">
      <div className={cn("text-3xl font-bold mb-1", colorClasses[color])}>
        {format(value)}
      </div>
      <div className="text-xs text-muted-foreground mb-3">{label}</div>
      <div className="h-1.5 bg-muted rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${Math.min(value, 100)}%` }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className={cn("h-full rounded-full", bgClasses[color])}
        />
      </div>
    </div>
  );
}
