import { DashboardView, NavTab } from "./DashboardView";

export default function DashboardPage({
  searchParams,
}: {
  searchParams?: { tab?: string };
}) {
  const initial = (searchParams?.tab as NavTab) || "dashboard";
  return <DashboardView initialTab={initial} />;
}
