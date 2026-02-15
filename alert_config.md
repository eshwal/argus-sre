# 🚨 Alert Configuration

This project uses an Elastic **Custom Threshold Rule** to trigger the autonomous investigation workflow.

## ⚙️ Rule Settings
* **Data View:** `Incident logs` (Targeting `logs-incident-*`)
* **Filter:** `http.response.status_code >= 500`
* **Aggregation:** Count
* **Condition:** Above `5` occurrences
* **Lookback Period:** `15 minutes`
* **Run Schedule:** Every `1 minute`
* **Group By:** `service.name`  
    > **⚠️ Critical:** Must Group By `service.name`. This ensures the alert context passes the specific failing service to the workflow via `{{event.alerts[0].service.name}}`.

---

## ⚡ Action: Trigger Workflow

1.  Add a new **Action** to the rule.
2.  Select **Elastic Workflow** as the action type.
3.  Choose the workflow named: **`Autonomous-Incident-Engine`**.

### **How the Data Flows**
No custom JSON mapping is required. The workflow natively consumes the `event.alerts[0]` object to extract:
* **Service Context:** Used by the Triage Agent to filter logs.
* **Alert Reason:** Provides the initial "symptoms" to the AI.
* **Timestamp:** Used by the Specialist Agent to correlate GitHub PRs.
