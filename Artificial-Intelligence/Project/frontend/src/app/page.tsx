"use client";

import React, { useState } from "react";
import { toast } from "sonner";
import { motion, AnimatePresence } from "motion/react";
import * as Tabs from "@radix-ui/react-tabs";
import {
  Upload,
  ChartBar,
  ListBullets,
  Eye,
  ArrowCounterClockwise,
} from "@phosphor-icons/react";
import { Header } from "@/components/Header";
import { ImageUploader } from "@/components/ImageUploader";
import { PatientForm } from "@/components/PatientForm";
import { DiagnosisResults } from "@/components/DiagnosisResults";
import { GradCAMViewer } from "@/components/GradCAMViewer";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { cn, API_BASE_URL } from "@/lib/utils";
import type { DiagnosisResponse, PatientData } from "@/lib/types";

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
  const [activeTab, setActiveTab] = useState("upload");

  const handleImageSelect = async (file: File) => {
    setSelectedImage(file);
    
    // Create preview
    const reader = new FileReader();
    reader.onloadend = () => {
      setImagePreview(reader.result as string);
    };
    reader.readAsDataURL(file);
    
    // Start analysis
    await analyzeMammogram(file);
  };

  const analyzeMammogram = async (file: File) => {
    setIsLoading(true);
    setHeatmapImage(null);
    
    try {
      const formData = new FormData();
      formData.append("image", file);
      formData.append("enhance", "true");
      
      // Add patient data
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
      
      toast.success("Analysis complete!", {
        description: "View your results in the Results tab.",
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
      
      toast.success("Grad-CAM generated!", {
        description: "View the heatmap in the Explainability tab.",
      });
      setActiveTab("explainability");
    } catch (error) {
      console.error("Grad-CAM error:", error);
      toast.error("Grad-CAM generation failed", {
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

  return (
    <div className="min-h-screen gradient-bg">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          {/* Introduction */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-8"
          >
            <h2 className="text-3xl font-bold text-foreground mb-3">
              AI-Powered Breast Tumor Analysis
            </h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Upload a mammogram image for comprehensive analysis combining deep learning
              classification with expert medical knowledge and fuzzy logic reasoning.
            </p>
          </motion.div>

          <Tabs.Root
            value={activeTab}
            onValueChange={setActiveTab}
            className="space-y-6"
          >
            {/* Tab List */}
            <Tabs.List className="flex gap-1 p-1 bg-muted rounded-xl">
              <TabTrigger value="upload" isActive={activeTab === "upload"}>
                <Upload size={18} />
                <span>Upload</span>
              </TabTrigger>
              <TabTrigger
                value="results"
                isActive={activeTab === "results"}
                disabled={!results}
              >
                <ChartBar size={18} />
                <span>Results</span>
              </TabTrigger>
              <TabTrigger
                value="details"
                isActive={activeTab === "details"}
                disabled={!results}
              >
                <ListBullets size={18} />
                <span>Details</span>
              </TabTrigger>
              <TabTrigger
                value="explainability"
                isActive={activeTab === "explainability"}
                disabled={!selectedImage}
              >
                <Eye size={18} />
                <span>Explainability</span>
              </TabTrigger>
            </Tabs.List>

            {/* Upload Tab */}
            <Tabs.Content value="upload">
              <div className="grid lg:grid-cols-2 gap-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Mammogram Image</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ImageUploader
                      onImageSelect={handleImageSelect}
                      isLoading={isLoading}
                    />
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>Patient Information</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <PatientForm
                      patientData={patientData}
                      onChange={setPatientData}
                    />
                  </CardContent>
                </Card>
              </div>
            </Tabs.Content>

            {/* Results Tab */}
            <Tabs.Content value="results">
              <AnimatePresence mode="wait">
                {results ? (
                  <div className="space-y-4">
                    <div className="flex justify-end">
                      <Button variant="outline" onClick={resetAnalysis}>
                        <ArrowCounterClockwise size={18} className="mr-2" />
                        New Analysis
                      </Button>
                    </div>
                    <DiagnosisResults results={results} />
                  </div>
                ) : (
                  <EmptyState
                    message="No analysis results yet"
                    description="Upload a mammogram image to get started"
                  />
                )}
              </AnimatePresence>
            </Tabs.Content>

            {/* Details Tab */}
            <Tabs.Content value="details">
              <AnimatePresence mode="wait">
                {results ? (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="space-y-6"
                  >
                    {/* Image Stats */}
                    <Card>
                      <CardHeader>
                        <CardTitle>Image Analysis</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                          <StatItem
                            label="Dimensions"
                            value={`${results.image_stats.width} × ${results.image_stats.height}`}
                          />
                          <StatItem
                            label="Mean Intensity"
                            value={results.image_stats.mean_intensity.toFixed(1)}
                          />
                          <StatItem
                            label="Std Deviation"
                            value={results.image_stats.std_intensity.toFixed(1)}
                          />
                          <StatItem
                            label="Contrast Ratio"
                            value={`${(results.image_stats.contrast_ratio * 100).toFixed(1)}%`}
                          />
                        </div>
                      </CardContent>
                    </Card>

                    {/* Expert Explanations */}
                    <Card>
                      <CardHeader>
                        <CardTitle>Expert System Explanations</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-4">
                          {results.expert_analysis.explanations.map((exp, idx) => (
                            <div
                              key={idx}
                              className="p-4 rounded-lg bg-muted/50 text-sm"
                            >
                              {exp}
                            </div>
                          ))}
                        </div>
                      </CardContent>
                    </Card>

                    {/* Additional Considerations */}
                    {results.expert_analysis.additional_considerations.length > 0 && (
                      <Card>
                        <CardHeader>
                          <CardTitle>Additional Considerations</CardTitle>
                        </CardHeader>
                        <CardContent>
                          <ul className="space-y-2">
                            {results.expert_analysis.additional_considerations.map(
                              (consideration, idx) => (
                                <li
                                  key={idx}
                                  className="flex items-start gap-2 text-sm"
                                >
                                  <span className="text-primary">•</span>
                                  {consideration}
                                </li>
                              )
                            )}
                          </ul>
                        </CardContent>
                      </Card>
                    )}

                    {/* All Fired Rules */}
                    <Card>
                      <CardHeader>
                        <CardTitle>Rules Activated</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-2">
                          {results.expert_analysis.rules_fired.map((rule) => (
                            <div
                              key={rule.id}
                              className="p-3 rounded-lg border border-border hover:bg-muted/50 transition-colors"
                            >
                              <div className="flex items-center gap-2 mb-1">
                                <span className="font-mono text-xs px-2 py-0.5 rounded bg-primary/10 text-primary">
                                  {rule.id}
                                </span>
                                <span className="font-medium text-sm">
                                  {rule.name}
                                </span>
                              </div>
                              <p className="text-xs text-muted-foreground">
                                {rule.description}
                              </p>
                            </div>
                          ))}
                        </div>
                      </CardContent>
                    </Card>
                  </motion.div>
                ) : (
                  <EmptyState
                    message="No details available"
                    description="Complete an analysis to view detailed information"
                  />
                )}
              </AnimatePresence>
            </Tabs.Content>

            {/* Explainability Tab */}
            <Tabs.Content value="explainability">
              {selectedImage && imagePreview ? (
                <GradCAMViewer
                  originalImage={imagePreview}
                  heatmapImage={heatmapImage}
                  isLoading={isGeneratingGradCAM}
                  onGenerateGradCAM={generateGradCAM}
                />
              ) : (
                <EmptyState
                  message="No image selected"
                  description="Upload an image first to generate explainability visualizations"
                />
              )}
            </Tabs.Content>
          </Tabs.Root>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-border mt-16 py-8">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          <p>
            Hybrid AI-Based Breast Tumor Diagnosis System | CS351 AI Project
          </p>
          <p className="mt-1">
            Combining CNN Classification with Rule-Based Expert Reasoning
          </p>
        </div>
      </footer>
    </div>
  );
}

interface TabTriggerProps {
  value: string;
  isActive: boolean;
  disabled?: boolean;
  children: React.ReactNode;
}

function TabTrigger({ value, isActive, disabled, children }: TabTriggerProps) {
  return (
    <Tabs.Trigger
      value={value}
      disabled={disabled}
      className={cn(
        "flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg text-sm font-medium transition-all duration-200",
        isActive
          ? "bg-background text-foreground shadow-sm"
          : "text-muted-foreground hover:text-foreground",
        disabled && "opacity-50 cursor-not-allowed"
      )}
    >
      {children}
    </Tabs.Trigger>
  );
}

function EmptyState({
  message,
  description,
}: {
  message: string;
  description: string;
}) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="text-center py-16"
    >
      <div className="mx-auto w-20 h-20 bg-muted rounded-full flex items-center justify-center mb-4">
        <ChartBar size={40} className="text-muted-foreground" />
      </div>
      <h3 className="text-lg font-medium text-foreground mb-2">{message}</h3>
      <p className="text-sm text-muted-foreground">{description}</p>
    </motion.div>
  );
}

function StatItem({ label, value }: { label: string; value: string }) {
  return (
    <div className="p-3 rounded-lg bg-muted/50 text-center">
      <div className="text-lg font-semibold text-foreground">{value}</div>
      <div className="text-xs text-muted-foreground">{label}</div>
    </div>
  );
}

