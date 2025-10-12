"use client";

import { TrendingUp } from "lucide-react";
import { CartesianGrid, Line, LineChart, XAxis } from "recharts";

import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { ChartConfig, ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart";

/**
 * Chart data representing exponential growth pattern
 * Values demonstrate accelerating improvement metrics over time
 * Formula used: f(x) = 5 * (1.5^x) to create clear exponential curve
 */
const chartData = [
  { month: "January", improvement: 8 },
  { month: "February", improvement: 12 },
  { month: "March", improvement: 18 },
  { month: "April", improvement: 28 },
  { month: "May", improvement: 42 },
  { month: "June", improvement: 64 },
  { month: "July", improvement: 95 },
  { month: "August", improvement: 143 }
];

/**
 * Chart configuration defining visual properties and labels
 */
const chartConfig = {
  improvement: {
    label: "Improvement Score",
    color: "var(--color-chart-1)"
  }
} satisfies ChartConfig;

/**
 * ImprovementChart Component
 *
 * Displays a line chart showing exponential growth in improvement metrics.
 * This visualization demonstrates progress and acceleration in key performance
 * indicators over time.
 *
 * @returns A card containing an interactive line chart with exponential growth data
 */
export function ImprovementChart() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Issue Resolution Improvement</CardTitle>
        <CardDescription>January - August 2025</CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig} className="h-[300px] w-full">
          <LineChart
            accessibilityLayer
            data={chartData}
            margin={{
              left: 12,
              right: 12
            }}
          >
            <CartesianGrid vertical={false} />
            <XAxis
              dataKey="month"
              tickLine={false}
              axisLine={false}
              tickMargin={8}
              tickFormatter={(value) => value.slice(0, 3)}
            />
            <ChartTooltip cursor={false} content={<ChartTooltipContent hideLabel />} />
            <Line
              dataKey="improvement"
              type="monotone"
              stroke="var(--color-improvement)"
              strokeWidth={3}
              isAnimationActive={false}
              dot={{
                fill: "var(--color-improvement)"
              }}
              activeDot={{
                r: 6
              }}
            />
          </LineChart>
        </ChartContainer>
      </CardContent>
      <CardFooter className="flex-col items-start gap-2 text-sm">
        <div className="flex items-center gap-2 font-medium leading-none">
          Trending up by 51% this month <TrendingUp className="h-4 w-4" />
        </div>
        <div className="leading-none text-muted-foreground">
          Showing exponential improvement in issue resolution efficiency
        </div>
      </CardFooter>
    </Card>
  );
}
