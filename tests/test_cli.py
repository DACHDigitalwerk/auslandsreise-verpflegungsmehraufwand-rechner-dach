# -*- coding: utf-8 -*-
import json
import subprocess
import sys


def test_cli_help():
    cmd = [sys.executable, "automation/github_staging/repo23/auslandsreise_dach/cli.py", "--help"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
    assert "dach-ausland" in res.stdout
    assert "--destination" in res.stdout


def test_cli_list_destinations():
    cmd = [sys.executable, "automation/github_staging/repo23/auslandsreise_dach/cli.py", "--list-destinations"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
    assert "BMF Auslandstagegelder" in res.stdout
    assert "USA_NEW_YORK" in res.stdout
    assert "SCHWEIZ_ZUERICH" in res.stdout


def test_cli_search():
    cmd = [sys.executable, "automation/github_staging/repo23/auslandsreise_dach/cli.py", "--search", "wien"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
    assert "OESTERREICH_WIEN" in res.stdout
    assert "Wien" in res.stdout


def test_cli_calculation():
    cmd = [
        sys.executable,
        "automation/github_staging/repo23/auslandsreise_dach/cli.py",
        "--destination", "UK_LONDON",
        "--days", "3",
        "--breakfasts", "2",
        "--lunches", "1",
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
    assert "Großbritannien (London)" in res.stdout
    assert "GESAMTANSPRUCH (STEUERFREI)" in res.stdout


def test_cli_json_output():
    cmd = [
        sys.executable,
        "automation/github_staging/repo23/auslandsreise_dach/cli.py",
        "--destination", "FRANKREICH_PARIS",
        "--days", "2",
        "--json",
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
    data = json.loads(res.stdout)
    assert data["destination"] == "Frankreich (Paris)"
    assert data["total_days"] == 2
    assert "grand_total_reimbursement" in data
