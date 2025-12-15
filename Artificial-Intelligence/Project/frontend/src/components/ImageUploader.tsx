"use client";

import React, { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { 
  UploadSimple, 
  Image as ImageIcon, 
  X,
  MagnifyingGlass,
  Sparkle,
  FileImage,
} from "@phosphor-icons/react";
import { cn } from "@/lib/utils";

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
          "relative border-2 border-dashed rounded-xl transition-all duration-300 cursor-pointer overflow-hidden",
          isDragActive
            ? "border-accent-cyan bg-accent-cyan/5 scale-[1.01]"
            : "border-border hover:border-accent-cyan/50 hover:bg-muted/30",
          isLoading && "opacity-50 cursor-not-allowed pointer-events-none",
          preview ? "p-4" : "p-8"
        )}
      >
        <input {...getInputProps()} />
        
        {preview ? (
          <div className="relative">
            <img
              src={preview}
              alt="Mammogram preview"
              className="max-h-72 mx-auto rounded-lg"
            />
            <button
              onClick={(e) => {
                e.stopPropagation();
                clearImage();
              }}
              className="absolute -top-2 -right-2 p-2 bg-danger text-white rounded-full shadow-lg hover:bg-danger/90 transition-colors"
            >
              <X size={14} weight="bold" />
            </button>
            
            {/* File info */}
            <div className="mt-3 flex items-center justify-center gap-2 text-xs text-muted-foreground">
              <FileImage size={14} />
              <span>{selectedFile?.name}</span>
              <span className="text-muted-foreground/50">•</span>
              <span>{selectedFile && (selectedFile.size / 1024).toFixed(1)} KB</span>
            </div>
          </div>
        ) : (
          <div className="text-center py-6">
            {/* Icon */}
            <div className="relative mx-auto w-16 h-16 mb-4">
              <div className="absolute inset-0 bg-accent-cyan/20 blur-xl rounded-full" />
              <div className={cn(
                "relative w-full h-full rounded-full flex items-center justify-center",
                "bg-gradient-to-br from-accent-cyan/20 to-accent-cyan/5 border border-accent-cyan/20"
              )}>
                {isDragActive ? (
                  <Sparkle size={28} className="text-accent-cyan animate-pulse" weight="fill" />
                ) : (
                  <UploadSimple size={28} className="text-accent-cyan" />
                )}
              </div>
            </div>
            
            <h3 className="text-lg font-semibold text-foreground mb-2">
              {isDragActive ? "Drop your file here" : "Upload Mammogram"}
            </h3>
            <p className="text-sm text-muted-foreground mb-4">
              Drag and drop or{" "}
              <span className="text-accent-cyan font-medium">browse</span>
            </p>
            
            <div className="flex items-center justify-center gap-2 text-xs text-muted-foreground/60">
              <ImageIcon size={14} />
              <span>PNG, JPG, JPEG, BMP, WebP supported</span>
            </div>
          </div>
        )}
        
        {/* Decorative corners */}
        {!preview && (
          <>
            <div className="absolute top-3 left-3 w-6 h-6 border-t-2 border-l-2 border-accent-cyan/30 rounded-tl-lg" />
            <div className="absolute top-3 right-3 w-6 h-6 border-t-2 border-r-2 border-accent-cyan/30 rounded-tr-lg" />
            <div className="absolute bottom-3 left-3 w-6 h-6 border-b-2 border-l-2 border-accent-cyan/30 rounded-bl-lg" />
            <div className="absolute bottom-3 right-3 w-6 h-6 border-b-2 border-r-2 border-accent-cyan/30 rounded-br-lg" />
          </>
        )}
      </div>

      {preview && (
        <button
          onClick={handleAnalyze}
          disabled={isLoading}
          className={cn(
            "w-full btn-primary py-3 rounded-xl flex items-center justify-center gap-2 font-semibold",
            isLoading && "opacity-70 cursor-not-allowed"
          )}
        >
          {isLoading ? (
            <>
              <div className="w-5 h-5 border-2 border-black/30 border-t-black rounded-full animate-spin" />
              Analyzing...
            </>
          ) : (
            <>
              <MagnifyingGlass size={20} weight="bold" />
              Analyze Mammogram
            </>
          )}
        </button>
      )}
    </div>
  );
}
