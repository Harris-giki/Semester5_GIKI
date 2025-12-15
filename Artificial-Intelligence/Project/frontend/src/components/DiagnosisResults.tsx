"use client";

import React from "react";
import {
  ShieldCheck,
  ShieldWarning,
  Lightning,
  Lightbulb,
  Brain,
  ChartLine,
  ListChecks,
  Clock,
  Info,
  CaretRight,
} from "@phosphor-icons/react";
import { motion } from "motion/react";
import { cn, getRiskColor, getRiskLabel, formatConfidence } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Progress } from "./ui/progress";
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
      {/* Main Summary Card */}
      <Card
        className={cn(
          "overflow-hidden",
          isUrgent && "ring-2 ring-danger pulse-urgent"
        )}
      >
        <div
          className={cn(
            "h-2",
            isMalignant ? "bg-danger" : "bg-success"
          )}
        />
        <CardHeader className="pb-4">
          <div className="flex items-start justify-between">
            <div>
              <CardTitle className="text-2xl flex items-center gap-3">
                {isMalignant ? (
                  <ShieldWarning size={28} className="text-danger" weight="fill" />
                ) : (
                  <ShieldCheck size={28} className="text-success" weight="fill" />
                )}
                <span className={isMalignant ? "text-danger" : "text-success"}>
                  {isMalignant ? "Malignant Detected" : "Benign Result"}
                </span>
              </CardTitle>
              <p className="text-muted-foreground mt-2">
                {combined_recommendation.summary}
              </p>
            </div>
            <div
              className={cn(
                "px-4 py-2 rounded-full text-sm font-medium border",
                getRiskColor(combined_recommendation.final_risk_category)
              )}
            >
              {getRiskLabel(combined_recommendation.final_risk_category)}
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Confidence & Risk Scores */}
          <div className="grid grid-cols-3 gap-6">
            <ScoreCard
              label="ML Confidence"
              value={ml_prediction.confidence * 100}
              format={(v) => `${v.toFixed(1)}%`}
              color={ml_prediction.confidence > 0.8 ? "primary" : "warning"}
            />
            <ScoreCard
              label="Severity Score"
              value={ml_prediction.severity_score}
              format={(v) => v.toFixed(1)}
              color={ml_prediction.severity_score > 70 ? "danger" : ml_prediction.severity_score > 40 ? "warning" : "success"}
            />
            <ScoreCard
              label="Composite Risk"
              value={combined_recommendation.composite_risk_score}
              format={(v) => v.toFixed(1)}
              color={combined_recommendation.composite_risk_score > 70 ? "danger" : combined_recommendation.composite_risk_score > 40 ? "warning" : "success"}
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
            <div className="relative h-4 rounded-full overflow-hidden bg-success/20">
              <div
                className="absolute left-0 top-0 h-full bg-success transition-all duration-500"
                style={{ width: `${ml_prediction.probabilities.benign * 100}%` }}
              />
              <div
                className="absolute right-0 top-0 h-full bg-danger transition-all duration-500"
                style={{ width: `${ml_prediction.probabilities.malignant * 100}%` }}
              />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Recommendations Card */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <ListChecks size={24} className="text-primary" />
            Recommendations
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="space-y-3">
            {combined_recommendation.top_recommendations.map((rec, idx) => (
              <motion.li
                key={idx}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: idx * 0.1 }}
                className="flex items-start gap-3 p-3 rounded-lg bg-muted/50"
              >
                <CaretRight size={18} className="text-primary mt-0.5 flex-shrink-0" />
                <span className="text-sm">{rec}</span>
              </motion.li>
            ))}
          </ul>
        </CardContent>
      </Card>

      {/* Analysis Details Grid */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Expert System Analysis */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              <Brain size={22} className="text-info" />
              Expert System Analysis
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <h4 className="font-medium text-sm text-muted-foreground">
                Rules Activated
              </h4>
              <div className="space-y-2">
                {expert_analysis.rules_fired.slice(0, 3).map((rule) => (
                  <div
                    key={rule.id}
                    className="p-2 rounded bg-muted/50 text-sm"
                  >
                    <span className="font-mono text-xs text-primary mr-2">
                      {rule.id}
                    </span>
                    {rule.name}
                  </div>
                ))}
              </div>
            </div>
            
            <div className="pt-2 border-t border-border">
              <div className="flex items-center gap-2 text-sm">
                <Clock size={16} className="text-muted-foreground" />
                <span className="text-muted-foreground">Follow-up:</span>
                <span className="font-medium">
                  {expert_analysis.follow_up.description}
                </span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Fuzzy Logic Analysis */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              <ChartLine size={22} className="text-warning" />
              Fuzzy Logic Analysis
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between p-3 rounded-lg bg-muted/50">
              <span className="text-sm text-muted-foreground">Fuzzy Risk Score</span>
              <span className="text-xl font-bold">
                {fuzzy_analysis.fuzzy_risk_score.toFixed(1)}
              </span>
            </div>

            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Uncertainty Level</span>
                <span
                  className={cn(
                    "font-medium",
                    fuzzy_analysis.uncertainty_level === "high"
                      ? "text-danger"
                      : fuzzy_analysis.uncertainty_level === "moderate"
                      ? "text-warning"
                      : "text-success"
                  )}
                >
                  {fuzzy_analysis.uncertainty_level.charAt(0).toUpperCase() +
                    fuzzy_analysis.uncertainty_level.slice(1)}
                </span>
              </div>
            </div>

            <p className="text-sm text-muted-foreground italic">
              {fuzzy_analysis.interpretation}
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Confidence Assessment */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Info size={22} className="text-info" />
            Confidence Assessment
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-start gap-4 p-4 rounded-lg bg-info-light/30">
            <Lightbulb size={24} className="text-info flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="font-medium mb-1">
                {expert_analysis.confidence_assessment.description}
              </h4>
              <p className="text-sm text-muted-foreground">
                {expert_analysis.confidence_assessment.reliability}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Urgency Alert */}
      {isUrgent && (
        <motion.div
          initial={{ scale: 0.95, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="p-4 rounded-xl bg-danger/10 border-2 border-danger flex items-center gap-4"
        >
          <Lightning size={32} className="text-danger" weight="fill" />
          <div>
            <h4 className="font-semibold text-danger">Immediate Attention Required</h4>
            <p className="text-sm text-danger/80">
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
  color: "primary" | "success" | "warning" | "danger";
}

function ScoreCard({ label, value, format, color }: ScoreCardProps) {
  const colorClasses = {
    primary: "text-primary",
    success: "text-success",
    warning: "text-warning",
    danger: "text-danger",
  };

  const progressColors = {
    primary: "bg-primary",
    success: "bg-success",
    warning: "bg-warning",
    danger: "bg-danger",
  };

  return (
    <div className="text-center">
      <div className={cn("text-3xl font-bold mb-1", colorClasses[color])}>
        {format(value)}
      </div>
      <div className="text-xs text-muted-foreground mb-2">{label}</div>
      <Progress
        value={value}
        className="h-1.5"
        indicatorClassName={progressColors[color]}
      />
    </div>
  );
}

