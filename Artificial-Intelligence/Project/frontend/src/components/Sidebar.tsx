"use client";

import React from "react";
import { cn } from "@/lib/utils";

interface NavItem {
  id: string;
  label: string;
  icon: React.ElementType;
  disabled?: boolean;
}

interface SidebarProps {
  items: NavItem[];
  activeTab: string;
  onTabChange: (tab: string) => void;
}

export function Sidebar({ items, activeTab, onTabChange }: SidebarProps) {
  return (
    <aside className="hidden lg:flex flex-col w-64 min-h-[calc(100vh-64px)] border-r border-border bg-background-secondary/50 p-4">
      <nav className="space-y-1">
        {items.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          
          return (
            <button
              key={item.id}
              onClick={() => !item.disabled && onTabChange(item.id)}
              disabled={item.disabled}
              className={cn(
                "w-full nav-item",
                isActive && "active",
                item.disabled && "opacity-40 cursor-not-allowed"
              )}
            >
              <Icon size={20} weight={isActive ? "fill" : "regular"} />
              <span className="text-sm font-medium">{item.label}</span>
            </button>
          );
        })}
      </nav>

      {/* Bottom info */}
      <div className="mt-auto pt-4 border-t border-border">
        <div className="px-3 py-2">
          <p className="text-xs text-muted-foreground">
            Hybrid AI Diagnosis System
          </p>
          <p className="text-xs text-muted-foreground/60 mt-1">
            v1.0.0 • CS351 Project
          </p>
        </div>
      </div>
    </aside>
  );
}

