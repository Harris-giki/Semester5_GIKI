"use client";

import React from "react";
import { Heartbeat, GithubLogo } from "@phosphor-icons/react";

export function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-border bg-background/80 backdrop-blur-xl">
      <div className="flex items-center justify-between h-16 px-6">
        {/* Logo */}
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="absolute inset-0 bg-accent-cyan/20 blur-lg rounded-lg" />
            <div className="relative p-2 rounded-lg bg-gradient-to-br from-accent-cyan/20 to-accent-cyan/5 border border-accent-cyan/20">
              <Heartbeat size={24} className="text-accent-cyan" weight="fill" />
            </div>
          </div>
          <div>
            <h1 className="text-base font-semibold text-foreground flex items-center gap-2">
              TumorDiagnosis
              <span className="text-[10px] font-medium px-1.5 py-0.5 rounded bg-accent-cyan/10 text-accent-cyan">
                AI
              </span>
            </h1>
            <p className="text-xs text-muted-foreground">
              Decision Support System
            </p>
          </div>
        </div>


        {/* Right side */}
        <div className="flex items-center gap-2">
          <a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            className="btn-ghost p-2 rounded-lg"
          >
            <GithubLogo size={20} />
          </a>
        </div>
      </div>
    </header>
  );
}

function NavLink({ children, active }: { children: React.ReactNode; active?: boolean }) {
  return (
    <button
      className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
        active 
          ? "text-foreground bg-muted" 
          : "text-muted-foreground hover:text-foreground hover:bg-muted/50"
      }`}
    >
      {children}
    </button>
  );
}
