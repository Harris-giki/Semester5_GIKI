"use client";

import React, { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { 
  UploadSimple, 
  Image as ImageIcon, 
  X,
  MagnifyingGlass,
  Sparkle
} from "@phosphor-icons/react";
import { cn } from "@/lib/utils";
import { Button } from "./ui/button";

interface ImageUploaderProps {
  onImageSelect: (file: File) => void;
  isLoading: boolean;
}

export function ImageUploader({ onImageSelect, isLoading }: ImageUploaderProps) {
  const [preview, setPreview] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (file) {
      setSelectedFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "image/*": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"],
    },
    maxFiles: 1,
    disabled: isLoading,
  });

  const clearImage = () => {
    setPreview(null);
    setSelectedFile(null);
  };

  const handleAnalyze = () => {
    if (selectedFile) {
      onImageSelect(selectedFile);
    }
  };

  return (
    <div className="space-y-4">
      <div
        {...getRootProps()}
        className={cn(
          "relative border-2 border-dashed rounded-xl p-8 transition-all duration-300 cursor-pointer",
          isDragActive
            ? "border-primary bg-primary/5 scale-[1.02]"
            : "border-border hover:border-primary/50 hover:bg-muted/50",
          isLoading && "opacity-50 cursor-not-allowed",
          preview && "p-4"
        )}
      >
        <input {...getInputProps()} />
        
        {preview ? (
          <div className="relative">
            <img
              src={preview}
              alt="Mammogram preview"
              className="max-h-80 mx-auto rounded-lg shadow-lg"
            />
            <button
              onClick={(e) => {
                e.stopPropagation();
                clearImage();
              }}
              className="absolute -top-2 -right-2 p-1.5 bg-danger text-white rounded-full shadow-md hover:bg-danger/90 transition-colors"
            >
              <X size={16} weight="bold" />
            </button>
          </div>
        ) : (
          <div className="text-center py-8">
            <div className="mx-auto w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mb-4">
              {isDragActive ? (
                <Sparkle size={32} className="text-primary animate-pulse" />
              ) : (
                <UploadSimple size={32} className="text-primary" />
              )}
            </div>
            <h3 className="text-lg font-medium text-foreground mb-2">
              {isDragActive
                ? "Drop your mammogram here"
                : "Upload Mammogram Image"}
            </h3>
            <p className="text-sm text-muted-foreground mb-4">
              Drag and drop or click to select
            </p>
            <div className="flex items-center justify-center gap-2 text-xs text-muted-foreground">
              <ImageIcon size={14} />
              <span>Supports PNG, JPG, JPEG, BMP, WebP</span>
            </div>
          </div>
        )}
      </div>

      {preview && (
        <Button
          onClick={handleAnalyze}
          disabled={isLoading}
          className="w-full"
          size="lg"
        >
          {isLoading ? (
            <>
              <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2" />
              Analyzing...
            </>
          ) : (
            <>
              <MagnifyingGlass size={20} className="mr-2" />
              Analyze Mammogram
            </>
          )}
        </Button>
      )}
    </div>
  );
}

