"use client";

import React from "react";
import { Heartbeat, Sun, Moon, GithubLogo } from "@phosphor-icons/react";
import { useTheme } from "next-themes";
import { Button } from "./ui/button";

export function Header() {
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = React.useState(false);

  React.useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <header className="sticky top-0 z-40 w-full border-b border-border bg-background/80 backdrop-blur-lg">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-primary/10">
            <Heartbeat size={28} className="text-primary" weight="fill" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-foreground">
              Breast Tumor Diagnosis
            </h1>
            <p className="text-xs text-muted-foreground">
              AI-Powered Decision Support System
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Button variant="ghost" size="icon" asChild>
            <a
              href="https://github.com"
              target="_blank"
              rel="noopener noreferrer"
            >
              <GithubLogo size={20} />
            </a>
          </Button>
          
          {mounted && (
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            >
              {theme === "dark" ? <Sun size={20} /> : <Moon size={20} />}
            </Button>
          )}
        </div>
      </div>
    </header>
  );
}

