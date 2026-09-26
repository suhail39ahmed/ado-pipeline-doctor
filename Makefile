.PHONY: help install demo test clean

help:
	@echo "Targets: install | demo | clean"

install:
	pip install -e .

demo:
	python -m pipeline_doctor fixtures/azure-pipelines/nuget-auth-fail.log >/tmp/ado-rca1.json
	python -m pipeline_doctor fixtures/github-actions/pytest-fail.log -o /tmp/ado-rca2.json
	@grep -q human_approval_required /tmp/ado-rca1.json
	@echo "✓ ado-pipeline-doctor demo OK — RCA JSON with human_approval_required" 

clean:
	rm -rf .venv dist build *.egg-info reports labs out audit.log __pycache__
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
