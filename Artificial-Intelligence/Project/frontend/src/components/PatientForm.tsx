"use client";

import React from "react";
import { 
  User, 
  Heart, 
  FirstAid, 
  Warning,
  Drop,
} from "@phosphor-icons/react";
import { cn } from "@/lib/utils";
import type { PatientData } from "@/lib/types";

interface PatientFormProps {
  patientData: PatientData;
  onChange: (data: PatientData) => void;
}

export function PatientForm({ patientData, onChange }: PatientFormProps) {
  const updateField = <K extends keyof PatientData>(
    field: K,
    value: PatientData[K]
  ) => {
    onChange({ ...patientData, [field]: value });
  };

  return (
    <div className="space-y-5">
      {/* Age Input */}
      <div>
        <label className="flex items-center gap-2 text-sm font-medium text-foreground mb-2">
          <User size={16} className="text-accent-cyan" />
          Age (optional)
        </label>
        <input
          type="number"
          min="18"
          max="120"
          placeholder="Enter patient age"
          value={patientData.age || ""}
          onChange={(e) => updateField("age", e.target.value ? parseInt(e.target.value) : undefined)}
          className="w-full px-4 py-3 rounded-lg bg-muted/30 border border-border text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-accent-cyan/50 focus:ring-1 focus:ring-accent-cyan/20 transition-colors"
        />
      </div>

      {/* Pain Level */}
      <div>
        <label className="flex items-center gap-2 text-sm font-medium text-foreground mb-2">
          <FirstAid size={16} className="text-accent-orange" />
          Pain Level (0-10)
        </label>
        <div className="space-y-2">
          <input
            type="range"
            min="0"
            max="10"
            value={patientData.pain_level || 0}
            onChange={(e) => updateField("pain_level", parseInt(e.target.value))}
            className="w-full h-2 bg-muted rounded-lg appearance-none cursor-pointer accent-accent-cyan"
          />
          <div className="flex justify-between text-xs text-muted-foreground">
            <span>No pain</span>
            <span className="text-foreground font-medium">
              {patientData.pain_level ?? 0}
            </span>
            <span>Severe</span>
          </div>
        </div>
      </div>

      {/* Toggle Options */}
      <div className="space-y-3 pt-2">
        <h4 className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
          Clinical Indicators
        </h4>
        
        <ToggleOption
          icon={Heart}
          label="Family History"
          description="Close relatives with breast cancer"
          checked={patientData.family_history}
          onChange={(checked) => updateField("family_history", checked)}
          color="purple"
        />
        
        <ToggleOption
          icon={Warning}
          label="Lump Detected"
          description="Palpable mass identified"
          checked={patientData.lump_detected}
          onChange={(checked) => updateField("lump_detected", checked)}
          color="orange"
        />
        
        <ToggleOption
          icon={Drop}
          label="Nipple Discharge"
          description="Abnormal nipple secretion"
          checked={patientData.nipple_discharge}
          onChange={(checked) => updateField("nipple_discharge", checked)}
          color="pink"
        />
      </div>
    </div>
  );
}

interface ToggleOptionProps {
  icon: React.ElementType;
  label: string;
  description: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
  color: "purple" | "orange" | "pink";
}

function ToggleOption({ 
  icon: Icon, 
  label, 
  description, 
  checked, 
  onChange,
  color,
}: ToggleOptionProps) {
  const colorClasses = {
    purple: "text-accent-purple",
    orange: "text-accent-orange",
    pink: "text-accent-pink",
  };

  return (
    <label className={cn(
      "flex items-center justify-between p-4 rounded-lg cursor-pointer transition-all",
      "bg-muted/20 border border-border",
      checked && "bg-muted/40 border-accent-cyan/30"
    )}>
      <div className="flex items-center gap-3">
        <Icon size={18} className={colorClasses[color]} />
        <div>
          <p className="text-sm font-medium text-foreground">{label}</p>
          <p className="text-xs text-muted-foreground">{description}</p>
        </div>
      </div>
      
      {/* Custom Toggle */}
      <div className="relative">
        <input
          type="checkbox"
          checked={checked}
          onChange={(e) => onChange(e.target.checked)}
          className="sr-only peer"
        />
        <div className={cn(
          "w-11 h-6 rounded-full transition-colors",
          "bg-muted peer-checked:bg-accent-cyan"
        )} />
        <div className={cn(
          "absolute top-0.5 left-0.5 w-5 h-5 rounded-full transition-transform",
          "bg-foreground peer-checked:translate-x-5"
        )} />
      </div>
    </label>
  );
}
