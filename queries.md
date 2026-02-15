🔍 Investigation Queries
This document catalogs the primary queries used by the Autonomous-Incident-Engine to correlate logs, metadata, and code changes.

1. Triage: Identify Top Error Patterns
Used by the Triage Agent to see the logs for which services are failing and what the specific error messages are.

Language: ES|QL

```SQL
FROM "logs-incident-*" | WHERE http.response.status_code >= 500 
  AND @timestamp > NOW() - 15m
| STATS count = COUNT(*), 
        distinct_errors = COUNT_DISTINCT(error.message) 
  BY service.name
| SORT count DESC
| LIMIT 10
```

2. Context: Fetch Service Metadata
Used by the Specialist Agent to identify the team owner,slack_channel and runbook url linked to a failing service.

Language: ES|QL

```SQL
FROM "service-metadata"
| WHERE service.name == ?service
| KEEP team.owner, team.slack_channel, runbook_url
```

3. Correlation: Identify Recent Code Changes
Used by the Specialist Agent to find Pull Requests merged shortly before the incident began.

Language: ES|QL

```SQL
FROM "github-prs"
| WHERE service.name == ?service
| SORT merged_at DESC
| LIMIT 3
| KEEP pr.title, pr.change_summary, pr.author, pr.html_url, merged_at
```

#💡 How the AI uses these queries

The Autonomous-Incident-Engine uses a "Chain of Thought" process:

Query 1 detects the failing service and error signature.

Query 2 finds the failing service is managed by which team and where to share final report in slack.

Query 3 scans the github-prs index and finds PR which might have caused failing of service.
