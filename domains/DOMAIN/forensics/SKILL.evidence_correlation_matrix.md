---
Domain: FORENSICS
Version: 1.0.0
Type: Algorithm
Category: Evidence Analysis
Complexity: Advanced
Estimated Execution Time: 3-8 minutes
name: evidence_correlation_matrix
---

# SKILL: Evidence Correlation Matrix

## Purpose

Analyze and correlate evidence across multiple forensic investigations using advanced correlation algorithms and Ralph Wiggum-style chaotic pattern recognition. This skill identifies hidden connections, establishes evidence relationships, and builds comprehensive correlation matrices for complex investigations.

## When to Use

- Investigating complex cases with multiple evidence sources
- Correlating evidence across different forensic investigations
- Identifying hidden patterns and connections in evidence data
- Building comprehensive evidence relationship matrices
- Analyzing Ralph Wiggum-style chaotic evidence patterns

## When NOT to Use

- For simple cases with obvious evidence connections
- When evidence is limited to a single source or type
- For straightforward investigations with clear evidence trails
- When immediate action is needed over comprehensive analysis

## Inputs

- **Required**: Multiple evidence sources and artifacts
- **Required**: Evidence metadata and provenance information
- **Required**: Investigation context and case details
- **Optional**: Historical correlation patterns and relationship data
- **Optional**: Cross-investigation evidence links and references
- **Assumptions**: Evidence sources are reliable, metadata is accurate, correlations can be established

## Outputs

- **Primary**: Comprehensive evidence correlation matrix with relationship analysis
- **Secondary**: Hidden pattern identification and connection discovery
- **Tertiary**: Evidence strength assessment and reliability scoring
- **Format**: JSON structure with correlation matrices, pattern analysis, and evidence relationships

## Capabilities

1. **Multi-Source Correlation**: Correlate evidence across different sources and investigations
2. **Pattern Recognition**: Identify hidden patterns and connections in evidence data
3. **Relationship Mapping**: Build comprehensive evidence relationship matrices
4. **Chaos Analysis**: Analyze Ralph Wiggum-style chaotic evidence patterns
5. **Evidence Scoring**: Assess evidence strength and reliability

## Usage Examples

### Example 1: Multi-Investigation Correlation

**Context**: Three separate security incidents with potential connections
**Input**: 
```
Evidence sources: 15 different systems and logs
Evidence types: Network logs, system artifacts, user activity
Investigation context: Potential coordinated attack
Correlation targets: Attack patterns, common vulnerabilities, timeline overlaps
```
**Output**: Comprehensive correlation matrix identifying coordinated attack patterns

### Example 2: Evidence Pattern Analysis

**Context**: Investigating recurring system failures with unknown cause
**Input**: Failure logs, system metrics, user reports, maintenance records
**Output**: Hidden pattern identification revealing root cause connections

## Input Format

- **Evidence Sources**: File paths, log entries, system artifacts, user reports
- **Evidence Metadata**: Timestamps, sources, reliability scores, chain of custody
- **Investigation Context**: Case details, investigation goals, relevant timelines
- **Correlation Parameters**: Relationship types, correlation thresholds, analysis depth

## Output Format

```json
{
  "correlation_matrix": {
    "matrix_id": "evidence_correlation_2026_03_03_001",
    "evidence_sources": 15,
    "correlation_pairs": 45,
    "matrix_structure": {
      "nodes": [
        {
          "evidence_id": "log_entry_001",
          "evidence_type": "network_log",
          "source": "firewall_001",
          "timestamp": "2026-03-03T10:00:00Z",
          "reliability_score": 0.95,
          "correlation_strength": 0.85
        },
        {
          "evidence_id": "artifact_002",
          "evidence_type": "system_artifact",
          "source": "server_002",
          "timestamp": "2026-03-03T10:15:00Z",
          "reliability_score": 0.88,
          "correlation_strength": 0.72
        }
      ],
      "edges": [
        {
          "source_evidence": "log_entry_001",
          "target_evidence": "artifact_002",
          "correlation_type": "temporal",
          "correlation_strength": 0.82,
          "confidence_level": 0.9,
          "relationship_description": "Sequential events within 15 minutes"
        },
        {
          "source_evidence": "log_entry_001",
          "target_evidence": "user_report_003",
          "correlation_type": "causal",
          "correlation_strength": 0.65,
          "confidence_level": 0.75,
          "relationship_description": "User report follows network anomaly"
        }
      ]
    }
  },
  "pattern_analysis": {
    "identified_patterns": [
      {
        "pattern_type": "coordinated_attack",
        "description": "Synchronized attacks across multiple systems",
        "evidence_count": 8,
        "confidence_level": 0.88,
        "pattern_strength": 0.82
      },
      {
        "pattern_type": "escalation_sequence",
        "description": "Progressive system compromise pattern",
        "evidence_count": 12,
        "confidence_level": 0.75,
        "pattern_strength": 0.68
      }
    ],
    "chaos_patterns": [
      {
        "pattern_type": "ralph_wiggum_effect",
        "description": "Unexpected evidence connections through chaotic interactions",
        "evidence_count": 5,
        "chaos_level": 0.9,
        "pattern_significance": "high"
      },
      {
        "pattern_type": "butterfly_correlation",
        "description": "Small evidence changes causing large correlation impacts",
        "evidence_count": 3,
        "chaos_level": 0.7,
        "pattern_significance": "medium"
      }
    ],
    "hidden_connections": [
      {
        "connection_type": "cross_investigation",
        "description": "Evidence link between separate investigations",
        "evidence_source": "log_entry_001",
        "evidence_target": "artifact_005",
        "connection_strength": 0.78,
        "significance": "critical"
      }
    ]
  },
  "evidence_assessment": {
    "evidence_quality": {
      "high_quality": 12,
      "medium_quality": 8,
      "low_quality": 3,
      "overall_reliability": 0.85
    },
    "correlation_strength": {
      "strong_correlations": 18,
      "medium_correlations": 22,
      "weak_correlations": 5,
      "average_strength": 0.72
    },
    "reliability_scoring": [
      {
        "evidence_id": "log_entry_001",
        "reliability_score": 0.95,
        "scoring_factors": ["timestamp_accuracy", "source_verification", "chain_of_custody"]
      },
      {
        "evidence_id": "artifact_002",
        "reliability_score": 0.88,
        "scoring_factors": ["integrity_verification", "source_reputation", "metadata_completeness"]
      }
    ]
  },
  "investigation_insights": {
    "key_findings": [
      "Coordinated attack pattern identified across 3 systems",
      "Evidence correlation suggests insider involvement",
      "Temporal analysis reveals attack sequence"
    ],
    "investigation_directions": [
      {
        "direction": "Focus on user_007 activity",
        "rationale": "Multiple evidence correlations point to this user",
        "priority": "high"
      },
      {
        "direction": "Analyze firewall_001 logs in detail",
        "rationale": "Central evidence source with multiple correlations",
        "priority": "medium"
      }
    ],
    "next_steps": [
      "Interview user_007 regarding suspicious activity",
      "Conduct detailed analysis of firewall logs",
      "Cross-reference with external threat intelligence"
    ]
  }
}
```

## Configuration Options

- `correlation_depth`: shallow, medium, deep (default: deep)
- `pattern_detection_sensitivity`: low, medium, high (default: high)
- `chaos_analysis_level`: basic, advanced, expert (default: advanced)
- `evidence_threshold`: strict, moderate, lenient (default: moderate)
- `chaos_injection_level`: none, light, heavy (default: heavy)

## Constraints

- **Hard Rules**: 
  - Never assume correlations without evidence support
  - Always maintain evidence chain of custody
  - Preserve evidence integrity during correlation analysis
- **Safety Requirements**: 
  - Use read-only access to original evidence
  - Document all correlation assumptions and methodologies
  - Maintain evidence provenance throughout analysis
- **Quality Standards**: 
  - Provide confidence levels for all correlations
  - Include evidence quality assessments
  - Generate actionable investigation insights

## Error Handling

- **Incomplete Evidence**: Use statistical inference and pattern matching
- **Conflicting Correlations**: Provide multiple correlation hypotheses with confidence levels
- **Missing Metadata**: Flag for manual investigation and data collection
- **Correlation Failures**: Document failure reasons and suggest alternative approaches

## Performance Optimization

- **Parallel Correlation**: Analyze multiple evidence sources concurrently
- **Incremental Processing**: Process large evidence datasets in chunks
- **Caching**: Cache correlation results for similar evidence patterns
- **Matrix Optimization**: Use optimized algorithms for large correlation matrices

## Integration Examples

### With Agent Ecosystem
```python
# Integrate evidence correlation into investigation workflows
correlation_matrix = EvidenceCorrelationMatrix()
correlation_report = correlation_matrix.analyze_evidence(
    evidence_sources=["log_entry_001", "artifact_002", "user_report_003"],
    correlation_depth="deep"
)
```

### With MCP Server
```python
@tool(name="evidence_correlation_matrix")
def correlate_evidence(evidence_sources: list, correlation_depth: str = "medium") -> dict:
    matrix = EvidenceCorrelationMatrix()
    return matrix.analyze_evidence(evidence_sources, correlation_depth)
```

## Best Practices

- **Comprehensive Evidence Collection**: Gather all relevant evidence sources
- **Quality Assessment**: Assess evidence quality before correlation analysis
- **Multiple Correlation Types**: Use temporal, causal, and spatial correlations
- **Pattern Recognition**: Look for hidden patterns and connections
- **Documentation**: Document all correlation assumptions and methodologies

## Troubleshooting

- **Insufficient Evidence**: Implement improved evidence collection procedures
- **Complex Correlations**: Use visualization tools for correlation matrix analysis
- **Conflicting Evidence**: Document all hypotheses with supporting evidence
- **Analysis Overload**: Prioritize correlation analysis based on investigation goals

## Monitoring and Metrics

- **Correlation Accuracy**: Success rate of identified correlations
- **Evidence Coverage**: Percentage of evidence sources included in correlation analysis
- **Pattern Detection Rate**: Number of hidden patterns identified per investigation
- **Correlation Strength**: Average strength of identified correlations
- **Investigation Impact**: Improvement in investigation outcomes due to correlation analysis

## Dependencies

- **Required Skills**: Evidence analysis, correlation algorithms, pattern recognition
- **Required Tools**: Python with analysis libraries, matrix computation tools, visualization
- **Required Files**: Evidence sources, metadata, investigation context, correlation parameters

## Version History

- **1.0.0**: Initial release with core evidence correlation and pattern recognition
- **1.1.0**: Added Ralph Wiggum chaos integration for creative correlation analysis
- **1.2.0**: Integrated real-time evidence monitoring and automated correlation detection

## License

MIT

## Description

The Evidence Correlation Matrix skill specializes in advanced correlation analysis of evidence across multiple forensic investigations. By applying sophisticated correlation algorithms and Ralph Wiggum-style chaotic pattern recognition, this skill identifies hidden connections, establishes evidence relationships, and builds comprehensive correlation matrices for complex investigations.

The skill implements specialized algorithms for analyzing evidence patterns, identifying correlations, and recognizing hidden connections. It goes beyond simple evidence matching to provide deep understanding of evidence relationships and their significance.

This skill is essential for conducting comprehensive forensic investigations, providing the tools needed to systematically correlate evidence and identify hidden patterns that lead to breakthroughs in complex cases.

## Workflow

1. **Evidence Assessment**: Assess available evidence sources and quality
2. **Metadata Analysis**: Analyze evidence metadata and provenance
3. **Correlation Analysis**: Apply correlation algorithms to identify relationships
4. **Pattern Recognition**: Identify hidden patterns and connections
5. **Chaos Analysis**: Analyze Ralph Wiggum-style chaotic evidence patterns
6. **Matrix Construction**: Build comprehensive correlation matrices
7. **Investigation Insights**: Generate actionable investigation insights and recommendations

## Examples

### Example 1: Coordinated Attack Investigation
**Scenario**: Multiple security incidents with potential coordination
**Process**: Correlate evidence across different systems and timelines
**Result**: Identified coordinated attack pattern with specific attack sequence

### Example 2: Complex Fraud Investigation
**Scenario**: Investigating financial fraud with multiple evidence sources
**Process**: Analyze transaction logs, communication records, and system access
**Result**: Discovered hidden connections revealing fraud network

## Asset Dependencies

- **Scripts**: correlation_matrix_core.py, pattern_analyzer.py, evidence_assessor.py
- **Templates**: correlation_matrix_schema.json, evidence_assessment_template.json
- **Reference Data**: Correlation algorithms, evidence analysis methodologies
- **Tools**: Python analysis libraries, matrix computation tools, visualization tools

## Ralph Wiggum Chaos Integration

This skill includes Ralph Wiggum-style chaotic creativity injection:

- **Unexpected Evidence Connections**: Discover correlations through chaotic evidence analysis
- **Creative Pattern Recognition**: Use entropy to identify non-obvious evidence patterns
- **Chaos-Driven Correlation**: Apply randomization to find hidden evidence relationships
- **Randomized Analysis Paths**: Explore evidence correlation from unexpected angles

The chaos engine enhances traditional evidence correlation by introducing creative approaches to pattern recognition while maintaining forensic-grade accuracy and reliability.