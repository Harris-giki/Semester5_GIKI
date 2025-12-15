"use client";

import React, { useState } from "react";
import { toast } from "sonner";
import { motion, AnimatePresence } from "motion/react";
import {
  Upload,
  ChartDonut,
  ListBullets,
  Eye,
  ArrowCounterClockwise,
  Brain,
  Pulse,
  Shield,
  Sparkle,
  CaretRight,
} from "@phosphor-icons/react";
import { Header } from "@/components/Header";
import { Sidebar } from "@/components/Sidebar";
import { ImageUploader } from "@/components/ImageUploader";
import { PatientForm } from "@/components/PatientForm";
import { DiagnosisResults } from "@/components/DiagnosisResults";
import { GradCAMViewer } from "@/components/GradCAMViewer";
import { StatsOverview } from "@/components/StatsOverview";
import { cn, API_BASE_URL } from "@/lib/utils";
import type { DiagnosisResponse, PatientData } from "@/lib/types";

type TabValue = "overview" | "upload" | "results" | "details" | "explainability";

export default function Home() {
  const [isLoading, setIsLoading] = useState(false);
  const [isGeneratingGradCAM, setIsGeneratingGradCAM] = useState(false);
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string>("");
  const [results, setResults] = useState<DiagnosisResponse | null>(null);
  const [heatmapImage, setHeatmapImage] = useState<string | null>(null);
  const [patientData, setPatientData] = useState<PatientData>({
    family_history: false,
    lump_detected: false,
    nipple_discharge: false,
  });
  const [activeTab, setActiveTab] = useState<TabValue>("overview");

  const handleImageSelect = async (file: File) => {
    setSelectedImage(file);
    
    const reader = new FileReader();
    reader.onloadend = () => {
      setImagePreview(reader.result as string);
    };
    reader.readAsDataURL(file);
    
    await analyzeMammogram(file);
  };

  const analyzeMammogram = async (file: File) => {
    setIsLoading(true);
    setHeatmapImage(null);
    
    try {
      const formData = new FormData();
      formData.append("image", file);
      formData.append("enhance", "true");
      
      if (patientData.age) {
        formData.append("age", patientData.age.toString());
      }
      if (patientData.pain_level !== undefined) {
        formData.append("pain_level", patientData.pain_level.toString());
      }
      formData.append("family_history", patientData.family_history.toString());
      formData.append("lump_detected", patientData.lump_detected.toString());
      formData.append("nipple_discharge", patientData.nipple_discharge.toString());

      const response = await fetch(`${API_BASE_URL}/api/diagnose`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Analysis failed");
      }

      const data: DiagnosisResponse = await response.json();
      setResults(data);
      setActiveTab("results");
      
      toast.success("Analysis complete", {
        description: "View your diagnosis results now.",
      });
    } catch (error) {
      console.error("Analysis error:", error);
      toast.error("Analysis failed", {
        description: "Please check if the backend server is running.",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const generateGradCAM = async () => {
    if (!selectedImage) return;
    
    setIsGeneratingGradCAM(true);
    
    try {
      const formData = new FormData();
      formData.append("image", selectedImage);

      const response = await fetch(`${API_BASE_URL}/api/gradcam`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Grad-CAM generation failed");
      }

      const data = await response.json();
      setHeatmapImage(data.heatmap);
      
      toast.success("Visualization ready", {
        description: "Grad-CAM heatmap generated successfully.",
      });
      setActiveTab("explainability");
    } catch (error) {
      console.error("Grad-CAM error:", error);
      toast.error("Generation failed", {
        description: "Please try again.",
      });
    } finally {
      setIsGeneratingGradCAM(false);
    }
  };

  const resetAnalysis = () => {
    setSelectedImage(null);
    setImagePreview("");
    setResults(null);
    setHeatmapImage(null);
    setActiveTab("upload");
  };

  const navItems = [
    { id: "overview" as const, label: "Overview", icon: ChartDonut },
    { id: "upload" as const, label: "New Analysis", icon: Upload },
    { id: "results" as const, label: "Results", icon: Pulse, disabled: !results },
    { id: "details" as const, label: "Details", icon: ListBullets, disabled: !results },
    { id: "explainability" as const, label: "Explainability", icon: Eye, disabled: !selectedImage },
  ];

  return (
    <div className="min-h-screen livekit-bg">
      <Header />
      
      <div className="flex">
        {/* Sidebar */}
        <Sidebar 
          items={navItems} 
          activeTab={activeTab} 
          onTabChange={setActiveTab}
        />

        {/* Main Content */}
        <main className="flex-1 p-6 lg:p-8">
          <div className="max-w-7xl mx-auto">
            <AnimatePresence mode="wait">
              {/* Overview Tab */}
              {activeTab === "overview" && (
                <motion.div
                  key="overview"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  className="space-y-8"
                >
                  {/* Hero Section */}
                  <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-[#0c0c0e] to-[#18181b] border border-border p-8 lg:p-12">
                    <div className="absolute inset-0 dot-pattern opacity-50" />
                    <div className="relative z-10">
                      <div className="flex items-center gap-2 text-accent-cyan text-sm font-medium mb-4">
                        <Sparkle size={16} weight="fill" />
                        <span>AI-Powered Diagnosis</span>
                      </div>
                      <h1 className="text-4xl lg:text-5xl font-bold text-foreground mb-4">
                        Breast Tumor<br />
                        <span className="text-accent-cyan">Analysis System</span>
                      </h1>
                      <p className="text-muted-foreground max-w-xl text-lg mb-8">
                        Combining deep learning classification with rule-based expert 
                        reasoning and fuzzy logic for comprehensive tumor analysis.
                      </p>
                      <button
                        onClick={() => setActiveTab("upload")}
                        className="btn-primary px-6 py-3 rounded-lg flex items-center gap-2"
                      >
                        Start Analysis
                        <CaretRight size={18} weight="bold" />
                      </button>
                    </div>
                    
                    {/* Decorative gradient */}
                    <div className="absolute -right-20 -top-20 w-80 h-80 bg-accent-cyan/10 rounded-full blur-3xl" />
                    <div className="absolute -right-10 -bottom-10 w-60 h-60 bg-accent-purple/10 rounded-full blur-3xl" />
                  </div>

                  {/* Stats Overview */}
                  <StatsOverview results={results} />

                  {/* Features Grid */}
                  <div className="grid md:grid-cols-3 gap-6">
                    <FeatureCard
                      icon={Brain}
                      title="CNN Classification"
                      description="ResNet50-based deep learning model trained on mammogram images for accurate tumor detection."
                      color="cyan"
                    />
                    <FeatureCard
                      icon={Shield}
                      title="Expert System"
                      description="Rule-based reasoning implementing clinical guidelines for comprehensive risk assessment."
                      color="purple"
                    />
                    <FeatureCard
                      icon={Pulse}
                      title="Fuzzy Logic"
                      description="Handles uncertainty in medical data to provide nuanced risk scoring and interpretations."
                      color="orange"
                    />
                  </div>
                </motion.div>
              )}

              {/* Upload Tab */}
              {activeTab === "upload" && (
                <motion.div
                  key="upload"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  className="space-y-6"
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <h2 className="text-2xl font-bold text-foreground">New Analysis</h2>
                      <p className="text-muted-foreground mt-1">
                        Upload a mammogram image and provide patient information
                      </p>
                    </div>
                  </div>

                  <div className="grid lg:grid-cols-2 gap-6">
                    <div className="glass-card rounded-xl p-6">
                      <h3 className="text-lg font-semibold text-foreground mb-4 flex items-center gap-2">
                        <Upload size={20} className="text-accent-cyan" />
                        Mammogram Image
                      </h3>
                      <ImageUploader
                        onImageSelect={handleImageSelect}
                        isLoading={isLoading}
                      />
                    </div>

                    <div className="glass-card rounded-xl p-6">
                      <h3 className="text-lg font-semibold text-foreground mb-4 flex items-center gap-2">
                        <ListBullets size={20} className="text-accent-purple" />
                        Patient Information
                      </h3>
                      <PatientForm
                        patientData={patientData}
                        onChange={setPatientData}
                      />
                    </div>
                  </div>
                </motion.div>
              )}

              {/* Results Tab */}
              {activeTab === "results" && (
                <motion.div
                  key="results"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  className="space-y-6"
                >
                  {results ? (
                    <>
                      <div className="flex items-center justify-between">
                        <div>
                          <h2 className="text-2xl font-bold text-foreground">Analysis Results</h2>
                          <p className="text-muted-foreground mt-1">
                            AI-powered diagnosis and risk assessment
                          </p>
                        </div>
                        <button
                          onClick={resetAnalysis}
                          className="btn-ghost px-4 py-2 rounded-lg flex items-center gap-2"
                        >
                          <ArrowCounterClockwise size={18} />
                          New Analysis
                        </button>
                      </div>
                      <DiagnosisResults results={results} />
                    </>
                  ) : (
                    <EmptyState
                      icon={ChartDonut}
                      title="No results yet"
                      description="Upload and analyze a mammogram to see results"
                      action={() => setActiveTab("upload")}
                      actionLabel="Start Analysis"
                    />
                  )}
                </motion.div>
              )}

              {/* Details Tab */}
              {activeTab === "details" && (
                <motion.div
                  key="details"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  className="space-y-6"
                >
                  {results ? (
                    <>
                      <div>
                        <h2 className="text-2xl font-bold text-foreground">Detailed Analysis</h2>
                        <p className="text-muted-foreground mt-1">
                          In-depth breakdown of the diagnostic process
                        </p>
                      </div>
                      
                      {/* Image Stats */}
                      <div className="glass-card rounded-xl p-6">
                        <h3 className="text-lg font-semibold text-foreground mb-4">Image Statistics</h3>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                          <StatBox label="Dimensions" value={`${results.image_stats.width} × ${results.image_stats.height}`} />
                          <StatBox label="Mean Intensity" value={results.image_stats.mean_intensity.toFixed(1)} />
                          <StatBox label="Std Deviation" value={results.image_stats.std_intensity.toFixed(1)} />
                          <StatBox label="Contrast" value={`${(results.image_stats.contrast_ratio * 100).toFixed(1)}%`} />
                        </div>
                      </div>

                      {/* Expert Explanations */}
                      <div className="glass-card rounded-xl p-6">
                        <h3 className="text-lg font-semibold text-foreground mb-4">Expert System Explanations</h3>
                        <div className="space-y-3">
                          {results.expert_analysis.explanations.map((exp, idx) => (
                            <div
                              key={idx}
                              className="p-4 rounded-lg bg-muted/30 text-sm text-foreground/90 border border-border"
                            >
                              {exp}
                            </div>
                          ))}
                        </div>
                      </div>

                      {/* Rules Fired */}
                      <div className="glass-card rounded-xl p-6">
                        <h3 className="text-lg font-semibold text-foreground mb-4">Rules Activated</h3>
                        <div className="grid md:grid-cols-2 gap-3">
                          {results.expert_analysis.rules_fired.map((rule) => (
                            <div
                              key={rule.id}
                              className="p-4 rounded-lg bg-muted/20 border border-border hover:border-accent-cyan/30 transition-colors"
                            >
                              <div className="flex items-center gap-2 mb-2">
                                <span className="font-mono text-xs px-2 py-1 rounded bg-accent-cyan/10 text-accent-cyan">
                                  {rule.id}
                                </span>
                                <span className="font-medium text-sm text-foreground">
                                  {rule.name}
                                </span>
                              </div>
                              <p className="text-xs text-muted-foreground">
                                {rule.description}
                              </p>
                            </div>
                          ))}
                        </div>
                      </div>
                    </>
                  ) : (
                    <EmptyState
                      icon={ListBullets}
                      title="No details available"
                      description="Complete an analysis to view detailed information"
                      action={() => setActiveTab("upload")}
                      actionLabel="Start Analysis"
                    />
                  )}
                </motion.div>
              )}

              {/* Explainability Tab */}
              {activeTab === "explainability" && (
                <motion.div
                  key="explainability"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                >
                  {selectedImage && imagePreview ? (
                    <>
                      <div className="mb-6">
                        <h2 className="text-2xl font-bold text-foreground">Model Explainability</h2>
                        <p className="text-muted-foreground mt-1">
                          Grad-CAM visualization showing areas of interest
                        </p>
                      </div>
                      <GradCAMViewer
                        originalImage={imagePreview}
                        heatmapImage={heatmapImage}
                        isLoading={isGeneratingGradCAM}
                        onGenerateGradCAM={generateGradCAM}
                      />
                    </>
                  ) : (
                    <EmptyState
                      icon={Eye}
                      title="No image selected"
                      description="Upload an image to generate explainability visualizations"
                      action={() => setActiveTab("upload")}
                      actionLabel="Upload Image"
                    />
                  )}
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </main>
      </div>
    </div>
  );
}

function FeatureCard({
  icon: Icon,
  title,
  description,
  color,
}: {
  icon: React.ElementType;
  title: string;
  description: string;
  color: "cyan" | "purple" | "orange";
}) {
  const colorClasses = {
    cyan: "text-accent-cyan bg-accent-cyan/10",
    purple: "text-accent-purple bg-accent-purple/10",
    orange: "text-accent-orange bg-accent-orange/10",
  };

  return (
    <div className="stat-card rounded-xl p-6">
      <div className={cn("w-12 h-12 rounded-lg flex items-center justify-center mb-4", colorClasses[color])}>
        <Icon size={24} />
      </div>
      <h3 className="font-semibold text-foreground mb-2">{title}</h3>
      <p className="text-sm text-muted-foreground">{description}</p>
    </div>
  );
}

function StatBox({ label, value }: { label: string; value: string }) {
  return (
    <div className="p-4 rounded-lg bg-muted/20 text-center">
      <div className="text-xl font-semibold text-foreground">{value}</div>
      <div className="text-xs text-muted-foreground mt-1">{label}</div>
    </div>
  );
}

function EmptyState({
  icon: Icon,
  title,
  description,
  action,
  actionLabel,
}: {
  icon: React.ElementType;
  title: string;
  description: string;
  action: () => void;
  actionLabel: string;
}) {
  return (
    <div className="flex flex-col items-center justify-center py-20">
      <div className="w-20 h-20 rounded-full bg-muted/50 flex items-center justify-center mb-6">
        <Icon size={40} className="text-muted-foreground" />
      </div>
      <h3 className="text-xl font-semibold text-foreground mb-2">{title}</h3>
      <p className="text-muted-foreground mb-6">{description}</p>
      <button
        onClick={action}
        className="btn-primary px-6 py-2 rounded-lg flex items-center gap-2"
      >
        {actionLabel}
        <CaretRight size={16} weight="bold" />
      </button>
    </div>
  );
}
