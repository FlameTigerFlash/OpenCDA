"""Intersection load metric"""

from typing import Mapping, Any

from opencda.metrics_tools.base_metric import BaseMetric
from opencda.metrics_tools.collection_models import MetricSeries
from opencda.metrics_tools.report_models import MetricReportSpec, MetricSummarySpec
from opencda.metrics_tools.metric_sample import MetricSample


class IntersectionLoadMetric(BaseMetric):
    """Metric for AIM"""

    metric_name = "free_space"

    def __init__(self, warmup_steps: int = 100):
        super().__init__(warmup_steps=warmup_steps)
        self._samples: list[MetricSample] = []

    def _process_context(self, context: Mapping[str, Any]) -> None:
        free_space = float(context.get("free_space", 0.0))
        self._samples.append(self._make_sample(free_space))

    def get_raw(self) -> tuple[MetricSeries, ...]:
        return (MetricSeries(name="free_space", samples=tuple(self._samples)),)

    @classmethod
    def get_report_spec(cls) -> MetricReportSpec:
        return MetricReportSpec(
            metric_name=cls.metric_name,
            display_name="Free Space",
            series_names=("free_space",),
            summary_specs=(
                MetricSummarySpec(
                    series_name="free_space",
                    cutoff=100.0,
                ),
            ),
        )
