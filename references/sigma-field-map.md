# Sigma to OCL field map

| Sigma field | OCL field | Type |
|---|---|---|
| EventID | Event ID | string |
| Image | Process Name | string |
| ParentImage | Parent Process Name | string |
| CommandLine | Command Line | string |
| User, AccountName | Principal Name | string |
| TargetUserName | Target User | string |
| SourceIp | Source IP | string |
| DestinationIp | Destination IP | string |
| SourcePort | Source Port | number |
| DestinationPort | Destination Port | number |
| LogonType | Logon Type | string |
| QueryName | Query Name | string |

Logsource mappings cover Windows Security, Windows Sysmon, Linux authentication, and OCI Audit logs. This map is a convention, not a tenant schema: verify field names against your own Log Source definitions before using a generated query.
