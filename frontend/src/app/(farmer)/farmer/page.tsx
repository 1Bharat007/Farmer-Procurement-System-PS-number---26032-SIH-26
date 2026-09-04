"use client";

import * as React from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { authStorage, FarmerUser } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, Calendar, Clock, LogOut, ShieldCheck, User } from "lucide-react";

export default function FarmerPortalPage() {
  const router = useRouter();
  const [user, setUser] = React.useState<FarmerUser | null>(null);

  React.useEffect(() => {
    const savedUser = authStorage.getUser();
    if (savedUser) {
      setUser(savedUser);
    }
  }, []);

  const handleLogout = () => {
    authStorage.clear();
    router.push("/login/farmer");
  };

  return (
    <div className="min-h-screen bg-[#F8F9FA] text-[#202124] flex flex-col font-sans">
      {/* Top Header */}
      <header className="border-b border-[#DADCE0] bg-white sticky top-0 z-50">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 h-14 sm:h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Link
              href="/"
              className="text-[13px] sm:text-[14px] font-medium text-[#0B3D91] hover:underline flex items-center"
            >
              <ArrowLeft className="w-4 h-4 mr-1.5" />
              Home
            </Link>
            <div className="h-4 w-px bg-[#DADCE0]" />
            <span className="text-[14px] sm:text-[16px] font-medium text-[#202124]">
              Farmer Portal
            </span>
          </div>

          <div className="flex items-center space-x-3">
            {user ? (
              <div className="flex items-center space-x-2">
                <span className="text-[12px] sm:text-[13px] text-[#5F6368] hidden sm:inline">
                  +91 {user.phone}
                </span>
                <Button
                  variant="text"
                  size="sm"
                  onClick={handleLogout}
                  className="text-[#D93025] hover:bg-[#FCE8E6]"
                >
                  <LogOut className="w-4 h-4 mr-1" />
                  Logout
                </Button>
              </div>
            ) : (
              <Link href="/login/farmer">
                <Button variant="outline" size="sm">
                  Sign In
                </Button>
              </Link>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-5xl mx-auto px-4 sm:px-6 py-6 sm:py-8 flex-1 w-full space-y-6">
        {/* Welcome Card */}
        <Card className="border-[#DADCE0] bg-white p-5 sm:p-6 shadow-none">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <div className="flex items-center space-x-2">
                <Badge variant="success" dot>
                  Verified Farmer Session
                </Badge>
                <span className="text-[12px] text-[#5F6368]">
                  ID: {user?.id ? `KS-FARMER-${user.id}` : "Active"}
                </span>
              </div>
              <h1 className="text-[20px] sm:text-[22px] leading-[26px] sm:leading-[28px] font-medium text-[#202124] mt-2">
                Welcome, {user?.full_name || "Farmer"}
              </h1>
              <p className="text-[13px] sm:text-[14px] leading-[18px] sm:leading-[20px] text-[#5F6368] mt-1">
                {user?.district ? `${user.district}, ${user.state || "India"}` : "Kisan Procurement Platform"} • Registered Crop: {user?.crop_type || "Wheat"}
              </p>
            </div>

            <Button variant="default" size="default" className="h-10 text-[14px]">
              <Calendar className="w-4 h-4 mr-2" />
              Book New Delivery Slot
            </Button>
          </div>
        </Card>

        {/* Feature Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 sm:gap-6">
          <Card className="border-[#DADCE0] bg-white p-5 shadow-none hover:border-[#0B3D91] transition-colors">
            <div className="w-8 h-8 rounded-[4px] bg-[#E8F0FE] flex items-center justify-center text-[#0B3D91] mb-3">
              <Calendar className="w-5 h-5" />
            </div>
            <h2 className="text-[16px] font-medium text-[#202124]">
              Slot Booking Engine
            </h2>
            <p className="text-[13px] leading-[18px] text-[#5F6368] mt-1.5">
              Select your nearby Mandi depot, crop variety, and reserved delivery window to avoid waiting queues.
            </p>
          </Card>

          <Card className="border-[#DADCE0] bg-white p-5 shadow-none hover:border-[#0B3D91] transition-colors">
            <div className="w-8 h-8 rounded-[4px] bg-[#E6F4EA] flex items-center justify-center text-[#1E8E3E] mb-3">
              <Clock className="w-5 h-5" />
            </div>
            <h2 className="text-[16px] font-medium text-[#202124]">
              Live Queue Tracker
            </h2>
            <p className="text-[13px] leading-[18px] text-[#5F6368] mt-1.5">
              Real-time WebSocket token tracking with live estimated gate entry and weighbridge timings.
            </p>
          </Card>

          <Card className="border-[#DADCE0] bg-white p-5 shadow-none hover:border-[#0B3D91] transition-colors">
            <div className="w-8 h-8 rounded-[4px] bg-[#FEF7E0] flex items-center justify-center text-[#E37400] mb-3">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <h2 className="text-[16px] font-medium text-[#202124]">
              Direct MSP Settlements
            </h2>
            <p className="text-[13px] leading-[18px] text-[#5F6368] mt-1.5">
              Instant weighment receipts and automated Direct Benefit Transfer (DBT) disbursement status.
            </p>
          </Card>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-[#DADCE0] bg-white py-3 text-center text-[11px] text-[#5F6368]">
        Ministry of Consumer Affairs, Food & Public Distribution • SIH 2026
      </footer>
    </div>
  );
}
