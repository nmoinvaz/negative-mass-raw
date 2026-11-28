#!/bin/bash
# the queue of record: the runs of jobs_record.txt, then the lints and tests of jobs_lint.txt; one job at a time
here=$(cd "$(dirname "$0")" && pwd)
"$here/run_queue.sh" "$here/jobs_record.txt"
"$here/run_queue.sh" "$here/jobs_lint.txt"
