import { ActionItem } from "./action-item";

export type Priority = "low" | "medium" | "high";

export type Issue = {
  id: string;
  title: string;
  description: string;
  priority: string;
  actionsItems: ActionItem[];
};
