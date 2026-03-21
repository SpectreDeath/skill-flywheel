#!/usr/bin/env python3
"""
Skill: k8s-validator
Domain: devops
Description: Validates Kubernetes manifests for best practices, security, and configuration issues
"""

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List

import yaml


class IssueSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class StrictnessLevel(Enum):
    BASIC = "basic"
    STANDARD = "standard"
    STRICT = "strict"


@dataclass
class K8sIssue:
    severity: IssueSeverity
    category: str
    resource_kind: str
    resource_name: str
    description: str
    field_path: str
    suggestion: str


@dataclass
class BestPracticeCheck:
    name: str
    description: str
    passed: bool
    details: str


@dataclass
class K8sValidator:
    manifest: str
    options: Dict[str, Any]
    resources: List[Dict[str, Any]] = field(default_factory=list)
    issues: List[K8sIssue] = field(default_factory=list)
    best_practices: List[BestPracticeCheck] = field(default_factory=list)

    def __post_init__(self):
        self.strictness = StrictnessLevel(self.options.get("strictness", "standard"))

    def parse_manifest(self) -> bool:
        try:
            docs = list(yaml.safe_load_all(self.manifest))
            self.resources = [doc for doc in docs if doc is not None]
            return True
        except Exception as e:
            self.issues.append(
                K8sIssue(
                    severity=IssueSeverity.CRITICAL,
                    category="parsing",
                    resource_kind="",
                    resource_name="",
                    description=f"Failed to parse YAML: {str(e)}",
                    field_path="",
                    suggestion="Ensure the YAML is valid and properly formatted",
                )
            )
            return False

    def validate_resources(self):
        for resource in self.resources:
            kind = resource.get("kind", "")
            resource.get("metadata", {}).get("name", "unnamed")

            if kind == "Deployment":
                self._validate_deployment(resource)
            elif kind == "Service":
                self._validate_service(resource)
            elif kind == "ConfigMap":
                self._validate_configmap(resource)
            elif kind == "Secret":
                self._validate_secret(resource)
            elif kind == "Pod":
                self._validate_pod(resource)
            elif kind == "Ingress":
                self._validate_ingress(resource)
            elif kind == "PersistentVolumeClaim":
                self._validate_pvc(resource)
            elif kind == "ServiceAccount":
                self._validate_serviceaccount(resource)
            elif kind in {"Role", "ClusterRole"}:
                self._validate_rbac(resource)
            elif kind == "NetworkPolicy":
                self._validate_networkpolicy(resource)
            else:
                self._validate_generic_resource(resource)

    def _validate_deployment(self, resource: Dict[str, Any]):
        name = resource.get("metadata", {}).get("name", "unnamed")
        spec = resource.get("spec", {})
        replicas = spec.get("replicas")

        if replicas is None:
            self.issues.append(
                K8sIssue(
                    severity=IssueSeverity.MEDIUM,
                    category="configuration",
                    resource_kind="Deployment",
                    resource_name=name,
                    description="No replica count specified",
                    field_path="spec.replicas",
                    suggestion="Set replicas for high availability (recommended: 2+)",
                )
            )

        self._check_pod_spec(
            spec.get("template", {}).get("spec", {}), "Deployment", name
        )
        self._validate_deployment_strategy(spec, name)

    def _validate_pod_spec(self, pod_spec: Dict[str, Any], kind: str, name: str):
        if not pod_spec:
            self.issues.append(
                K8sIssue(
                    severity=IssueSeverity.CRITICAL,
                    category="specification",
                    resource_kind=kind,
                    resource_name=name,
                    description="Pod spec is empty",
                    field_path="spec.template.spec",
                    suggestion="Provide a valid pod spec",
                )
            )
            return

        containers = pod_spec.get("containers", [])
        if not containers:
            self.issues.append(
                K8sIssue(
                    severity=IssueSeverity.CRITICAL,
                    category="specification",
                    resource_kind=kind,
                    resource_name=name,
                    description="No containers defined",
                    field_path="spec.template.spec.containers",
                    suggestion="Add at least one container",
                )
            )
            return

        for container in containers:
            self._validate_container(container, kind, name)

    def _validate_container(self, container: Dict[str, Any], kind: str, name: str):
        container_name = container.get("name", "unnamed")

        if not container.get("image"):
            self.issues.append(
                K8sIssue(
                    severity=IssueSeverity.CRITICAL,
                    category="specification",
                    resource_kind=kind,
                    resource_name=name,
                    description="Container has no image specified",
                    field_path=f"containers[{container_name}].image",
                    suggestion="Specify a container image",
                )
            )

        image = container.get("image", "")
        if image and "latest" in image and self.strictness != StrictnessLevel.BASIC:
            self.issues.append(
                K8sIssue(
                    severity=IssueSeverity.MEDIUM,
                    category="best_practice",
                    resource_kind=kind,
                    resource_name=name,
                    description="Using 'latest' tag is not recommended",
                    field_path=f"containers[{container_name}].image",
                    suggestion="Use specific version tags instead of 'latest'",
                )
            )

        resources = container.get("resources", {})
        if not resources:
            self.issues.append(
                K8sIssue(
                    severity=IssueSeverity.HIGH,
                    category="best_practice",
                    resource_kind=kind,
                    resource_name=name,
                    description="No resource limits defined",
                    field_path=f"containers[{container_name}].resources",
                    suggestion="Define resource limits (requests and limits) for CPU and memory",
                )
            )
        else:
            self._validate_resource_limits(resources, container_name, kind, name)

        security_context = container.get("securityContext", {})
        self._validate_security_context(security_context, container_name, kind, name)

        if not container.get("ports"):
            if self.strictness == StrictnessLevel.STRICT:
                self.issues.append(
                    K8sIssue(
                        severity=IssueSeverity.LOW,
                        category="best_practice",
                        resource_kind=kind,
                        resource_name=name,
                        description="No ports exposed",
                        field_path=f"containers[{container_name}].ports",
                        suggestion="Explicitly define container ports for documentation",
                    )
                )

        liveness_probe = container.get("livenessProbe")
        readiness_probe = container.get("readinessProbe")

        if not liveness_probe and self.strictness != StrictnessLevel.BASIC:
            self.issues.append(
                K8sIssue(
                    severity=IssueSeverity.MEDIUM,
                    category="best_practice",
                    resource_kind=kind,
                    resource_name=name,
                    description="No liveness probe defined",
                    field_path=f"containers[{container_name}].livenessProbe",
                    suggestion="Add a liveness probe to detect hung processes",
                )
            )

        if not readiness_probe and self.strictness != StrictnessLevel.BASIC:
            self.issues.append(
                K8sIssue(
                    severity=IssueSeverity.MEDIUM,
                    category="best_practice",
                    resource_kind=kind,
                    resource_name=name,
                    description="No readiness probe defined",
                    field_path=f"containers[{container_name}].readinessProbe",
                    suggestion="Add a readiness probe to determine when container is ready",
                )
            )

    def _validate_resource_limits(
        self, resources: Dict[str, Any], container_name: str, kind: str, name: str
    ):
        requests = resources.get("requests", {})
        limits = resources.get("limits", {})

        if not requests:
            self.issues.append(
                K8sIssue(
                    severity=IssueSeverity.MEDIUM,
                    category="best_practice",
                    resource_kind=kind,
                    resource_name=name,
                    description="No resource requests defined",
                    field_path=f"containers[{container_name}].resources.requests",
                    suggestion="Define resource requests for scheduling",
                )
            )

        if not limits:
            self.issues.append(
                K8sIssue(
                    severity=IssueSeverity.MEDIUM,
                    category="best_practice",
                    resource_kind=kind,
                    resource_name=name,
                    description="No resource limits defined",
                    field_path=f"containers[{container_name}].resources.limits",
                    suggestion="Define resource limits to prevent resource exhaustion",
                )
            )

        if limits:
            memory = limits.get("memory", "")
            limits.get("cpu", "")

            if memory and not self._is_valid_memory(memory):
                self.issues.append(
                    K8sIssue(
                        severity=IssueSeverity.HIGH,
                        category="validation",
                        resource_kind=kind,
                        resource_name=name,
                        description=f"Invalid memory limit format: {memory}",
                        field_path=f"containers[{container_name}].resources.limits.memory",
                        suggestion="Use format like '512Mi', '1Gi', '2G'",
                    )
                )

    def _is_valid_memory(self, value: str) -> bool:
        pattern = r"^\d+(Ki|Mi|Gi|Ti|Pi|Ei|K|M|G|T|P|E)?$"
        return bool(re.match(pattern, value, re.IGNORECASE))

    def _validate_security_context(
        self,
        security_context: Dict[str, Any],
        container_name: str,
        kind: str,
        name: str,
    ):
        if not security_context:
            self.issues.append(
                K8sIssue(
                    severity=IssueSeverity.HIGH,
                    category="security",
                    resource_kind=kind,
                    resource_name=name,
                    description="No security context defined",
                    field_path=f"containers[{container_name}].securityContext",
                    suggestion="Define a security context with appropriate runAsNonRoot, runAsUser, and capabilities",
                )
            )
            return

        if not security_context.get("runAsNonRoot"):
            self.issues.append(
                K8sIssue(
                    severity=IssueSeverity.HIGH,
                    category="security",
                    resource_kind=kind,
                    resource_name=name,
                    description="Container may run as root",
                    field_path=f"containers[{container_name}].securityContext.runAsNonRoot",
                    suggestion="Set runAsNonRoot: true to run as non-root user",
                )
            )

        if not security_context.get("readOnlyRootFilesystem"):
            if self.strictness != StrictnessLevel.BASIC:
                self.issues.append(
                    K8sIssue(
                        severity=IssueSeverity.MEDIUM,
                        category="security",
                        resource_kind=kind,
                        resource_name=name,
                        description="Root filesystem is writable",
                        field_path=f"containers[{container_name}].securityContext.readOnlyRootFilesystem",
                        suggestion="Set readOnlyRootFilesystem: true for read-only root filesystem",
                    )
                )

        capabilities = security_context.get("capabilities", {})
        add_caps = capabilities.get("add", [])
        if "SYS_ADMIN" in add_caps or "ALL" in add_caps:
            self.issues.append(
                K8sIssue(
                    severity=IssueSeverity.CRITICAL,
                    category="security",
                    resource_kind=kind,
                    resource_name=name,
                    description="Dangerous capability added",
                    field_path=f"containers[{container_name}].securityContext.capabilities.add",
                    suggestion="Avoid adding dangerous capabilities like SYS_ADMIN",
                )
            )

    def _validate_deployment_strategy(self, spec: Dict[str, Any], name: str):
        strategy = spec.get("strategy", {})

        if not strategy and self.strictness != StrictnessLevel.BASIC:
            self.issues.append(
                K8sIssue(
                    severity=IssueSeverity.LOW,
                    category="best_practice",
                    resource_kind="Deployment",
                    resource_name=name,
                    description="No deployment strategy defined",
                    field_path="spec.strategy",
                    suggestion="Define a rollingUpdate or Recreate strategy",
                )
            )

        strategy_type = strategy.get("type", "RollingUpdate")
        if strategy_type == "RollingUpdate":
            rolling = strategy.get("rollingUpdate", {})
            rolling.get("maxSurge", "25%")
            max_unavailable = rolling.get("maxUnavailable", "25%")

            if max_unavailable == "25%" and self.strictness == StrictnessLevel.STRICT:
                self.issues.append(
                    K8sIssue(
                        severity=IssueSeverity.LOW,
                        category="best_practice",
                        resource_kind="Deployment",
                        resource_name=name,
                        description="Default rolling update parameters may cause downtime",
                        field_path="spec.strategy.rollingUpdate",
                        suggestion="Consider tuning maxSurge and maxUnavailable for zero-downtime deployments",
                    )
                )

    def _validate_service(self, resource: Dict[str, Any]):
        name = resource.get("metadata", {}).get("name", "unnamed")
        spec = resource.get("spec", {})

        service_type = spec.get("type", "ClusterIP")

        if service_type == "LoadBalancer" and not spec.get("selector"):
            self.issues.append(
                K8sIssue(
                    severity=IssueSeverity.CRITICAL,
                    category="configuration",
                    resource_kind="Service",
                    resource_name=name,
                    description="LoadBalancer service has no selector",
                    field_path="spec.selector",
                    suggestion="Add a selector to target pods",
                )
            )

        if not spec.get("selector") and service_type != "ExternalName":
            self.issues.append(
                K8sIssue(
                    severity=IssueSeverity.HIGH,
                    category="configuration",
                    resource_kind="Service",
                    resource_name=name,
                    description="Service has no selector",
                    field_path="spec.selector",
                    suggestion="Add a selector to target pods or define targetPort",
                )
            )

        ports = spec.get("ports", [])
        if not ports:
            self.issues.append(
                K8sIssue(
                    severity=IssueSeverity.CRITICAL,
                    category="configuration",
                    resource_kind="Service",
                    resource_name=name,
                    description="Service has no ports defined",
                    field_path="spec.ports",
                    suggestion="Define at least one service port",
                )
            )

        for port in ports:
            if not port.get("targetPort"):
                self.issues.append(
                    K8sIssue(
                        severity=IssueSeverity.MEDIUM,
                        category="configuration",
                        resource_kind="Service",
                        resource_name=name,
                        description="Service port has no targetPort",
                        field_path=f"spec.ports[{port.get('name', 'unnamed')}].targetPort",
                        suggestion="Set targetPort to match container port",
                    )
                )

    def _validate_configmap(self, resource: Dict[str, Any]):
        name = resource.get("metadata", {}).get("name", "unnamed")

        if not resource.get("data") and not resource.get("binaryData"):
            self.issues.append(
                K8sIssue(
                    severity=IssueSeverity.MEDIUM,
                    category="configuration",
                    resource_kind="ConfigMap",
                    resource_name=name,
                    description="ConfigMap has no data",
                    field_path="data",
                    suggestion="Add data or binaryData to the ConfigMap",
                )
            )

    def _validate_secret(self, resource: Dict[str, Any]):
        name = resource.get("metadata", {}).get("name", "unnamed")
        secret_type = resource.get("type", "Opaque")

        if secret_type == "Opaque":
            if not resource.get("data") and not resource.get("stringData"):
                self.issues.append(
                    K8sIssue(
                        severity=IssueSeverity.HIGH,
                        category="configuration",
                        resource_kind="Secret",
                        resource_name=name,
                        description="Secret has no data",
                        field_path="data",
                        suggestion="Add data or stringData to the Secret",
                    )
                )

    def _validate_pod(self, resource: Dict[str, Any]):
        name = resource.get("metadata", {}).get("name", "unnamed")
        spec = resource.get("spec", {})

        self._check_pod_spec(spec, "Pod", name)

    def _validate_ingress(self, resource: Dict[str, Any]):
        name = resource.get("metadata", {}).get("name", "unnamed")
        spec = resource.get("spec", {})

        if not spec.get("rules"):
            self.issues.append(
                K8sIssue(
                    severity=IssueSeverity.CRITICAL,
                    category="configuration",
                    resource_kind="Ingress",
                    resource_name=name,
                    description="Ingress has no rules defined",
                    field_path="spec.rules",
                    suggestion="Define at least one rule with host and paths",
                )
            )

        tls = spec.get("tls", [])
        for tls_config in tls:
            if not tls_config.get("hosts"):
                self.issues.append(
                    K8sIssue(
                        severity=IssueSeverity.MEDIUM,
                        category="security",
                        resource_kind="Ingress",
                        resource_name=name,
                        description="TLS config has no hosts specified",
                        field_path="spec.tls.hosts",
                        suggestion="Specify hosts for TLS configuration",
                    )
                )

        annotations = resource.get("metadata", {}).get("annotations", {})
        if not annotations.get("kubernetes.io/ingress.class") and not annotations.get(
            "nginx.ingress.kubernetes.io/rewrite-target"
        ):
            if self.strictness != StrictnessLevel.BASIC:
                self.issues.append(
                    K8sIssue(
                        severity=IssueSeverity.LOW,
                        category="best_practice",
                        resource_kind="Ingress",
                        resource_name=name,
                        description="No ingress class annotation",
                        field_path="metadata.annotations",
                        suggestion="Consider adding ingress class annotation for clarity",
                    )
                )

    def _validate_pvc(self, resource: Dict[str, Any]):
        name = resource.get("metadata", {}).get("name", "unnamed")
        spec = resource.get("spec", {})

        if not spec.get("accessModes"):
            self.issues.append(
                K8sIssue(
                    severity=IssueSeverity.HIGH,
                    category="configuration",
                    resource_kind="PersistentVolumeClaim",
                    resource_name=name,
                    description="No access modes defined",
                    field_path="spec.accessModes",
                    suggestion="Define access modes (ReadWriteOnce, ReadOnlyMany, ReadWriteMany)",
                )
            )

        if not spec.get("resources"):
            self.issues.append(
                K8sIssue(
                    severity=IssueSeverity.HIGH,
                    category="configuration",
                    resource_kind="PersistentVolumeClaim",
                    resource_name=name,
                    description="No resources (storage) requested",
                    field_path="spec.resources",
                    suggestion="Define storage request size",
                )
            )

    def _validate_serviceaccount(self, resource: Dict[str, Any]):
        name = resource.get("metadata", {}).get("name", "unnamed")

        if not resource.get("imagePullSecrets"):
            self.issues.append(
                K8sIssue(
                    severity=IssueSeverity.LOW,
                    category="best_practice",
                    resource_kind="ServiceAccount",
                    resource_name=name,
                    description="No imagePullSecrets defined",
                    field_path="imagePullSecrets",
                    suggestion="Add imagePullSecrets if using private container registry",
                )
            )

    def _validate_rbac(self, resource: Dict[str, Any]):
        name = resource.get("metadata", {}).get("name", "unnamed")
        kind = resource.get("kind", "Role")
        rules = resource.get("rules", [])

        if not rules:
            self.issues.append(
                K8sIssue(
                    severity=IssueSeverity.HIGH,
                    category="configuration",
                    resource_kind=kind,
                    resource_name=name,
                    description="No rules defined",
                    field_path="rules",
                    suggestion="Define at least one rule with apiGroups, resources, and verbs",
                )
            )

        for idx, rule in enumerate(rules):
            if (
                not rule.get("apiGroups")
                and not rule.get("resources")
                and not rule.get("nonResourceURLs")
            ):
                self.issues.append(
                    K8sIssue(
                        severity=IssueSeverity.HIGH,
                        category="configuration",
                        resource_kind=kind,
                        resource_name=name,
                        description=f"Rule {idx} has no valid resources",
                        field_path=f"rules[{idx}]",
                        suggestion="Define apiGroups, resources, or nonResourceURLs",
                    )
                )

    def _validate_networkpolicy(self, resource: Dict[str, Any]):
        name = resource.get("metadata", {}).get("name", "unnamed")
        spec = resource.get("spec", {})

        if not spec.get("podSelector"):
            self.issues.append(
                K8sIssue(
                    severity=IssueSeverity.MEDIUM,
                    category="configuration",
                    resource_kind="NetworkPolicy",
                    resource_name=name,
                    description="No pod selector defined",
                    field_path="spec.podSelector",
                    suggestion="Define podSelector to target specific pods",
                )
            )

        if not spec.get("policyTypes"):
            self.issues.append(
                K8sIssue(
                    severity=IssueSeverity.MEDIUM,
                    category="configuration",
                    resource_kind="NetworkPolicy",
                    resource_name=name,
                    description="No policy types defined",
                    field_path="spec.policyTypes",
                    suggestion="Define policy types (Ingress, Egress)",
                )
            )

    def _validate_generic_resource(self, resource: Dict[str, Any]):
        name = resource.get("metadata", {}).get("name", "unnamed")
        kind = resource.get("kind", "Unknown")

        if not resource.get("metadata"):
            self.issues.append(
                K8sIssue(
                    severity=IssueSeverity.CRITICAL,
                    category="specification",
                    resource_kind=kind,
                    resource_name=name,
                    description="Resource has no metadata",
                    field_path="metadata",
                    suggestion="Define metadata with name",
                )
            )

    def check_best_practices(self):
        self.best_practices = []

        has_deployment_with_hpa = False
        has_pdb = False
        has_resource_limits = True
        has_security_context = True

        for resource in self.resources:
            kind = resource.get("kind", "")
            resource.get("metadata", {}).get("name", "unnamed")

            if kind == "Deployment":
                spec = resource.get("spec", {})
                replicas = spec.get("replicas", 0)

                if replicas > 1:
                    has_pdb = True

                template_spec = spec.get("template", {}).get("spec", {})
                for container in template_spec.get("containers", []):
                    if not container.get("resources", {}).get("limits"):
                        has_resource_limits = False
                    if not container.get("securityContext"):
                        has_security_context = False

            if kind == "HorizontalPodAutoscaler":
                has_deployment_with_hpa = True

        self.best_practices.append(
            BestPracticeCheck(
                name="Resource Limits",
                description="All containers should have resource limits defined",
                passed=has_resource_limits,
                details="Resource limits prevent container from consuming excessive resources",
            )
        )

        self.best_practices.append(
            BestPracticeCheck(
                name="Security Context",
                description="Containers should have security context configured",
                passed=has_security_context,
                details="Security context provides pod/container security settings",
            )
        )

        self.best_practices.append(
            BestPracticeCheck(
                name="High Availability",
                description="Deployments should have multiple replicas or HPA",
                passed=has_deployment_with_hpa or has_pdb,
                details="Multiple replicas ensure high availability and zero-downtime updates",
            )
        )

        self.best_practices.append(
            BestPracticeCheck(
                name="Pod Disruption Budget",
                description="Should have PodDisruptionBudget for HA deployments",
                passed=has_pdb,
                details="PDB ensures minimum number of pods available during disruptions",
            )
        )

        self.best_practices.append(
            BestPracticeCheck(
                name="Liveness & Readiness Probes",
                description="Containers should have health check probes",
                passed=any(
                    container.get("livenessProbe") or container.get("readinessProbe")
                    for resource in self.resources
                    for container in resource.get("spec", {})
                    .get("template", {})
                    .get("spec", {})
                    .get("containers", [])
                ),
                details="Probes help Kubernetes manage container health and traffic routing",
            )
        )

    def generate_fixes(self) -> List[Dict[str, Any]]:
        fixes = []

        for issue in self.issues:
            fix = {
                "resource_kind": issue.resource_kind,
                "resource_name": issue.resource_name,
                "field_path": issue.field_path,
                "issue": issue.description,
                "suggestion": issue.suggestion,
            }

            if "No resource limits" in issue.description:
                fix["fix_example"] = {
                    "resources": {
                        "requests": {"cpu": "100m", "memory": "128Mi"},
                        "limits": {"cpu": "500m", "memory": "512Mi"},
                    }
                }

            elif "No security context" in issue.description:
                fix["fix_example"] = {
                    "securityContext": {
                        "runAsNonRoot": True,
                        "runAsUser": 1000,
                        "readOnlyRootFilesystem": True,
                        "allowPrivilegeEscalation": False,
                    }
                }

            elif "No liveness probe" in issue.description:
                fix["fix_example"] = {
                    "livenessProbe": {
                        "httpGet": {"path": "/healthz", "port": 8080},
                        "initialDelaySeconds": 30,
                        "periodSeconds": 10,
                    }
                }

            elif "No readiness probe" in issue.description:
                fix["fix_example"] = {
                    "readinessProbe": {
                        "httpGet": {"path": "/ready", "port": 8080},
                        "initialDelaySeconds": 5,
                        "periodSeconds": 5,
                    }
                }

            elif "runAsNonRoot" in issue.suggestion:
                fix["fix_example"] = {
                    "securityContext": {"runAsNonRoot": True, "runAsUser": 1000}
                }

            fixes.append(fix)

        return fixes

    def run(self) -> Dict[str, Any]:
        if not self.parse_manifest():
            return {
                "status": "error",
                "resources": [],
                "issues": [],
                "best_practices": [],
                "fixes": [],
            }

        self.validate_resources()
        self.check_best_practices()
        fixes = self.generate_fixes()

        critical_count = sum(
            1 for i in self.issues if i.severity == IssueSeverity.CRITICAL
        )
        high_count = sum(1 for i in self.issues if i.severity == IssueSeverity.HIGH)

        status = "success"
        if critical_count > 0 or high_count > 5:
            status = "error"
        elif self.issues:
            status = "warning"

        return {
            "status": status,
            "resources": [
                {
                    "kind": r.get("kind", "Unknown"),
                    "name": r.get("metadata", {}).get("name", "unnamed"),
                    "apiVersion": r.get("apiVersion", "v1"),
                }
                for r in self.resources
            ],
            "issues": [
                {
                    "severity": i.severity.value,
                    "category": i.category,
                    "resource_kind": i.resource_kind,
                    "resource_name": i.resource_name,
                    "description": i.description,
                    "field_path": i.field_path,
                    "suggestion": i.suggestion,
                }
                for i in self.issues
            ],
            "best_practices": [
                {
                    "name": bp.name,
                    "description": bp.description,
                    "passed": bp.passed,
                    "details": bp.details,
                }
                for bp in self.best_practices
            ],
            "fixes": fixes,
            "summary": {
                "total_resources": len(self.resources),
                "total_issues": len(self.issues),
                "critical": critical_count,
                "high": high_count,
                "medium": sum(
                    1 for i in self.issues if i.severity == IssueSeverity.MEDIUM
                ),
                "low": sum(1 for i in self.issues if i.severity == IssueSeverity.LOW),
                "passed_checks": sum(1 for bp in self.best_practices if bp.passed),
                "total_checks": len(self.best_practices),
            },
        }


def k8s_validator(manifest: str, options: dict = None) -> dict:
    """
    Validates Kubernetes manifests for best practices, security, and configuration issues.

    Args:
        manifest: K8s YAML manifest (can be multi-document)
        options: Dict with strictness level ("basic", "standard", "strict")

    Returns:
        Dict with status, resources, issues, best_practices, and fixes
    """
    if options is None:
        options = {}

    validator = K8sValidator(manifest=manifest, options=options)
    return validator.run()


def invoke(payload: dict) -> dict:
    """
    Skill invocation function for the Skill Flywheel system.

    Args:
        payload: Dict containing:
            - manifest: K8s YAML manifest string
            - options: Optional dict with strictness level

    Returns:
        Validation result dict
    """
    manifest = payload.get("manifest", "")
    options = payload.get("options", {})

    if not manifest:
        return {
            "status": "error",
            "error": "No manifest provided",
            "resources": [],
            "issues": [],
            "best_practices": [],
            "fixes": [],
        }

    return k8s_validator(manifest, options)


def register_skill() -> dict:
    """
    Returns skill metadata for the Skill Flywheel system.

    Returns:
        Dict with skill definition
    """
    return {
        "name": "k8s-validator",
        "domain": "devops",
        "description": "Validates Kubernetes manifests for best practices, security, and configuration issues",
        "version": "1.0.0",
        "functions": {
            "k8s_validator": {
                "description": "Main validation function",
                "parameters": {
                    "manifest": {
                        "type": "string",
                        "description": "K8s YAML manifest (can be multi-document YAML)",
                    },
                    "options": {
                        "type": "dict",
                        "description": "Validation options",
                        "properties": {
                            "strictness": {
                                "type": "string",
                                "enum": ["basic", "standard", "strict"],
                                "default": "standard",
                            }
                        },
                    },
                },
            },
            "invoke": {
                "description": "Skill invocation function for Skill Flywheel",
                "parameters": {
                    "payload": {
                        "type": "dict",
                        "description": "Payload containing manifest and options",
                    }
                },
            },
            "register_skill": {"description": "Returns skill metadata"},
        },
        "supported_kinds": [
            "Deployment",
            "Service",
            "ConfigMap",
            "Secret",
            "Pod",
            "Ingress",
            "PersistentVolumeClaim",
            "ServiceAccount",
            "Role",
            "ClusterRole",
            "NetworkPolicy",
            "HorizontalPodAutoscaler",
            "PodDisruptionBudget",
        ],
        "validation_checks": [
            "Resource limits and requests",
            "Security context",
            "Liveness and readiness probes",
            "Deployment strategy",
            "Service selectors",
            "Ingress rules",
            "RBAC rules",
            "Network policy configuration",
            "Best practices compliance",
        ],
    }


if __name__ == "__main__":
    sample_manifest = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: nginx:latest
        ports:
        - containerPort: 80
"""

    result = k8s_validator(sample_manifest, {"strictness": "standard"})
    print(f"Status: {result['status']}")
    print(f"Issues found: {len(result['issues'])}")
    print(
        f"Best practice checks: {result['summary']['passed_checks']}/{result['summary']['total_checks']}"
    )
