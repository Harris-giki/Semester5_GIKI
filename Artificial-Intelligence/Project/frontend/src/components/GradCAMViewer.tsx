"use client";

import React, { useState } from "react";
import { Eye, EyeSlash, ArrowsOut, Info } from "@phosphor-icons/react";
import { motion, AnimatePresence } from "motion/react";
import { cn } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";

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
  const [isFullscreen, setIsFullscreen] = useState(false);

  return (
    <>
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <Eye size={22} className="text-primary" />
              Explainability Visualization
            </CardTitle>
            {heatmapImage && (
              <div className="flex items-center gap-2">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setShowHeatmap(!showHeatmap)}
                >
                  {showHeatmap ? (
                    <>
                      <EyeSlash size={18} className="mr-1" />
                      Hide Heatmap
                    </>
                  ) : (
                    <>
                      <Eye size={18} className="mr-1" />
                      Show Heatmap
                    </>
                  )}
                </Button>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => setIsFullscreen(true)}
                >
                  <ArrowsOut size={18} />
                </Button>
              </div>
            )}
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          {!heatmapImage ? (
            <div className="text-center py-8">
              <div className="mx-auto w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mb-4">
                <Eye size={32} className="text-primary" />
              </div>
              <h3 className="text-lg font-medium mb-2">Grad-CAM Visualization</h3>
              <p className="text-sm text-muted-foreground mb-4">
                Generate a heatmap showing which regions of the image
                influenced the model&apos;s decision
              </p>
              <Button onClick={onGenerateGradCAM} disabled={isLoading}>
                {isLoading ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2" />
                    Generating...
                  </>
                ) : (
                  "Generate Grad-CAM"
                )}
              </Button>
            </div>
          ) : (
            <div className="relative">
              <div className="relative rounded-lg overflow-hidden">
                <img
                  src={originalImage}
                  alt="Original mammogram"
                  className={cn(
                    "w-full transition-opacity duration-300",
                    showHeatmap && "opacity-0"
                  )}
                />
                <AnimatePresence>
                  {showHeatmap && (
                    <motion.img
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      exit={{ opacity: 0 }}
                      src={`data:image/png;base64,${heatmapImage}`}
                      alt="Grad-CAM heatmap"
                      className="absolute inset-0 w-full h-full object-cover"
                    />
                  )}
                </AnimatePresence>
              </div>

              {/* Legend */}
              <div className="mt-4 p-3 rounded-lg bg-muted/50 flex items-start gap-3">
                <Info size={18} className="text-info flex-shrink-0 mt-0.5" />
                <div className="text-sm">
                  <p className="font-medium mb-1">How to interpret:</p>
                  <ul className="text-muted-foreground space-y-1">
                    <li>
                      <span className="inline-block w-3 h-3 rounded bg-red-500 mr-2" />
                      Hot (red) areas: High influence on classification
                    </li>
                    <li>
                      <span className="inline-block w-3 h-3 rounded bg-yellow-500 mr-2" />
                      Warm (yellow) areas: Moderate influence
                    </li>
                    <li>
                      <span className="inline-block w-3 h-3 rounded bg-blue-500 mr-2" />
                      Cool (blue) areas: Low influence
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Fullscreen Modal */}
      <AnimatePresence>
        {isFullscreen && heatmapImage && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-4"
            onClick={() => setIsFullscreen(false)}
          >
            <motion.div
              initial={{ scale: 0.9 }}
              animate={{ scale: 1 }}
              exit={{ scale: 0.9 }}
              className="relative max-w-4xl w-full"
              onClick={(e) => e.stopPropagation()}
            >
              <button
                onClick={() => setIsFullscreen(false)}
                className="absolute -top-12 right-0 text-white hover:text-primary transition-colors"
              >
                Press ESC or click outside to close
              </button>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <h4 className="text-white mb-2 text-sm font-medium">Original</h4>
                  <img
                    src={originalImage}
                    alt="Original"
                    className="rounded-lg w-full"
                  />
                </div>
                <div>
                  <h4 className="text-white mb-2 text-sm font-medium">Grad-CAM Overlay</h4>
                  <img
                    src={`data:image/png;base64,${heatmapImage}`}
                    alt="Heatmap"
                    className="rounded-lg w-full"
                  />
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}

