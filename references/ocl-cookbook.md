# OCL cookbook

Set the time window outside query text and scope searches to the compartment subtree. Adapt field names to the selected Log Source.

## Windows

```ocl
'Log Source' = 'Windows Security Events' and 'Event ID' = '4625'
```

```ocl
'Log Source' = 'Windows Security Events' and 'Event ID' in ('4624', '4625') | stats count as Count by 'Principal Name'
```

```ocl
'Log Source' = 'Windows Security Events' and 'Logon Type' = '10' | fields 'Principal Name', 'Source IP'
```

```ocl
'Log Source' = 'Windows Sysmon Operational Logs' and 'Process Name' like '*powershell*'
```

```ocl
'Log Source' = 'Windows Sysmon Operational Logs' and 'Parent Process Name' like '*service*' | head 50
```

## Linux

```ocl
'Log Source' = 'Linux Secure Logs' and 'Principal Name' = 'root'
```

```ocl
'Log Source' = 'Linux Secure Logs' and 'Original Log Content' like '*authentication failure*'
```

```ocl
'Log Source' = 'Linux Secure Logs' | stats count as Count by 'Principal Name' | sort -Count
```

```ocl
'Log Source' = 'Linux Secure Logs' and 'Source IP' = '192.0.2.10'
```

```ocl
'Log Source' = 'Linux Secure Logs' | timestats count as Count by 'Principal Name'
```

## OCI Audit

```ocl
'Log Source' = 'OCI Audit Logs' | stats count as Count by 'Principal Name'
```

```ocl
'Log Source' = 'OCI Audit Logs' and 'Response Code' = '401'
```

```ocl
'Log Source' = 'OCI Audit Logs' and 'Status Code' in ('400', '403')
```

```ocl
'Log Source' = 'OCI Audit Logs' | fields 'Principal Name', 'Source IP' | head 100
```

```ocl
'Log Source' = 'OCI Audit Logs' and 'Original Log Content' like '*Delete*'
```

## VCN flow logs

```ocl
'Log Source' = 'VCN Flow Logs' and 'Destination Port' = 443
```

```ocl
'Log Source' = 'VCN Flow Logs' and 'Source Port' = 53
```

```ocl
'Log Source' = 'VCN Flow Logs' | stats count as Count by 'Source IP'
```

```ocl
'Log Source' = 'VCN Flow Logs' and 'Destination IP' = '198.51.100.7'
```

```ocl
'Log Source' = 'VCN Flow Logs' | link 'Source IP', 'Destination IP'
```

## OKE

```ocl
'Log Source' = 'Kubernetes Container Logs' and 'Original Log Content' like '*error*'
```

```ocl
'Log Source' = 'Kubernetes Container Logs' | stats count as Count by 'Log Source'
```

```ocl
'Log Source' = 'Kubernetes Container Logs' | eval Category = 'application' | fields Category
```

```ocl
'Log Source' = 'Kubernetes Container Logs' | stats count as Count by 'Status Code' | where Count > 5
```

```ocl
'Log Source' in ('Kubernetes Container Logs', 'OCI Audit Logs') | stats count as Count by 'Log Source'
```
