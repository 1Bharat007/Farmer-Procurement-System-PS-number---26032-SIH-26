import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const badgeVariants = cva(
  "inline-flex items-center rounded-full px-2.5 py-0.5 text-[12px] leading-[16px] font-medium transition-colors select-none",
  {
    variants: {
      variant: {
        // Google Status Chips - Light tint background + dark contrast text
        success:
          "bg-[#E6F4EA] text-[#137333] border border-[#CEEAD6]",
        error:
          "bg-[#FCE8E6] text-[#C5221F] border border-[#FAD2CF]",
        warning:
          "bg-[#FEF7E0] text-[#B06000] border border-[#FEEFC3]",
        info:
          "bg-[#E8F0FE] text-[#1A73E8] border border-[#D2E3FC]",
        neutral:
          "bg-[#F1F3F4] text-[#3C4043] border border-[#DADCE0]",
      },
    },
    defaultVariants: {
      variant: "neutral",
    },
  }
);

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {
  dot?: boolean;
}

function Badge({ className, variant, dot = false, children, ...props }: BadgeProps) {
  const dotColors: Record<string, string> = {
    success: "bg-[#1E8E3E]",
    error: "bg-[#D93025]",
    warning: "bg-[#E37400]",
    info: "bg-[#1A73E8]",
    neutral: "bg-[#5F6368]",
  };

  const selectedDotColor = variant && dotColors[variant] ? dotColors[variant] : dotColors.neutral;

  return (
    <div className={cn(badgeVariants({ variant }), className)} {...props}>
      {dot && (
        <span
          className={cn("w-1.5 h-1.5 rounded-full mr-1.5 shrink-0", selectedDotColor)}
        />
      )}
      {children}
    </div>
  );
}

export { Badge, badgeVariants };
