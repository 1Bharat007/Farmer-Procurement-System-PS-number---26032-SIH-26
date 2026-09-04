"use client";

import * as React from "react";
import { cn } from "@/lib/utils";

export interface LanguageToggleProps {
  currentLocale?: "en" | "hi";
  onLocaleChange?: (locale: "en" | "hi") => void;
  className?: string;
}

export function LanguageToggle({
  currentLocale = "en",
  onLocaleChange,
  className,
}: LanguageToggleProps) {
  const [selected, setSelected] = React.useState<"en" | "hi">(currentLocale);

  const handleSelect = (locale: "en" | "hi") => {
    setSelected(locale);
    if (onLocaleChange) {
      onLocaleChange(locale);
    }
  };

  return (
    <div
      role="group"
      aria-label="Language selection"
      className={cn(
        "inline-flex items-center rounded-full border border-[#DADCE0] bg-white p-0.5 text-[12px] font-medium select-none shadow-none",
        className
      )}
    >
      <button
        type="button"
        onClick={() => handleSelect("en")}
        aria-pressed={selected === "en"}
        className={cn(
          "rounded-full px-2.5 py-1 transition-colors duration-150 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[#0B3D91]",
          selected === "en"
            ? "bg-[#0B3D91] text-white"
            : "text-[#5F6368] hover:text-[#202124] hover:bg-[#F8F9FA]"
        )}
      >
        English
      </button>
      <button
        type="button"
        onClick={() => handleSelect("hi")}
        aria-pressed={selected === "hi"}
        className={cn(
          "rounded-full px-2.5 py-1 transition-colors duration-150 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[#0B3D91]",
          selected === "hi"
            ? "bg-[#0B3D91] text-white"
            : "text-[#5F6368] hover:text-[#202124] hover:bg-[#F8F9FA]"
        )}
      >
        हिंदी
      </button>
    </div>
  );
}
