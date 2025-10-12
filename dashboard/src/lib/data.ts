import type { Issue } from "@/types/issue";

/**
 * Fetches the list of issues for the dashboard.
 *
 * Currently returns hardcoded mock data for development purposes.
 * This function will be updated in the future to fetch data from an external API endpoint.
 *
 * @returns A promise that resolves to an array of Issue objects
 *
 * @example
 * ```typescript
 * const issues = await getIssues();
 * console.log(issues); // Array of Issue objects
 * ```
 */
export async function getIssues(): Promise<Issue[]> {
  // TODO: Replace with actual API call in the future
  // Example: const response = await fetch('https://api.example.com/issues');
  // return response.json();

  return [
    {
      id: "ISS-001",
      title: "Authentication System Bug",
      description:
        "Users are experiencing intermittent login failures when attempting to authenticate through the OAuth provider. The issue appears to be related to session token expiration handling and affects approximately 15% of login attempts during peak hours.",
      priority: "high",
      actionsItems: [
        {
          id: "ACT-001",
          item: "Review error logs and stack traces"
        },
        {
          id: "ACT-002",
          item: "Reproduce issue in staging environment"
        },
        {
          id: "ACT-003",
          item: "Identify root cause and document findings"
        },
        {
          id: "ACT-004",
          item: "Implement fix and write unit tests"
        },
        {
          id: "ACT-005",
          item: "Deploy to production and monitor"
        }
      ]
    },
    {
      id: "ISS-002",
      title: "Database Query Performance Degradation",
      description:
        "The user dashboard is loading significantly slower than expected, with query times exceeding 3 seconds. Analysis indicates that the issue stems from missing indexes on frequently queried columns in the users and transactions tables.",
      priority: "medium",
      actionsItems: [
        {
          id: "ACT-006",
          item: "Run EXPLAIN ANALYZE on slow queries"
        },
        {
          id: "ACT-007",
          item: "Add appropriate indexes to database tables"
        },
        {
          id: "ACT-008",
          item: "Test query performance improvements"
        },
        {
          id: "ACT-009",
          item: "Update ORM queries to leverage new indexes"
        }
      ]
    },
    {
      id: "ISS-003",
      title: "Implement Dark Mode Support",
      description:
        "Multiple users have requested a dark mode option for the application. This feature would improve accessibility and reduce eye strain for users working in low-light environments. Implementation should include theme persistence and smooth transitions.",
      priority: "low",
      actionsItems: [
        {
          id: "ACT-010",
          item: "Design dark mode color palette and tokens"
        },
        {
          id: "ACT-011",
          item: "Implement theme switching mechanism"
        },
        {
          id: "ACT-012",
          item: "Update all components to support dark mode"
        },
        {
          id: "ACT-013",
          item: "Add theme persistence to local storage"
        },
        {
          id: "ACT-014",
          item: "Test accessibility and contrast ratios"
        }
      ]
    },
    {
      id: "ISS-004",
      title: "API Rate Limiting Not Enforced",
      description:
        "Critical security vulnerability discovered: API endpoints are not properly enforcing rate limits, allowing potential abuse and DDoS attacks. This poses a significant risk to system stability and could result in service outages.",
      priority: "high",
      actionsItems: [
        {
          id: "ACT-015",
          item: "Implement rate limiting middleware"
        },
        {
          id: "ACT-016",
          item: "Configure appropriate rate limits per endpoint"
        },
        {
          id: "ACT-017",
          item: "Add rate limit headers to API responses"
        },
        {
          id: "ACT-018",
          item: "Set up monitoring and alerting for rate limit violations"
        }
      ]
    },
    {
      id: "ISS-005",
      title: "User Profile Page Redesign",
      description:
        "The current user profile page has outdated styling and poor information hierarchy. Users report difficulty finding key account settings. A redesign would improve user experience and align with our updated design system.",
      priority: "medium",
      actionsItems: [
        {
          id: "ACT-019",
          item: "Conduct user research and gather feedback"
        },
        {
          id: "ACT-020",
          item: "Create wireframes and mockups"
        },
        {
          id: "ACT-021",
          item: "Implement new profile page layout"
        },
        {
          id: "ACT-022",
          item: "Conduct usability testing"
        }
      ]
    }
  ];
}
