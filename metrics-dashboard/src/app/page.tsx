"use client";

import * as React from "react";
import type { Issue } from "@/types/issue";
import { Table, TableBody, TableCaption, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { ImprovementChart } from "@/components/improvement-chart";
import { getIssues } from "@/lib/data";
import { AppSidebar, type DashboardView } from "@/components/app-sidebar";
import { SidebarInset, SidebarTrigger } from "@/components/ui/sidebar";
import { ModeToggle } from "@/components/theme-toggle";

/**
 * Issue Triage Dashboard - Main Page
 *
 * Displays a comprehensive dashboard for managing and prioritizing software issues.
 * Features a sidebar navigation interface with two main sections:
 * - Issues: Displays the triage catalog in a responsive data table with priority indicators and action items
 * - Improvement: Shows exponential growth metrics through interactive charts
 */

/**
 * Main dashboard component that renders the issue triage interface
 *
 * Fetches issues data and presents it in a sidebar layout with visualization options.
 * The Issues view renders a responsive table that highlights priority, descriptions,
 * and structured action items for each issue.
 *
 * @returns The main dashboard page with sidebar navigation for Issues and Improvement tracking
 */
export default function IssueDashboard() {
  const [activeView, setActiveView] = React.useState<DashboardView>("issues");
  const [issuesData, setIssuesData] = React.useState<Issue[]>([]);

  // Fetch issues data on component mount
  React.useEffect(() => {
    getIssues().then(setIssuesData);
  }, []);

  return (
    <>
      <AppSidebar activeView={activeView} onViewChange={setActiveView} />
      <SidebarInset>
        <div className="min-h-screen bg-background">
          {/* Header Section */}
          <header className="border-b border-border bg-card sticky top-0 z-40">
            <div className="flex items-center gap-4 px-6 py-4">
              <SidebarTrigger />
              <div className="flex-1">
                <h1 className="text-xl font-bold tracking-tight text-foreground">
                  {activeView === "issues" ? "Issue Triage" : "Improvement Metrics"}
                </h1>
              </div>
              <p className="text-sm text-muted-foreground hidden md:block">
                Manage and prioritize software issues efficiently
              </p>
              <ModeToggle />
            </div>
          </header>

          {/* Main Content */}
          <main className="px-4 sm:px-6 py-8 max-w-full">
            {activeView === "issues" && <IssueTable issues={issuesData} />}
            {activeView === "improvement" && (
              <div className="flex flex-col gap-6">
                <ImprovementChart />
              </div>
            )}
          </main>
        </div>
      </SidebarInset>
    </>
  );
}

/**
 * Permitted priority levels for issues displayed within the dashboard table.
 */
type IssuePriority = "high" | "medium" | "low";

/**
 * Look-up metadata describing how to render each issue priority in the table,
 * including accessible labels and styled badges.
 */
const ISSUE_PRIORITY_METADATA: Record<
  IssuePriority,
  {
    readonly label: string;
    readonly badgeClassName: string;
  }
> = {
  high: { label: "High", badgeClassName: "bg-red-500 text-white" },
  medium: { label: "Medium", badgeClassName: "bg-yellow-500 text-black" },
  low: { label: "Low", badgeClassName: "bg-green-500 text-white" }
};

/**
 * Strongly typed properties for the `IssueTable` component.
 */
type IssueTableProps = {
  /**
   * Complete list of issues to be surfaced within the triage table.
   */
  readonly issues: Issue[];
};

/**
 * Responsive table view for the issue triage catalog.
 *
 * Renders structured rows with priority badges, descriptions, and actionable items.
 * Designed to provide quick scanning for priority while remaining readable on smaller viewports.
 *
 * @param props - Component properties
 * @param props.issues - The issues that should populate the table body
 * @returns The issue table component
 */
function IssueTable({ issues }: IssueTableProps) {
  return (
    <div className="rounded-lg border border-border bg-card shadow-sm overflow-hidden">
      <div className="overflow-x-auto">
        <Table>
          <TableCaption>
            {`Tracking ${issues.length} ${issues.length === 1 ? "issue" : "issues"} across priority levels.`}
          </TableCaption>
          <TableHeader>
            <TableRow>
              <TableHead className="min-w-[150px]">Issue</TableHead>
              <TableHead className="min-w-[120px]">Priority</TableHead>
              <TableHead className="min-w-[200px]">Description</TableHead>
              <TableHead className="min-w-[200px]">Action Items</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {issues.map((issue) => (
              <IssueTableRow key={issue.id} issue={issue} />
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}

/**
 * Strongly typed properties for the `IssueTableRow` component.
 */
type IssueTableRowProps = {
  /**
   * Specific issue to render within a table row.
   */
  readonly issue: Issue;
};

/**
 * Table row implementation for a single issue.
 *
 * Breaks the issue into structured cells that highlight metadata and provide
 * a readable list of next steps.
 *
 * @param props - Component properties
 * @param props.issue - The issue data rendered in the table row
 * @returns The populated table row element
 */
function IssueTableRow({ issue }: IssueTableRowProps) {
  const priority = issue.priority as IssuePriority;
  const { label, badgeClassName } = ISSUE_PRIORITY_METADATA[priority];

  return (
    <TableRow>
      <TableCell className="align-top">
        <span className="text-card-foreground text-sm font-semibold break-words">{issue.title}</span>
      </TableCell>
      <TableCell className="align-top">
        <span
          className={`inline-flex items-center rounded-md px-2 py-1 text-xs font-medium whitespace-nowrap ${badgeClassName}`}
        >
          {label}
        </span>
      </TableCell>
      <TableCell className="align-top">
        <p className="text-card-foreground text-sm leading-relaxed break-words">{issue.description}</p>
      </TableCell>
      <TableCell className="align-top">
        <ol className="list-decimal list-inside space-y-2 text-sm leading-relaxed text-card-foreground break-words">
          {issue.actionsItems.map((action) => (
            <li key={action.id} className="break-words">
              {action.item}
            </li>
          ))}
        </ol>
      </TableCell>
    </TableRow>
  );
}
