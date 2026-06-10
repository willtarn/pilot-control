"""Optional local runner for Pilot Control Inspect tasks.

Example:
    python -m inspect_eval.run_pilot_control --split dev --model openai/gpt-4o-mini
"""

from __future__ import annotations

import argparse
from inspect_ai import eval
from .pilot_control_task import pilot_control


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--split', default='dev', choices=['all', 'dev', 'test'])
    parser.add_argument('--model', default='openai/gpt-4o-mini')
    parser.add_argument('--scenario-family', default=None)
    parser.add_argument('--log-dir', default='./logs')
    args = parser.parse_args()
    eval(
        pilot_control(split=args.split, scenario_family=args.scenario_family),
        model=args.model,
        log_dir=args.log_dir,
    )


if __name__ == '__main__':
    main()
