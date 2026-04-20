import pytest
import os

if __name__ == "__main__":
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    pytest.main([
        os.path.join(project_root, "tests"),
        f"--html={os.path.join(project_root, 'reports/html/report.html')}"
    ])