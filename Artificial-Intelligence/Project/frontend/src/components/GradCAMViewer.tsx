"use client";

import React, { useState } from "react";
import { 
  Eye, 
  EyeSlash, 
  MagicWand,
  Info,
} from "@phosphor-icons/react";
import { motion } from "motion/react";
import { cn } from "@/lib/utils";

interface GradCAMViewerProps {
  originalImage: string;
  heatmapImage: string | null;
  isLoading: boolean;
  onGenerateGradCAM: () => void;
}

export function GradCAMViewer({
  originalImage,
  heatmapImage,
  isLoading,
  onGenerateGradCAM,
}: GradCAMViewerProps) {
  const [showHeatmap, setShowHeatmap] = useState(true);
  const [opacity, setOpacity] = useState(0.6);

  return (
    <div className="space-y-6">
      {/* Viewer */}
      <div className="glass-card rounded-xl p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-foreground flex items-center gap-2">
            <Eye size={20} className="text-accent-cyan" />
            Grad-CAM Visualization
          </h3>
          
          {heatmapImage && (
            <div className="flex items-center gap-2">
              <button
                onClick={() => setShowHeatmap(!showHeatmap)}
                className={cn(
                  "btn-ghost px-3 py-1.5 rounded-lg flex items-center gap-2 text-sm",
                  showHeatmap && "bg-accent-cyan/10 text-accent-cyan"
                )}
              >
                {showHeatmap ? <Eye size={16} /> : <EyeSlash size={16} />}
                {showHeatmap ? "Heatmap On" : "Heatmap Off"}
              </button>
            </div>
          )}
        </div>

        {/* Image Display */}
        <div className="relative aspect-video bg-muted/20 rounded-xl overflow-hidden flex items-center justify-center">
          {heatmapImage ? (
            <div className="relative">
              <img
                src={originalImage}
                alt="Original mammogram"
                className="max-h-[500px] rounded-lg"
              />
              {showHeatmap && (
                <motion.img
                  initial={{ opacity: 0 }}
                  animate={{ opacity }}
                  src={`data:image/png;base64,${heatmapImage}`}
                  alt="Grad-CAM heatmap"
                  className="absolute inset-0 max-h-[500px] rounded-lg"
                  style={{ mixBlendMode: "screen" }}
                />
              )}
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center py-12">
              <img
                src={originalImage}
                alt="Original mammogram"
                className="max-h-80 rounded-lg mb-6"
              />
              
              <button
                onClick={onGenerateGradCAM}
                disabled={isLoading}
                className={cn(
                  "btn-primary px-6 py-3 rounded-xl flex items-center gap-2 font-semibold",
                  isLoading && "opacity-70 cursor-not-allowed"
                )}
              >
                {isLoading ? (
                  <>
                    <div className="w-5 h-5 border-2 border-black/30 border-t-black rounded-full animate-spin" />
                    Generating...
                  </>
                ) : (
                  <>
                    <MagicWand size={20} weight="bold" />
                    Generate Grad-CAM
                  </>
                )}
              </button>
            </div>
          )}
        </div>

        {/* Opacity Slider */}
        {heatmapImage && (
          <div className="mt-4">
            <div className="flex items-center justify-between text-sm mb-2">
              <span className="text-muted-foreground">Heatmap Opacity</span>
              <span className="text-foreground font-medium">{Math.round(opacity * 100)}%</span>
            </div>
            <input
              type="range"
              min="0"
              max="100"
              value={opacity * 100}
              onChange={(e) => setOpacity(parseInt(e.target.value) / 100)}
              className="w-full h-2 bg-muted rounded-lg appearance-none cursor-pointer accent-accent-cyan"
            />
          </div>
        )}
      </div>

      {/* Info Card */}
      <div className="glass-card rounded-xl p-6">
        <h3 className="text-lg font-semibold text-foreground mb-4 flex items-center gap-2">
          <Info size={20} className="text-accent-purple" />
          What is Grad-CAM?
        </h3>
        
        <div className="space-y-4 text-sm text-muted-foreground">
          <p>
            <strong className="text-foreground">Gradient-weighted Class Activation Mapping (Grad-CAM)</strong> 
            {" "}is an explainable AI technique that produces visual explanations for 
            decisions made by CNN models.
          </p>
          
          <div className="grid md:grid-cols-2 gap-4 pt-2">
            <div className="p-4 rounded-lg bg-muted/20 border border-border">
              <h4 className="font-medium text-foreground mb-2">How it works</h4>
              <p className="text-xs">
                Grad-CAM uses the gradients flowing into the final convolutional layer 
                to highlight important regions in the image that influenced the model&apos;s prediction.
              </p>
            </div>
            
            <div className="p-4 rounded-lg bg-muted/20 border border-border">
              <h4 className="font-medium text-foreground mb-2">Interpretation</h4>
              <ul className="text-xs space-y-1">
                <li className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded bg-red-500" />
                  Red/Yellow = High importance
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded bg-blue-500" />
                  Blue/Purple = Low importance
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
