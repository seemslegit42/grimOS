// packages/client/src/pages/Dashboard.tsx
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
    ChartContainer,
    ChartLegend,
    ChartLegendContent,
    ChartTooltip,
    ChartTooltipContent,
} from "@/components/ui/chart";
import { ScrollArea } from "@/components/ui/scroll-area";
import { UserButton, useUser } from "@clerk/clerk-react";
import { motion } from "framer-motion";
import {
    AlertTriangle,
    BarChart3,
    Bell,
    Brain,
    Briefcase,
    Cpu,
    DraftingCompass,
    LayoutDashboard,
    Lightbulb,
    LogOut,
    Menu,
    MessageSquare,
    ScrollText,
    Settings,
    Settings2,
    Shield,
    Users,
    X,
    Zap
} from "lucide-react";
import React, { useState } from 'react';
import { Bar, BarChart, CartesianGrid, Cell, Pie, PieChart, Tooltip as RechartsTooltip, ResponsiveContainer, XAxis, YAxis } from "recharts";
import { useLocation } from "wouter";

// Helper to generate mock data for charts
const generate_mock_chart_data = (num_points = 7, min_value = 50, max_value = 200) => {
  return Array.from({ length: num_points }, (_, i) => ({
    name: `Day ${i + 1}`,
    value: Math.floor(Math.random() * (max_value - min_value + 1)) + min_value,
    uv: Math.floor(Math.random() * (max_value - min_value + 1)) + min_value, // for 2-line charts
  }));
};

const mock_security_alerts = [
  { id: 'alert1', severity: 'Critical', description: 'Anomalous login detected from unauthorized IP.', time: '2m ago', icon: <AlertTriangle className="h-4 w-4 text-red-500" /> },
  { id: 'alert2', severity: 'High', description: 'Potential malware signature found in /var/sys.', time: '15m ago', icon: <AlertTriangle className="h-4 w-4 text-orange-500" /> },
  { id: 'alert3', severity: 'Medium', description: 'Multiple failed login attempts for user "admin".', time: '1h ago', icon: <AlertTriangle className="h-4 w-4 text-yellow-500" /> },
];

const mock_active_workflows = [
  { id: 'wf1', name: 'Automated Threat Remediation', status: 'Active', progress: 75, color: 'text-lime-400' },
  { id: 'wf2', name: 'Resource Scaling Protocol', status: 'Pending', progress: 20, color: 'text-blue-400' },
  { id: 'wf3', name: 'Data Integrity Check', status: 'Error', progress: 90, color: 'text-red-500' },
];

const mock_cognitive_insights = [
  { id: 'ci1', text: 'Predicted 15% increase in operational efficiency by Q3.', source: 'Cognitive Core Forecasting' },
  { id: 'ci2', text: 'Identified emerging vulnerability pattern in sector XYZ.', source: 'PhantomIntel™ Module' },
];

const kpi_data = [
  { title: "Threat Intel Level", value: "98.2%", trend: "+0.5%", color: "text-lime-400", icon: <Shield className="h-6 w-6" /> },
  { title: "Process Efficiency", value: "147%", trend: "+2.1%", color: "text-lime-400", icon: <Zap className="h-6 w-6" /> },
  { title: "Cognitive Core Status", value: "Autonomous", trend: "Optimal", color: "text-blue-400", icon: <Brain className="h-6 w-6" /> },
  { title: "RuneForge Workflows", value: "12 Active", trend: "3 Pending", color: "text-blue-400", icon: <DraftingCompass className="h-6 w-6" /> },
];


// Chart Config for shadcn/ui charts
const chart_config = {
  value: { label: "Value", color: "hsl(var(--chart-1))" },
  desktop: { label: "Desktop", color: "hsl(var(--chart-1))" },
  mobile: { label: "Mobile", color: "hsl(var(--chart-2))" },
} satisfies import("@/components/ui/chart").ChartConfig;


// Sidebar Component
const GrimOsSidebar: React.FC<{ isOpen: boolean; toggleSidebar: () => void; isMobile: boolean }> = ({ isOpen, toggleSidebar, isMobile }) => {
  const [_, navigate] = useLocation();
  const navItems = [
    { name: "Dashboard", icon: LayoutDashboard, path: "/dashboard" },
    { name: "Security Hub", icon: Shield, path: "/dashboard/security" },
    { name: "Operations Center", icon: Settings2, path: "/dashboard/operations" },
    { name: "Cognitive Core", icon: Brain, path: "/dashboard/cognitive" },
    { name: "RuneForge", icon: DraftingCompass, path: "/dashboard/runeforge" },
    { name: "ScrollWeaver", icon: ScrollText, path: "/dashboard/scrollweaver" },
    { name: "System Settings", icon: Settings, path: "/dashboard/settings" },
  ];

  const sidebarVariants = {
    open: { x: 0, width: isMobile ? "80%" : "280px" },
    closed: { x: "-100%", width: isMobile ? "80%" : "280px" },
  };
  
  const mobileOverlayVariants = {
    open: { opacity: 1, pointerEvents: "auto" as "auto" },
    closed: { opacity: 0, pointerEvents: "none" as "none" },
  };

  return (
    <>
      {isMobile && (
        <motion.div
          variants={mobileOverlayVariants}
          initial="closed"
          animate={isOpen ? "open" : "closed"}
          transition={{ duration: 0.3 }}
          className="fixed inset-0 bg-black/50 z-40 md:hidden"
          onClick={toggleSidebar}
        />
      )}
      <motion.aside
        variants={sidebarVariants}
        initial={isMobile ? "closed" : "open"}
        animate={isOpen || !isMobile ? "open" : "closed"}
        transition={{ type: "spring", stiffness: 300, damping: 30 }}
        className={`glass fixed top-0 left-0 h-full z-50 flex flex-col border-r border-white/10 shadow-2xl ${isMobile ? 'w-4/5 max-w-xs' : 'w-72'}`}
      >
        <div className="p-6 border-b border-white/10 flex items-center justify-between">
          <div 
            className="flex items-center space-x-2 cursor-pointer"
            onClick={() => navigate("/")}
          >
            <span className="text-2xl font-bold bg-gradient-to-r from-[#7ED321] to-[#00BFFF] bg-clip-text text-transparent">
              grimOS
            </span>
          </div>
          {isMobile && (
            <Button variant="ghost" size="icon" onClick={toggleSidebar} className="text-white hover:text-lime-400">
              <X className="h-6 w-6" />
            </Button>
          )}
        </div>
        <ScrollArea className="flex-1">
          <nav className="p-4 space-y-2">
            {navItems.map((item) => (
              <Button
                key={item.name}
                variant="ghost"
                className="w-full justify-start text-white/80 hover:text-lime-400 hover:bg-lime-500/10 space-x-3 rounded-lg"
                onClick={() => {
                  navigate(item.path);
                  if (isMobile) toggleSidebar();
                }}
              >
                <item.icon className="h-5 w-5" />
                <span>{item.name}</span>
              </Button>
            ))}
          </nav>
        </ScrollArea>
        <div className="p-4 mt-auto border-t border-white/10">
          <Button variant="ghost" className="w-full justify-start text-white/80 hover:text-red-500/80 hover:bg-red-500/10 space-x-3 rounded-lg">
            <LogOut className="h-5 w-5" />
            <span>Logout (Placeholder)</span>
          </Button>
        </div>
      </motion.aside>
    </>
  );
};

// Header Component
const GrimOsHeader: React.FC<{ toggleSidebar: () => void }> = ({ toggleSidebar }) => {
  const { user } = useUser();
  return (
    <header className="glass sticky top-0 z-30 px-4 sm:px-6 py-3 border-b border-white/10">
      <div className="container mx-auto flex items-center justify-between max-w-full">
        <Button variant="ghost" size="icon" onClick={toggleSidebar} className="text-white hover:text-lime-400 md:hidden">
          <Menu className="h-6 w-6" />
        </Button>
        <div className="hidden md:block">
          <h1 className="text-xl font-semibold text-white/90">Welcome, {user?.firstName || "Operator"}</h1>
        </div>
        <div className="flex items-center space-x-4">
          <Button variant="ghost" size="icon" className="text-white hover:text-lime-400 relative">
            <Bell className="h-5 w-5" />
            <span className="absolute top-0 right-0 block h-2 w-2 rounded-full bg-red-500 ring-2 ring-offset-1 ring-offset-background ring-red-500/50"></span>
          </Button>
          <UserButton afterSignOutUrl="/" appearance={{
            elements: {
              userButtonAvatarBox: "w-8 h-8 ring-2 ring-lime-500/50 hover:ring-lime-400 transition-all",
              userButtonPopoverCard: "glassmorphic-popover", // Custom class for popover
            }
          }} />
        </div>
      </div>
    </header>
  );
};

// KPI Card Component
const KpiCard: React.FC<{ title: string; value: string; trend: string; color: string; icon: React.ReactNode; delay: number }> = ({ title, value, trend, color, icon, delay }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.5, delay }}
  >
    <Card className="glass-darker border-white/10 shadow-lg hover:border-lime-400/30 transition-all duration-300 hover:shadow-lime-500/10">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className={`text-sm font-medium ${color}`}>{title}</CardTitle>
        <span className={color}>{icon}</span>
      </CardHeader>
      <CardContent>
        <div className="text-3xl font-bold text-white">{value}</div>
        <p className="text-xs text-white/60">{trend}</p>
      </CardContent>
    </Card>
  </motion.div>
);

// Widget Shell Component
const DashboardWidget: React.FC<{ title: string; icon?: React.ReactNode; children: React.ReactNode; className?: string; delay?: number, accentColor?: string }> = 
({ title, icon, children, className = "", delay = 0, accentColor = "border-lime-400/30" }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.5, delay }}
    className="h-full"
  >
    <Card className={`glass-darker border-white/10 shadow-lg transition-all duration-300 hover:shadow-xl h-full flex flex-col ${className}`} style={{ '--accent-hover-border': accentColor }} data-accent-color={accentColor}>
      <CardHeader className="pb-3">
        <div className="flex items-center space-x-2">
          {icon && <span className={accentColor.replace('border-', 'text-').replace('/30', '')}>{icon}</span>}
          <CardTitle className="text-lg font-semibold text-white/90">{title}</CardTitle>
        </div>
      </CardHeader>
      <CardContent className="flex-grow overflow-hidden">
        {children}
      </CardContent>
    </Card>
  </motion.div>
);


// Main Dashboard Page Component
export default function Dashboard() {
  const { isLoaded, isSignedIn } = useUser();
  const [_, navigate] = useLocation();
  const [is_sidebar_open, set_is_sidebar_open] = useState(false);
  const [is_mobile, set_is_mobile] = useState(false);

  React.useEffect(() => {
    const check_mobile = () => set_is_mobile(window.innerWidth < 768);
    check_mobile();
    window.addEventListener('resize', check_mobile);
    return () => window.removeEventListener('resize', check_mobile);
  }, []);

  React.useEffect(() => {
    if (isLoaded && !isSignedIn) {
      navigate("/sign-in");
    }
  }, [isLoaded, isSignedIn, navigate]);

  if (!isLoaded) {
    return <div className="min-h-screen digital-weave-bg bg-near-black flex items-center justify-center text-lime-400 text-xl">Initializing grimOS Interface...</div>;
  }
  
  const toggle_sidebar = () => set_is_sidebar_open(!is_sidebar_open);

  // Mock data for charts
  const security_events_data = generate_mock_chart_data(7, 5, 30);
  const workflow_performance_data = generate_mock_chart_data(12, 80, 100);
  const resource_allocation_data = [
    { name: 'CPU', value: 75, fill: 'hsl(var(--chart-1))' },
    { name: 'Memory', value: 60, fill: 'hsl(var(--chart-2))' },
    { name: 'Storage', value: 40, fill: 'hsl(var(--chart-3))' },
    { name: 'Network', value: 85, fill: 'hsl(var(--chart-4))' },
  ];


  return (
    <div className="min-h-screen digital-weave-bg bg-near-black flex">
      <GrimOsSidebar isOpen={is_sidebar_open} toggleSidebar={toggle_sidebar} isMobile={is_mobile} />
      <div className={`flex-1 flex flex-col transition-all duration-300 ease-in-out ${!is_mobile && is_sidebar_open ? 'md:ml-72' : 'md:ml-0'}`}>
        <GrimOsHeader toggleSidebar={toggle_sidebar} />
        <ScrollArea className="flex-1">
          <main className="p-4 sm:p-6 space-y-6">
            {/* KPI Cards Row */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
              {kpi_data.map((kpi, index) => (
                <KpiCard key={kpi.title} {...kpi} delay={index * 0.05} />
              ))}
            </div>

            {/* Main Dashboard Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6">
              {/* Security Alerts Widget */}
              <DashboardWidget title="Recent Security Alerts" icon={<Shield className="h-5 w-5" />} delay={0.1} accentColor="border-red-500/40" className="lg:col-span-1">
                <ScrollArea className="h-64 pr-2">
                  <ul className="space-y-3">
                    {mock_security_alerts.map(alert => (
                      <li key={alert.id} className="flex items-start space-x-2 p-2 glass-darker rounded-md border border-white/5 hover:bg-white/5">
                        {alert.icon}
                        <div>
                          <p className="text-sm font-medium text-white/90">{alert.description}</p>
                          <p className="text-xs text-white/60">{alert.time} - {alert.severity}</p>
                        </div>
                      </li>
                    ))}
                  </ul>
                </ScrollArea>
              </DashboardWidget>

              {/* Active Workflows Widget */}
              <DashboardWidget title="Active Workflows" icon={<Zap className="h-5 w-5" />} delay={0.15} accentColor="border-blue-400/40" className="lg:col-span-1">
                 <ScrollArea className="h-64 pr-2">
                  <ul className="space-y-3">
                    {mock_active_workflows.map(wf => (
                      <li key={wf.id} className="p-2 glass-darker rounded-md border border-white/5 hover:bg-white/5">
                        <div className="flex justify-between items-center mb-1">
                          <span className={`text-sm font-medium ${wf.color}`}>{wf.name}</span>
                          <span className={`text-xs px-2 py-0.5 rounded-full bg-opacity-20 ${
                            wf.status === 'Active' ? 'bg-lime-500 text-lime-300' : 
                            wf.status === 'Pending' ? 'bg-blue-500 text-blue-300' : 'bg-red-500 text-red-300'
                          }`}>{wf.status}</span>
                        </div>
                        <div className="w-full bg-white/10 rounded-full h-1.5">
                          <div className={`h-1.5 rounded-full ${
                             wf.status === 'Active' ? 'bg-lime-500' : 
                             wf.status === 'Pending' ? 'bg-blue-500' : 'bg-red-500'
                          }`} style={{ width: `${wf.progress}%` }}></div>
                        </div>
                      </li>
                    ))}
                  </ul>
                </ScrollArea>
              </DashboardWidget>

              {/* Cognitive Insights Widget */}
              <DashboardWidget title="Cognitive Insights" icon={<Lightbulb className="h-5 w-5" />} delay={0.2} accentColor="border-purple-400/40" className="lg:col-span-1">
                 <ScrollArea className="h-64 pr-2">
                  <ul className="space-y-3">
                    {mock_cognitive_insights.map(insight => (
                      <li key={insight.id} className="p-2 glass-darker rounded-md border border-white/5 hover:bg-white/5">
                        <p className="text-sm text-white/90">{insight.text}</p>
                        <p className="text-xs text-purple-400/80 mt-1">{insight.source}</p>
                      </li>
                    ))}
                  </ul>
                </ScrollArea>
              </DashboardWidget>

              {/* Security Events Trend Chart */}
              <DashboardWidget title="Security Events Trend" icon={<BarChart3 className="h-5 w-5" />} delay={0.25} className="lg:col-span-2">
                <ChartContainer config={chart_config} className="h-[250px] w-full">
                  <BarChart accessibilityLayer data={security_events_data} margin={{ top: 5, right: 10, left: -20, bottom: 0 }}>
                    <CartesianGrid vertical={false} strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                    <XAxis dataKey="name" tickLine={false} axisLine={false} tickMargin={8} tickFormatter={(value) => value.slice(0, 3)} className="text-xs text-white/60 fill-current" />
                    <YAxis tickLine={false} axisLine={false} tickMargin={8} className="text-xs text-white/60 fill-current" />
                    <ChartTooltip content={<ChartTooltipContent hideIndicator className="glass-darker !border-lime-500/50" />} />
                    <Bar dataKey="value" fill="hsl(var(--chart-1))" radius={4} />
                  </BarChart>
                </ChartContainer>
              </DashboardWidget>
              
              {/* Resource Allocation Pie Chart */}
              <DashboardWidget title="Resource Allocation" icon={<Cpu className="h-5 w-5" />} delay={0.3} className="lg:col-span-1">
                 <ChartContainer config={chart_config} className="h-[250px] w-full">
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie data={resource_allocation_data} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} labelLine={false}
                             label={({ cx, cy, midAngle, innerRadius, outerRadius, percent }) => {
                                const RADIAN = Math.PI / 180;
                                const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
                                const x  = cx + radius * Math.cos(-midAngle * RADIAN);
                                const y = cy  + radius * Math.sin(-midAngle * RADIAN);
                                return (
                                  <text x={x} y={y} fill="white" textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central" className="text-xs">
                                    {`${(percent * 100).toFixed(0)}%`}
                                  </text>
                                );
                              }}
                        >
                          {resource_allocation_data.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.fill} className="focus:outline-none hover:opacity-80 transition-opacity" />
                          ))}
                        </Pie>
                        <RechartsTooltip contentStyle={{ backgroundColor: 'rgba(30,30,30,0.8)', borderColor: 'rgba(126,211,33,0.5)', borderRadius: '0.5rem' }} itemStyle={{ color: '#FFFFFF' }} />
                        <ChartLegend content={<ChartLegendContent className="text-xs text-white/70" />} />
                      </PieChart>
                    </ResponsiveContainer>
                  </ChartContainer>
              </DashboardWidget>

              {/* Quick Actions / Rune Pylon */}
              <DashboardWidget title="Rune Pylon" icon={<Briefcase className="h-5 w-5" />} delay={0.35} className="lg:col-span-1">
                 <div className="space-y-3">
                    <Button className="w-full glass-primary btn-hover-effect justify-start text-white">
                      <Zap className="mr-2 h-4 w-4 text-lime-400"/> Initiate Anomaly Scan
                    </Button>
                    <Button className="w-full glass-secondary btn-hover-effect-secondary justify-start text-white">
                      <DraftingCompass className="mr-2 h-4 w-4 text-blue-400"/> Design New Workflow
                    </Button>
                     <Button className="w-full glass-accent btn-hover-effect-accent justify-start text-white">
                      <MessageSquare className="mr-2 h-4 w-4 text-pink-400"/> Query ScrollWeaver
                    </Button>
                 </div>
              </DashboardWidget>

              {/* Team Activity / Audit Log Stub */}
               <DashboardWidget title="Team Activity Log" icon={<Users className="h-5 w-5" />} delay={0.4} className="lg:col-span-2">
                <ScrollArea className="h-[200px] pr-2">
                  <div className="text-sm text-white/70 space-y-2">
                    <p><span className="text-lime-400">Operator J.Doe</span> initiated <span className="text-blue-400">Workflow Alpha-7</span>. [2 min ago]</p>
                    <p><span className="text-lime-400">System</span> auto-patched vulnerability <span className="text-pink-400">CVE-2025-XXXX</span>. [10 min ago]</p>
                    <p><span className="text-lime-400">Analyst K.Smith</span> accessed <span className="text-blue-400">Threat Intel Dashboard</span>. [25 min ago]</p>
                     <p><span className="text-lime-400">Cognitive Core</span> updated <span className="text-purple-400">market forecast model</span>. [45 min ago]</p>
                  </div>
                </ScrollArea>
              </DashboardWidget>

            </div>
          </main>
        </ScrollArea>
      </div>
      {/* Styling for Clerk's popover to match glassmorphism */}
      <style jsx global>{`
        /* Card accent hover effect */
        .card[data-accent-color]:hover {
          border-color: var(--accent-hover-border) !important;
        }
        
        .cl-userButtonPopoverCard {
          background-color: rgba(30, 30, 30, 0.75) !important; /* Dark glass */
          backdrop-filter: blur(16px) !important;
          border: 1px solid rgba(255, 255, 255, 0.1) !important;
          border-radius: 0.75rem !important; /* Match shadcn/ui */
          box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2), inset 0 1px 1px rgba(255, 255, 255, 0.05) !important;
        }
        .cl-userButtonPopoverMain, .cl-userButtonPopoverActions {
          background-color: transparent !important;
        }
        .cl-userButtonPopoverActionButton, .cl-userButtonPopoverSamlAccountListItem {
          color: #FFFFFF !important;
        }
        .cl-userButtonPopoverActionButton:hover, .cl-userButtonPopoverSamlAccountListItem:hover {
          background-color: rgba(126, 211, 33, 0.2) !important; /* Lime accent hover */
        }
        .cl-userButtonPopoverActionButton__icon {
          color: #7ED321 !important; /* Lime accent for icons */
        }
        .cl-userButtonPopoverFooter {
          display: none !important; /* Optional: hide Clerk footer */
        }
        .glassmorphic-popover { /* For shadcn popovers if needed */
          background-color: rgba(30, 30, 30, 0.85) !important;
          backdrop-filter: blur(16px) !important;
          border: 1px solid rgba(255, 255, 255, 0.15) !important;
          color: white !important;
        }
        .glassmorphic-popover .cl-internal-b3fm6y { /* target specific clerk elements if too broad */
            color: white !important;
        }
      `}</style>
    </div>
  );
}

