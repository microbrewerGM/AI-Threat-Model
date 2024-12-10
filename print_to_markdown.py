import yaml
from pathlib import Path

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def generate_markdown(data):
    md = []
    md.append("---\n")

    # Header Information
    md.append(f"# {data.get('title', 'Threat Model')}\n")
    md.append(f"**Threat Model Report via Threagile**\n")
    md.append("## Header Information\n")
    md.append(f"- **Title:** {data.get('title', '')}")
    md.append(f"- **Date:** {data.get('date', '')}")
    md.append(f"- **Version:** {data.get('threagile_version', '')}")

    # Author Information
    author = data.get('author', {})
    if author:
        md.append(f"- **Author:**")
        md.append(f"  - **Name:** {author.get('name', '')}")
        md.append(f"  - **Homepage:** [{author.get('homepage', '')}]({author.get('homepage', '')})")

    # Contributors Information
    contributors = data.get('contributors', [])
    if contributors:
        md.append(f"- **Contributors:**")
        for contributor in contributors:
            md.append(f"  - **Name:** {contributor.get('name', '')}")
            if 'contact' in contributor:
                md.append(f"    - **Contact:** {contributor.get('contact', '')}")
            if 'homepage' in contributor:
                md.append(f"    - **Homepage:** [{contributor.get('homepage', '')}]({contributor.get('homepage', '')})")

    # Management Summary Comment
    management_comment = data.get('management_summary_comment', '')
    if management_comment:
        md.append(f"- **Management Summary Comment:** {management_comment}\n")
    else:
        md.append(f"- **Management Summary Comment:** *[To be added]*\n")

    md.append("---\n")

    # To Do List
    to_do = data.get('toDo', '')
    if to_do:
        md.append("## To Do\n")
        # Assuming 'toDo' contains a list in YAML; if it's a string, adjust accordingly
        try:
            to_do_items = yaml.safe_load(to_do)
            for item in to_do_items:
                if isinstance(item, dict):
                    for key, sub_items in item.items():
                        md.append(f"- **{key}**:")
                        for sub_item in sub_items:
                            md.append(f"  - {sub_item}")
                else:
                    md.append(f"- {item}")
        except yaml.YAMLError:
            # If 'toDo' is a plain string
            md.append(to_do.strip() + "\n")
        md.append("---\n")

    # Technical Assets
    technical_assets = data.get('technical_assets', {})
    if technical_assets:
        md.append("## Assets\n")
        for asset_name, asset in technical_assets.items():
            md.append(f"### {asset_name}\n")
            md.append(f"- **ID:** `{asset.get('id', '')}`")
            md.append(f"- **Description:** {asset.get('description', '')}")
            md.append(f"- **Type:** {asset.get('type', '')}")
            md.append(f"- **Usage:** {asset.get('usage', '')}")
            md.append(f"- **Used as Client by Human:** {asset.get('used_as_client_by_human', False)}")
            md.append(f"- **Out of Scope:** {asset.get('out_of_scope', False)}")
            md.append(f"- **Size:** {asset.get('size', '')}")
            md.append(f"- **Technology:** {asset.get('technology', '')}")
            tags = asset.get('tags', [])
            if tags:
                md.append(f"- **Tags:** {', '.join(tags)}")
            md.append(f"- **Internet Accessible:** {asset.get('internet', False)}")
            md.append(f"- **Machine:** {asset.get('machine', '')}\n")

            # Data Assets Processed
            data_assets_processed = asset.get('data_assets_processed', [])
            if data_assets_processed:
                md.append("**Data Assets Processed:**")
                for da in data_assets_processed:
                    md.append(f"- `{da}`")
                md.append("")

            # Data Assets Stored
            data_assets_stored = asset.get('data_assets_stored', [])
            if data_assets_stored:
                md.append("**Data Assets Stored:**")
                for da in data_assets_stored:
                    md.append(f"- `{da}`")
                md.append("")

            # Data Formats Accepted
            data_formats_accepted = asset.get('data_formats_accepted', [])
            if data_formats_accepted:
                md.append("**Data Formats Accepted:**")
                for df in data_formats_accepted:
                    md.append(f"- {df.capitalize()}")
                md.append("")

            md.append("---\n")

    # Abuse Cases
    abuse_cases = data.get('abuse_cases', {})
    if abuse_cases:
        md.append("## Abuse Cases\n")
        for abuse_name, abuse in abuse_cases.items():
            md.append(f"### {abuse_name}\n")
            lines = abuse.split('\n')
            description = []
            example = []
            vectors = []
            guardrails = []
            current_section = None
            for line in lines:
                line = line.strip()
                if line.startswith('Example: >'):
                    current_section = 'example'
                    continue
                elif line.startswith('Vectors:'):
                    current_section = 'vectors'
                    continue
                elif line.startswith('Guardrails:'):
                    current_section = 'guardrails'
                    continue
                elif line.endswith(': >') or line.endswith(': >') or not line:
                    current_section = None
                    continue

                if current_section == 'description' or not current_section:
                    description.append(line)
                elif current_section == 'example':
                    example.append(line)
                elif current_section == 'vectors':
                    vectors.append(line)
                elif current_section == 'guardrails':
                    guardrails.append(line)

            # In this YAML, 'Prompt Injection' abuse_case is a single '>' block, the summary is likely above, so adjust accordingly
            # Instead, assume 'description' is everything until 'Example:', then 'example', etc.
            # For simplicity, we'll re-use the initial lines as description
            md.append(f"**Description:** {abuse}")
            md.append("\n**Example:**")
            if example:
                md.append("```")
                md.append("\n".join(example))
                md.append("```\n")
            md.append("**Vectors:**")
            for vector in vectors:
                md.append(f"- {vector}")
            md.append("**Guardrails:**")
            for guard in guardrails:
                md.append(f"- {guard}")
            md.append("---\n")

    # Security Requirements
    security_requirements = data.get('security_requirements', {})
    if security_requirements:
        md.append("## Security Requirements\n")
        for req_name, req in security_requirements.items():
            md.append(f"### {req_name}\n")
            lines = req.split('\n')
            scope = ""
            type_ = ""
            description = ""
            action = ""
            mitigation = ""
            check = ""
            steps = []
            criteria = []
            drawbacks = []
            usage = ""
            asvs = ""
            cheat_sheet = ""
            user_satisfaction = ""
            context_recall = ""
            context_relevance = ""
            ulg = ""
            for line in lines:
                line = line.strip()
                if line.startswith('Scope:'):
                    scope = line.replace('Scope:', '').strip()
                elif line.startswith('Type:'):
                    type_ = line.replace('Type:', '').strip()
                elif line.startswith('Description:'):
                    description = line.replace('Description:', '').strip()
                elif line.startswith('Action:'):
                    action = line.replace('Action:', '').strip()
                elif line.startswith('Mitigation:'):
                    mitigation = line.replace('Mitigation:', '').strip()
                elif line.startswith('Check:'):
                    check = line.replace('Check:', '').strip()
                elif line.startswith('Steps:'):
                    current_section = 'steps'
                    continue
                elif line.startswith('Criteria:'):
                    current_section = 'criteria'
                    continue
                elif line.startswith('Drawbacks:'):
                    current_section = 'drawbacks'
                    continue
                elif line.startswith('Usage:'):
                    usage = line.replace('Usage:', '').strip()
                elif line.startswith('ASVS:'):
                    asvs = line.replace('ASVS:', '').strip()
                elif line.startswith('cheat_sheet:'):
                    cheat_sheet = line.replace('cheat_sheet:', '').strip()
                elif line.startswith('User Satisfaction:'):
                    user_satisfaction = line.replace('User Satisfaction:', '').strip()
                elif line.startswith('Context Recall:'):
                    context_recall = line.replace('Context Recall:', '').strip()
                elif line.startswith('Context Relevance:'):
                    context_relevance = line.replace('Context Relevance:', '').strip()
                elif line.startswith('Usage:'):
                    usage = line.replace('Usage:', '').strip()
                elif line.startswith('Out of Scope:'):
                    usage = line.replace('Out of Scope:', '').strip()
                elif line.startswith('Steps:'):
                    current_section = 'steps'
                    continue
                elif line.startswith('Criteria:'):
                    current_section = 'criteria'
                    continue
                elif line.startswith('Drawbacks:'):
                    current_section = 'drawbacks'
                    continue
                elif current_section == 'steps':
                    steps.append(line)
                elif current_section == 'criteria':
                    criteria.append(line)
                elif current_section == 'drawbacks':
                    drawbacks.append(line)

            md.append(f"- **Scope:** {scope}")
            if type_:
                md.append(f"- **Type:** {type_}")
            if description:
                md.append(f"- **Description:** {description}")
            if action:
                md.append(f"- **Action:** {action}")
            if mitigation:
                md.append(f"- **Mitigation:** {mitigation}")
            if check:
                md.append(f"- **Check:** {check}")
            if criteria:
                md.append("  - **Criteria:**")
                for criterion in criteria:
                    md.append(f"    - {criterion}")
            if steps:
                md.append("  - **Steps:**")
                for step in steps:
                    md.append(f"    - {step}")
            if drawbacks:
                md.append("  - **Drawbacks:**")
                for drawback in drawbacks:
                    md.append(f"    - {drawback}")
            if usage:
                md.append(f"- **Usage:** {usage}")
            if asvs:
                md.append(f"- **ASVS:** {asvs}")
            if cheat_sheet:
                md.append(f"- **Cheat Sheet:** [{cheat_sheet}]({cheat_sheet})")
            if user_satisfaction:
                md.append(f"- **User Satisfaction:** {user_satisfaction}")
            if context_recall:
                md.append(f"- **Context Recall:** {context_recall}")
            if context_relevance:
                md.append(f"- **Context Relevance:** {context_relevance}")
            md.append("\n---\n")

    # Individual Risk Categories
    individual_risk_categories = data.get('individual_risk_categories', {})
    if individual_risk_categories:
        md.append("## Individual Risk Categories\n")
        for risk_name, risk in individual_risk_categories.items():
            if not isinstance(risk, dict):  # Skip non-dictionary entries
                continue
            md.append(f"### {risk_name}\n")
            for key, value in risk.items():
                if key != 'risks_identified':
                    md.append(f"- **{key.replace('_', ' ').capitalize()}:** {value}")
            # Handle nested risks_identified
            risks_identified = risk.get('risks_identified', {})
            if risks_identified:
                md.append("\n**Risks Identified:**")
                for sub_risk, details in risks_identified.items():
                    md.append(f"- **{sub_risk}**")
                    for detail_key, detail_value in details.items():
                        md.append(f"  - **{detail_key.replace('_', ' ').capitalize()}:** {detail_value}")
            md.append("---\n")

    # Risk Tracking
    risk_tracking = data.get('risk_tracking', {})
    if risk_tracking:
        md.append("## Risk Tracking\n")
        md.append("| Risk ID | Status | Justification | Ticket | Date | Checked By | Severity | Exploitation Likelihood | Exploitation Impact | Detection Logic | Risk Assessment | False Positives | CWE | Impact | Action | Mitigation |")
        md.append("|---------|--------|---------------|--------|------|------------|----------|------------------------|---------------------|-----------------|-----------------|------------------|-----|--------|--------|------------|")
        for risk_id, details in risk_tracking.items():
            status = details.get('status', '')
            justification = details.get('justification', '').replace('|', '\\|')
            ticket = details.get('ticket', '')
            date = details.get('date', '')
            checked_by = details.get('checked_by', '').replace('|', '\\|')
            severity = details.get('severity', '')
            exploitation_likelihood = details.get('exploitation_likelihood', '')
            exploitation_impact = details.get('exploitation_impact', '')
            detection_logic = details.get('detection_logic', '').replace('|', '\\|')
            risk_assessment = details.get('risk_assessment', '').replace('|', '\\|')
            false_positives = details.get('false_positives', '').replace('|', '\\|')
            cwe = details.get('cwe', '')
            impact = details.get('impact', '').replace('|', '\\|')
            action = details.get('action', '').replace('|', '\\|')
            mitigation = details.get('mitigation', '').replace('|', '\\|')

            md.append(f"| {risk_id} | {status} | {justification} | {ticket} | {date} | {checked_by} | {severity} | {exploitation_likelihood} | {exploitation_impact} | {detection_logic} | {risk_assessment} | {false_positives} | {cwe} | {impact} | {action} | {mitigation} |")
        md.append("---\n")

    return '\n'.join(md)

def main():
    yaml_file = 'GenAI-RAG-Threat-Model.yaml'  # Replace with your YAML file path
    data = load_yaml(yaml_file)
    markdown_content = generate_markdown(data)

    # Save to a Markdown file
    output_file = Path(yaml_file).stem + '.md'
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(markdown_content)
    print(f"Markdown file '{output_file}' generated successfully.")

if __name__ == '__main__':
    main()
