#!/usr/bin/env python3

import sys
import multiprocessing

from mountainlab_pytools.mlprocessors.registry import registry, register_processor

registry.namespace = "ms4alg_new"

from mountainlab_pytools.mlprocessors.core import Input, Output, Processor
from mountainlab_pytools.mlprocessors.core import FloatParameter, IntegerParameter
from mountainlab_pytools.mlprocessors.validators import Validator, FileExtensionValidator

class MdaInput(Input):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.insert(0, FileExtensionValidator(["mda"]))


@register_processor(registry)
class apply_label_map(Processor):
    VERSION="0.12.1"
    AUTHOR='J Chung and J Magland'

    firings = MdaInput()
    label_map = MdaInput()
    firings_out = Output()

    def run(self):
        from p_apply_label_map import apply_label_map as original_apply_label_map
        return original_apply_label_map(firings = self.firings,
                                        label_map = self.label_map,
                                        firings_out = self.firings_out)

@register_processor(registry)
class create_label_map(Processor):
    VERSION='0.11.1'
    AUTHOR='J Chung and J Magland'

    metrics = Input()
    label_map = Output()

    firing_rate_thresh = FloatParameter(optional=True)
    isolation_thresh = FloatParameter(optional=True)
    noise_overlap_thresh = FloatParameter(optional=True)
    peak_snr_thresh = FloatParameter(optional=True)

    def run(self):
        from p_create_label_map import create_label_map as original_create_label_map
        return original_create_label_map(
            metrics = self.metrics,
            label_map = self.label_map,
            firing_rate_thresh = self.firing_rate_thresh,
            isolation_thresh = self.isolation_thresh,
            noise_overlap_thresh = self.noise_overlap_thresh,
            peak_snr_thresh = self.peak_snr_thresh
        )

@register_processor(registry)
class sort(Processor):
    VERSION='0.11'

    timeseries = Input()
    geom = Input(optional=True)
    firings_out = Output()

    adjacency_radius = FloatParameter()
    detect_sign = IntegerParameter(choices=[1, -1, 0])
    detect_threshold = FloatParameter()
    detect_interval = IntegerParameter()
    clip_size = IntegerParameter()
    num_workers = IntegerParameter(optional=True, default=multiprocessing.cpu_count())

    def run(self):
        from p_ms4alg import sort as original_sort
        return original_sort(
            timeseries = self.timeseries,
            geom = self.geom,
            firings_out = self.firings_out,
            adjacency_radius = self.adjacency_radius,
            detect_sign = self.detect_sign,
            detect_threshold = self.detect_threshold,
            detect_interval = self.detect_interval,
            clip_size = self.clip_size,
            num_workers = self.num_workers
        )

if __name__ == "__main__":
    registry.process(sys.argv)
