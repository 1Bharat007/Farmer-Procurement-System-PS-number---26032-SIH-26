import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center whitespace-nowrap rounded-[4px] text-[14px] font-medium tracking-[0.25px] transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#0B3D91] focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-40 select-none",
  {
    variants: {
      variant: {
        // Google Filled (Primary) - Navy background, white text, no gradient, no drop shadows
        default:
          "bg-[#0B3D91] text-white hover:bg-[#082E6E] active:bg-[#062252]",
        // Google Outlined - 1px divider border, navy text, subtle hover
        outline:
          "border border-[#DADCE0] bg-white text-[#0B3D91] hover:bg-[#F8F9FA] active:bg-[#F1F3F4]",
        // Google Text-Only - No border, navy text, light hover
        text:
          "bg-transparent text-[#0B3D91] hover:bg-[#F1F3F4] active:bg-[#E8F0FE]",
        // Secondary subtle filled
        secondary:
          "bg-[#F1F3F4] text-[#202124] hover:bg-[#E8EAED] active:bg-[#DADCE0]",
        // Destructive / Danger
        destructive:
          "bg-[#D93025] text-white hover:bg-[#B3261E] active:bg-[#991B1B]",
        // Destructive text
        destructiveText:
          "bg-transparent text-[#D93025] hover:bg-[#FCE8E6] active:bg-[#FAD2CF]",
      },
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-8 px-3 text-[12px]",
        lg: "h-10 px-6 text-[14px]",
        icon: "h-9 w-9 p-0",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, ...props }, ref) => {
    return (
      <button
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    );
  }
);
Button.displayName = "Button";

export { Button, buttonVariants };
