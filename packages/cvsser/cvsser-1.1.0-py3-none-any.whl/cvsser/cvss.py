# -*- coding: utf-8 -*-

from .cvss_guide import cvss_guide

class VectorString:
    def __init__(self, vector_string=None, guide_only=False):
        self.guide = cvss_guide
        if not guide_only:
            if not vector_string:
                raise TypeError("No vector string input was provided.")
            if type(vector_string) != str:
                raise TypeError('Input is not a string.')
            if vector_string == '':
                raise TypeError('An empty string was passed to the function.')
            self._parse(vector_string)

    def _parse(self, vector_string):
        metrics = vector_string.split('/')
        met0 = metrics[0].split(':')

        # Provisionally determine the version
        if met0[0] == "CVSS":
            metrics = metrics[1:]
            if len(metrics) < 8:
                raise ValueError('String input does not include enough metrics to be a valid CVSS vector string.')
            if met0[1] == "3.0":
                prov_version = "v3.0"
            elif met0[1] == "3.1":
                prov_version = "v3.1"
            else:
                raise ValueError('Invalid CVSS version specified.')
        else:
            if len(metrics) < 6:
                raise ValueError('String input does not include enough metrics to be a valid CVSS vector string.')
            prov_version = "v2.0"

        # Create dictionary of metrics key/value pairs
        temp_di = {}
        for m in metrics:
            kv = m.split(':')
            if len(kv) != 2:
                raise ValueError('String input has at least one metric with invalid syntax.')
            if kv[0] not in temp_di:
                temp_di[kv[0]] = kv[1]
            else:
                raise ValueError('String input has at least one duplicated metric.')

        v2_required_metrics = [k for k,v in self.guide["v2.0"].items() if v["mandatory"]]
        v2_all_metrics = list(self.guide["v2.0"])
        v3_required_metrics = [k for k,v in self.guide["v3.0"].items() if v["mandatory"]]
        v3_all_metrics = list(self.guide["v3.0"])
        included_metrics = [k for k in temp_di]

        # Check that all required metrics are present:
        if prov_version == "v2.0":
            if not all(item in included_metrics for item in v2_required_metrics):
                raise ValueError(f'Not all of the mandatory metrics ({",".join(v2_required_metrics)}) are included in the vector string')
        if prov_version == "v3.0" or prov_version == "v3.1":
            if not all(item in included_metrics for item in v3_required_metrics):
                raise ValueError(f'Not all of the mandatory metrics ({",".join(v3_required_metrics)}) are included in the vector string')

        # Check that all included metrics are valid:
        if prov_version == "v2.0":
            for m in included_metrics:
                if m not in v2_all_metrics:
                    raise ValueError(f'At least one included metric ({m}) is invalid.')
        if prov_version == "v3.0" or prov_version == "v3.1":
            for m in included_metrics:
                if m not in v3_all_metrics:
                    raise ValueError(f'At least one included metric ({m}) is invalid.')

        # Check that all values are valid:
        if prov_version in ["v3.0", "v3.1"]:
            for k,v in temp_di.items():
                if v not in self.guide["v3.0"][k]["values"]:
                    raise ValueError(f'At least one metric ({k}) has an invalid value ({v}).')

        self.metrics = temp_di
        self.version = prov_version

        # Assign instance attributes based upon metrics captured in the vector string
        for k,v in self.guide[self.version].items():
            code = k.lower()
            full_name = "_".join(v["name"].split(' ')).lower()
            if self.version == "v2.0":
                setattr(self, code, self.metrics.get(k, "ND"))
                setattr(self, full_name, self.metrics.get(k, "ND"))
            if self.version in ["v3.0", "v3.1"]:
                setattr(self, code, self.metrics.get(k, "X"))
                setattr(self, full_name, self.metrics.get(k, "X"))

    def to_dict(self, style='default', parentheticals='none', include='all'):
        if style not in ["default","verbose"]:
            raise ValueError("Invalid value for 'style' parameter. Valid values are ['default', 'verbose'].")
        if parentheticals not in ["both", "metrics", "values", "none"]:
            raise ValueError("Invalid value for 'parentheticals' parameter. Valid values are ['none', 'metrics', 'values', 'both'].")
        if include not in ["all", "mandatory", "base"]:
            raise ValueError("Invalid value for 'include' parameter. Valid values are ['all', 'mandatory', 'base'].")
        if style == 'default' and parentheticals != "none":
            raise AttributeError("The 'parentheticals' attribute is only compatible with the 'verbose' style.")

        if style == 'default':
            response = {}
            for k,v in self.guide[self.version].items():
                name = k
                val = getattr(self,k.lower())
                response[k] = {}
                response[k]["metric"] = name
                response[k]["value"] = val

        elif style == 'verbose':
            response = {}
            for k,v in self.guide[self.version].items():
                if parentheticals == "both":
                    name = f"""{v["name"]} ({k})"""
                    val = f"""{v["values"][getattr(self,k.lower())]} ({getattr(self,k.lower())})"""
                elif parentheticals == "metrics":
                    name = f"""{v["name"]} ({k})"""
                    val = f"""{v["values"][getattr(self, k.lower())]}"""
                elif parentheticals == "values":
                    name = v["name"]
                    val = f"""{v["values"][getattr(self, k.lower())]} ({getattr(self, k.lower())})"""
                elif parentheticals == "none":
                    name = v["name"]
                    val = f"""{v["values"][getattr(self, k.lower())]}"""
                response[k] = {}
                response[k]["metric"] = name
                response[k]["value"] = val

        if include == 'all':
            return response
        # If only base/mandatory metric types are required, remove the optional metrics
        elif include in ['mandatory', 'base']:
            mod_response = {}
            for k,v in response.items():
                if self.guide[self.version][k]["type"] == "Base":
                    mod_response[k] = v
            return mod_response
