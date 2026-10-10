.PHONY: test validate example verify package

test:
	python -m pytest -q

validate:
	python scripts/validate_plugin.py
	python -m compileall -q video_workflow skills adapters scripts

example:
	bash scripts/render_example.sh

verify:
	python scripts/verify_release.py

package: verify
	bash scripts/package_plugin.sh
