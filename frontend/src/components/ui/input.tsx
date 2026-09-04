import * as React from "react";
import { cn } from "@/lib/utils";

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  helperText?: string;
  errorMessage?: string;
  error?: boolean;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  (
    {
      className,
      type = "text",
      label,
      helperText,
      errorMessage,
      error = false,
      id,
      disabled,
      required,
      ...props
    },
    ref
  ) => {
    const generatedId = React.useId();
    const inputId = id || generatedId;
    const hasError = error || Boolean(errorMessage);

    return (
      <div className="w-full flex flex-col space-y-1">
        {label && (
          <label
            htmlFor={inputId}
            className={cn(
              "text-[12px] leading-[16px] font-medium transition-colors",
              hasError
                ? "text-[#D93025]"
                : disabled
                ? "text-[#80868B]"
                : "text-[#5F6368] peer-focus:text-[#0B3D91]"
            )}
          >
            {label}
            {required && <span className="text-[#D93025] ml-0.5">*</span>}
          </label>
        )}
        <div className="relative">
          <input
            id={inputId}
            type={type}
            disabled={disabled}
            required={required}
            className={cn(
              "peer flex h-10 w-full rounded-[4px] border bg-white px-3 py-2 text-[14px] leading-[20px] text-[#202124] placeholder:text-[#80868B] transition-colors focus-visible:outline-none focus-visible:ring-1 disabled:cursor-not-allowed disabled:bg-[#F8F9FA] disabled:text-[#80868B] disabled:border-[#DADCE0]",
              hasError
                ? "border-[#D93025] focus-visible:border-[#D93025] focus-visible:ring-[#D93025]"
                : "border-[#DADCE0] hover:border-[#BDC1C6] focus-visible:border-[#0B3D91] focus-visible:ring-[#0B3D91]",
              className
            )}
            ref={ref}
            {...props}
          />
        </div>
        {hasError && errorMessage ? (
          <p className="text-[12px] leading-[16px] text-[#D93025] font-normal">
            {errorMessage}
          </p>
        ) : helperText ? (
          <p className="text-[12px] leading-[16px] text-[#5F6368] font-normal">
            {helperText}
          </p>
        ) : null}
      </div>
    );
  }
);
Input.displayName = "Input";

export { Input };
