"use client";

import React from "react";
import { User, FirstAid, Users, Warning } from "@phosphor-icons/react";
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
      <div className="flex items-center gap-2 mb-4">
        <User size={20} className="text-primary" />
        <h3 className="font-medium text-foreground">Patient Information</h3>
        <span className="text-xs text-muted-foreground">(Optional)</span>
      </div>

      <div className="grid grid-cols-2 gap-4">
        {/* Age */}
        <div>
          <label className="block text-sm font-medium text-foreground mb-1.5">
            Age
          </label>
          <input
            type="number"
            min={18}
            max={100}
            placeholder="Enter age"
            value={patientData.age || ""}
            onChange={(e) =>
              updateField("age", e.target.value ? parseInt(e.target.value) : undefined)
            }
            className="w-full px-3 py-2 rounded-lg border border-border bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/50"
          />
        </div>

        {/* Pain Level */}
        <div>
          <label className="block text-sm font-medium text-foreground mb-1.5">
            Pain Level (0-10)
          </label>
          <input
            type="number"
            min={0}
            max={10}
            placeholder="0-10"
            value={patientData.pain_level ?? ""}
            onChange={(e) =>
              updateField(
                "pain_level",
                e.target.value ? parseInt(e.target.value) : undefined
              )
            }
            className="w-full px-3 py-2 rounded-lg border border-border bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/50"
          />
        </div>
      </div>

      {/* Checkboxes */}
      <div className="space-y-3 pt-2">
        <CheckboxField
          checked={patientData.family_history}
          onChange={(v) => updateField("family_history", v)}
          icon={<Users size={16} />}
          label="Family history of breast cancer"
        />

        <CheckboxField
          checked={patientData.lump_detected}
          onChange={(v) => updateField("lump_detected", v)}
          icon={<FirstAid size={16} />}
          label="Lump detected during self-examination"
        />

        <CheckboxField
          checked={patientData.nipple_discharge}
          onChange={(v) => updateField("nipple_discharge", v)}
          icon={<Warning size={16} />}
          label="Nipple discharge present"
        />
      </div>
    </div>
  );
}

interface CheckboxFieldProps {
  checked: boolean;
  onChange: (value: boolean) => void;
  icon: React.ReactNode;
  label: string;
}

function CheckboxField({ checked, onChange, icon, label }: CheckboxFieldProps) {
  return (
    <label
      className={cn(
        "flex items-center gap-3 p-3 rounded-lg border cursor-pointer transition-all duration-200",
        checked
          ? "border-primary bg-primary/5"
          : "border-border hover:border-primary/50"
      )}
    >
      <input
        type="checkbox"
        checked={checked}
        onChange={(e) => onChange(e.target.checked)}
        className="sr-only"
      />
      <div
        className={cn(
          "w-5 h-5 rounded border-2 flex items-center justify-center transition-colors",
          checked
            ? "bg-primary border-primary"
            : "border-border"
        )}
      >
        {checked && (
          <svg
            className="w-3 h-3 text-white"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={3}
              d="M5 13l4 4L19 7"
            />
          </svg>
        )}
      </div>
      <span className={cn("text-muted-foreground", checked && "text-primary")}>
        {icon}
      </span>
      <span className="text-sm text-foreground">{label}</span>
    </label>
  );
}

