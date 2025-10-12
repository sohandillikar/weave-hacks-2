"use client";

import * as React from "react";
import Image from "next/image";
import { LayoutDashboard, TrendingUp } from "lucide-react";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem
} from "@/components/ui/sidebar";

/**
 * Navigation items configuration for the application sidebar.
 *
 * Each item represents a distinct view in the dashboard, mapping to specific
 * content sections that can be displayed when selected.
 */
const navigationItems = [
  {
    id: "issues" as const,
    title: "Issues",
    icon: LayoutDashboard,
    description: "View and manage issue triage"
  },
  {
    id: "improvement" as const,
    title: "Improvement",
    icon: TrendingUp,
    description: "Track improvement metrics"
  }
] as const;

/**
 * Type representing valid view identifiers for the dashboard.
 */
export type DashboardView = (typeof navigationItems)[number]["id"];

/**
 * Properties for the AppSidebar component.
 */
type AppSidebarProps = {
  /**
   * Currently active view in the dashboard.
   */
  readonly activeView: DashboardView;

  /**
   * Callback function invoked when a navigation item is selected.
   *
   * @param view - The identifier of the newly selected view
   */
  readonly onViewChange: (view: DashboardView) => void;
};

/**
 * Application sidebar component providing primary navigation for the dashboard.
 *
 * Renders a collapsible sidebar with logo, navigation menu items, and footer information.
 * Supports visual indication of the currently active view and triggers view changes
 * through the provided callback.
 *
 * @param props - Component properties
 * @param props.activeView - The currently active dashboard view
 * @param props.onViewChange - Handler for view selection changes
 * @returns The application sidebar component
 */
export function AppSidebar({ activeView, onViewChange }: AppSidebarProps) {
  return (
    <Sidebar>
      <SidebarHeader>
        <div className="flex items-center gap-3 px-2 py-2">
          <Image src="/logo.png" alt="Logo" width={32} height={32} />
          <div className="flex flex-col">
            <h2 className="text-sm font-bold tracking-tight">Issue Triage</h2>
            <p className="text-xs text-muted-foreground">Dashboard</p>
          </div>
        </div>
      </SidebarHeader>

      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupContent>
            <SidebarMenu>
              {navigationItems.map((item) => (
                <SidebarMenuItem key={item.id}>
                  <SidebarMenuButton
                    isActive={activeView === item.id}
                    onClick={() => onViewChange(item.id)}
                    tooltip={item.description}
                  >
                    <item.icon />
                    <span>{item.title}</span>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter>
        <div className="px-3 py-2 text-xs text-muted-foreground">Manage and prioritize efficiently</div>
      </SidebarFooter>
    </Sidebar>
  );
}
