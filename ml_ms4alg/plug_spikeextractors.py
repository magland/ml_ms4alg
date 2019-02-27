from abc import ABC, abstractmethod
import numpy as np

class _SortingExtractor(ABC):
    def __init__(self):
        self._unit_properties = {}
        self._unit_features = {}

    @abstractmethod
    def getUnitIds(self):
        pass

    @abstractmethod
    def getUnitSpikeTrain(self, unit_id, start_frame=None, end_frame=None):
        pass

    def setUnitSpikeFeatures(self, unit_id, feature_name, value):
        if isinstance(unit_id, (int, np.integer)):
            if unit_id in self.getUnitIds():
                if unit_id not in self._unit_features.keys():
                    self._unit_features[unit_id] = {}
                if isinstance(feature_name, str) and len(value) == len(self.getUnitSpikeTrain(unit_id)):
                    self._unit_features[unit_id][feature_name] = value
                else:
                    raise ValueError("feature_name must be a string")
            else:
                raise ValueError("Non-valid unit_id")
        else:
            raise ValueError("unit_id must be an int")

    def getUnitSpikeFeatures(self, unit_id, feature_name, start_frame=None, end_frame=None):
        if isinstance(unit_id, (int, np.integer)):
            if unit_id in self.getUnitIds():
                if unit_id not in self._unit_features.keys():
                    self._unit_features[unit_id] = {}
                if isinstance(feature_name, str):
                    if feature_name in self._unit_features[unit_id].keys():
                        if start_frame is None:
                            start_frame = 0
                        if end_frame is None:
                            end_frame = len(self.getUnitSpikeTrain(unit_id))
                        return self._unit_features[unit_id][feature_name][start_frame:end_frame]
                    else:
                        raise ValueError("This feature has not been added to this unit")
                else:
                    raise ValueError("property_name must be a string")
            else:
                raise ValueError("Non-valid unit_id")
        else:
            raise ValueError("unit_id must be an int")

    def getUnitSpikeFeatureNames(self, unit_id=None):
        if unit_id is None:
            feature_names = []
            for unit_id in self.getUnitIds():
                curr_feature_names = self.getUnitSpikeFeatureNames(unit_id)
                for curr_feature_name in curr_feature_names:
                    feature_names.append(curr_feature_name)
            feature_names = sorted(list(set(feature_names)))
            return feature_names
        if isinstance(unit_id, (int, np.integer)):
            if unit_id in self.getUnitIds():
                if unit_id not in self._unit_features:
                    self._unit_features[unit_id] = {}
                feature_names = sorted(self._unit_features[unit_id].keys())
                return feature_names
            else:
                raise ValueError("Non-valid unit_id")
        else:
            raise ValueError("unit_id must be an int")

    def setUnitProperty(self, unit_id, property_name, value):
        if isinstance(unit_id, (int, np.integer)):
            if unit_id in self.getUnitIds():
                if unit_id not in self._unit_properties:
                    self._unit_properties[unit_id] = {}
                if isinstance(property_name, str):
                    self._unit_properties[unit_id][property_name] = value
                else:
                    raise ValueError("property_name must be a string")
            else:
                raise ValueError("Non-valid unit_id")
        else:
            raise ValueError("unit_id must be an int")

    def setUnitsProperty(self, *, unit_ids=None, property_name, values):
        if unit_ids is None:
            unit_ids = self.getUnitIds()
        for i, unit in enumerate(unit_ids):
            self.setUnitProperty(unit_id=unit, property_name=property_name, value=values[i])

    def addUnitProperty(self, unit_id, property_name, value):
        '''DEPRECATED!
        '''
        print('WARNING: addUnitProperty is deprecated. Use setUnitProperty instead.')
        if isinstance(unit_id, (int, np.integer)):
            if unit_id in self.getUnitIds():
                if isinstance(property_name, str):
                    self._unit_properties[unit_id][property_name] = value
                else:
                    raise ValueError("property_name must be a string")
            else:
                raise ValueError("Non-valid unit_id")
        else:
            raise ValueError("unit_id must be an int")

    def getUnitProperty(self, unit_id, property_name):
        if isinstance(unit_id, (int, np.integer)):
            if unit_id in self.getUnitIds():
                if unit_id not in self._unit_properties:
                    self._unit_properties[unit_id] = {}
                if isinstance(property_name, str):
                    if property_name in list(self._unit_properties[unit_id].keys()):
                        return self._unit_properties[unit_id][property_name]
                    else:
                        raise ValueError("This property has not been added to this unit")
                else:
                    raise ValueError("property_name must be a string")
            else:
                raise ValueError("Non-valid unit_id")
        else:
            raise ValueError("unit_id must be an int")

    def getUnitsProperty(self, *, unit_ids=None, property_name):
        if unit_ids is None:
            unit_ids = self.getUnitIds()
        values = [self.getUnitProperty(unit_id=unit, property_name=property_name) for unit in unit_ids]
        return values

    def getUnitPropertyNames(self, unit_id=None):
        if unit_id is None:
            property_names = []
            for unit_id in self.getUnitIds():
                curr_property_names = self.getUnitPropertyNames(unit_id)
                for curr_property_name in curr_property_names:
                    property_names.append(curr_property_name)
            property_names = sorted(list(set(property_names)))
            return property_names
        if isinstance(unit_id, (int, np.integer)):
            if unit_id in self.getUnitIds():
                if unit_id not in self._unit_properties:
                    self._unit_properties[unit_id] = {}
                property_names = sorted(self._unit_properties[unit_id].keys())
                return property_names
            else:
                raise ValueError("Non-valid unit_id")
        else:
            raise ValueError("unit_id must be an int")

    @staticmethod
    def writeSorting(sorting, save_path):
        raise NotImplementedError("The writeSorting function is not \
                                  implemented for this extractor")

class _SubSortingExtractor(_SortingExtractor):

    def __init__(self, parent_sorting, *, unit_ids=None, renamed_unit_ids=None, start_frame=None, end_frame=None):
        _SortingExtractor.__init__(self)
        self._parent_sorting = parent_sorting
        self._unit_ids = unit_ids
        self._renamed_unit_ids = renamed_unit_ids
        self._start_frame = start_frame
        self._end_frame = end_frame
        if self._unit_ids is None:
            self._unit_ids = self._parent_sorting.getUnitIds()
        if self._renamed_unit_ids is None:
            self._renamed_unit_ids = self._unit_ids
        if self._start_frame is None:
            self._start_frame = 0
        if self._end_frame is None:
            self._end_frame = float("inf")
        self._original_unit_id_lookup = {}
        for i in range(len(self._unit_ids)):
            self._original_unit_id_lookup[self._renamed_unit_ids[i]] = self._unit_ids[i]

    def getUnitIds(self):
        return self._renamed_unit_ids

    def getUnitSpikeTrain(self, unit_id, start_frame=None, end_frame=None):
        if start_frame is None:
            start_frame = 0
        if end_frame is None:
            end_frame = np.Inf
        if (isinstance(unit_id, (int, np.integer))):
            if (unit_id in self.getUnitIds()):
                original_unit_id = self._original_unit_id_lookup[unit_id]
            else:
                raise ValueError("Non-valid channel_id")
        else:
            raise ValueError("channel_id must be an int")
        sf = self._start_frame + start_frame
        ef = self._start_frame + end_frame
        if sf < self._start_frame:
            sf = self._start_frame
        if ef > self._end_frame:
            ef = self._end_frame
        return self._parent_sorting.getUnitSpikeTrain(unit_id=original_unit_id, start_frame=sf,
                                                      end_frame=ef) - self._start_frame

class _NumpySortingExtractor(_SortingExtractor):
    def __init__(self):
        _SortingExtractor.__init__(self)
        self._unit_ids = []
        self._units = {}
        # self._properties = {}

    def loadFromExtractor(self, sorting):
        ids = sorting.getUnitIds()
        for id in ids:
            self.addUnit(id, sorting.getUnitSpikeTrain(id))

    def setTimesLabels(self, times, labels):
        units = np.sort(np.unique(labels))
        for unit in units:
            times0 = times[np.where(labels == unit)[0]]
            self.addUnit(unit_id=int(unit), times=times0)

    def addUnit(self, unit_id, times):
        self._unit_ids.append(unit_id)
        self._units[unit_id] = dict(times=times)

    def getUnitIds(self):
        return self._unit_ids

    def getUnitSpikeTrain(self, unit_id, start_frame=None, end_frame=None):
        if start_frame is None:
            start_frame = 0
        if end_frame is None:
            end_frame = np.Inf
        times = self._units[unit_id]['times']
        inds = np.where((start_frame <= times) & (times < end_frame))[0]
        return np.rint(times[inds]).astype(int)