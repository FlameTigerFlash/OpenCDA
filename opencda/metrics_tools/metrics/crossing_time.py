"""Intersection crossing time"""

from typing import Mapping, Any

from opencda.metrics_tools.base_metric import BaseMetric
from opencda.metrics_tools.collection_models import MetricSeries
from opencda.metrics_tools.report_models import MetricReportSpec, MetricSummarySpec
from opencda.metrics_tools.metric_sample import MetricSample

import time


class CrossingTimeMetric(BaseMetric):
    """Metric for AIM"""

    metric_name = "crossing_time"

    def __init__(self, warmup_steps: int = 100):
        super().__init__(warmup_steps=warmup_steps)
        self._samples: list[MetricSample] = []
        self.intersection_enter_time: float = 0
        self.at_intersection: bool = False

    def _process_context(self, context: Mapping[str, Any]) -> None:
        cur_at_intersection = bool(context.get("at_intersection", False))
        if cur_at_intersection and not self.at_intersection:
            self.intersection_enter_time = time.time()
        elif not cur_at_intersection and self.at_intersection:
            self._samples.append(self._make_sample(time.time() - self.intersection_enter_time))
        self.at_intersection = cur_at_intersection

    def get_raw(self) -> tuple[MetricSeries, ...]:
        return (MetricSeries(name="crossing_time", samples=tuple(self._samples)),)

    @classmethod
    def get_report_spec(cls) -> MetricReportSpec:
        return MetricReportSpec(
            metric_name=cls.metric_name,
            display_name="Crossing Time",
            series_names=("crossing_time",),
            summary_specs=(
                MetricSummarySpec(
                    series_name="crossing_time",
                    cutoff=100.0,
                ),
            ),
        )
