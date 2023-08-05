import argparse

from k8kat.auth.kube_broker import broker

from kama_sdk import worker, opsim, server, shell
from kama_sdk.core.core import config_man_helper, utils, config_man
from kama_sdk.model.base import static_validator
from kama_sdk.model.base.model import models_man


def collect_args() -> argparse.Namespace:
  parser = argparse.ArgumentParser(description='Process some integers.')
  parser.add_argument(
    "-m",
    "--mode",
    default='server',
    choices=["server", "worker", "telem_worker", "shell", "opsim"],
    help="which type of process should start"
  )

  parser.add_argument(
    "-ns",
    "--namespace",
    help="coerce a kubernetes namespace during development"
  )

  return parser.parse_args()


def process_coerce_ns_request(args: argparse.Namespace):
  if ns := args.namespace:
    if not utils.is_in_cluster():
      config_man.coerce_ns(ns)
      print(f"[kama_sdk:entrypoint] coerced namespace to {ns}")
    else:
      print(f"[kama_sdk:entrypoint] cannot coerce namespace while in-cluster")


def start():
  args = collect_args()
  broker.connect()
  models_man.add_defaults()
  config_man_helper.clear_trackers()
  static_validator.run_all()
  process_coerce_ns_request(args)

  if args.mode == 'server':
    server.start()
  elif args.mode == 'worker':
    worker.start_main()
  elif args.mode == 'telem_worker':
    worker.start_telem()
  elif args.mode == 'opsim':
    opsim.start()
  elif args.mode == 'shell':
    shell.start()
  else:
    print(f"Unrecognized exec mode {args.mode}")
