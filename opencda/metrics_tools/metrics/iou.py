"""Intersection load metric"""

from typing import Mapping, Any

from opencda.metrics_tools.base_metric import BaseMetric
from opencda.metrics_tools.collection_models import MetricSeries
from opencda.metrics_tools.report_models import MetricReportSpec, MetricSummarySpec
from opencda.metrics_tools.metric_sample import MetricSample


class IntersectionOverUnionMetric(BaseMetric):
    """Metric for COP"""

    metric_name = "iou"

    def __init__(self, warmup_steps: int = 100):
        super().__init__(warmup_steps=warmup_steps)
        self._samples: list[MetricSample] = []

    def _process_context(self, context: Mapping[str, Any]) -> None:
        iou = list(context.get("iou", []))
        for el in iou:
            self._samples.append(self._make_sample(el))

    def get_raw(self) -> tuple[MetricSeries, ...]:
        return (MetricSeries(name="iou", samples=tuple(self._samples)),)

    @classmethod
    def get_report_spec(cls) -> MetricReportSpec:
        return MetricReportSpec(
            metric_name=cls.metric_name,
            display_name="Intersection Over Union",
            series_names=("iou",),
            summary_specs=(
                MetricSummarySpec(
                    series_name="iou",
                    cutoff=100.0,
                ),
            ),
        )
