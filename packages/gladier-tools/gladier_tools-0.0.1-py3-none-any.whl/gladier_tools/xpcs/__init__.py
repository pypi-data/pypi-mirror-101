from gladier.defaults import GladierDefaults

from .corr import *
from .apply_qmap import *
from gladier_tools.xpcs.custom_pilot import custom_pilot
from gladier_tools.xpcs.plot import make_corr_plots

__all__ = ['EigenCorr', 'ApplyQmap', 'CustomPilot', 'MakeCorrPlots']


class EigenCorr(GladierDefaults):

    flow_definition = {
      'Comment': 'Run Corr on an HDF IMM Pair',
      'StartAt': 'Eigen Corr',
      'States': {
        'Eigen Corr': {
          'Comment': 'Eigen Corr',
          'Type': 'Action',
          'ActionUrl': 'https://api.funcx.org/automate',
          'ActionScope': 'https://auth.globus.org/scopes/facd7ccc-c5f4-42aa-916b-a0e270e2c2a9/all',
          'Parameters': {
              'tasks': [{
                'endpoint.$': '$.input.funcx_endpoint_compute',
                'func.$': '$.input.eigen_corr_funcx_id',
                'payload.$': '$.input',
            }]
          },
          'ResultPath': '$.result',
          'WaitTime': 600,
          'End': True
        }
      }
    }

    required_input = [
        'proc_dir',
        'imm_file',
        'hdf_file',
        'flags',
        'flat_file',
        'corr_loc',
    ]

    funcx_functions = [
        eigen_corr
    ]


class ApplyQmap(GladierDefaults):

    flow_definition = {
      'Comment': 'Update an HDF with a new qmap settings file',
      'StartAt': 'ApplyQmap',
      'States': {
        'ApplyQmap': {
          'Comment': 'Apply Qmap',
          'Type': 'Action',
          'ActionUrl': 'https://api.funcx.org/automate',
          'ActionScope': 'https://auth.globus.org/scopes/facd7ccc-c5f4-42aa-916b-a0e270e2c2a9/all',
          'Parameters': {
              'tasks': [{
                    'endpoint.$': '$.input.funcx_endpoint_compute',
                    'func.$': '$.input.apply_qmap_funcx_id',
                    'payload.$': '$.input',
                }]
          },
          'ResultPath': '$.result',
          'WaitTime': 600,
          'End': True
        }
      }
    }

    required_input = [
        'proc_dir',
        'qmap_file',
        'flat_file',
    ]

    funcx_functions = [
        apply_qmap
    ]


class MakeCorrPlots(GladierDefaults):

    flow_definition = {
      'Comment': 'Generate plots for a corr run. REQUIRES globus-automation to be INSTALLED',
      'StartAt': 'MakeCorrPlots',
      'States': {
        'MakeCorrPlots': {
          'Comment': 'Plot the results of a corr run, given the result hdf file',
          'Type': 'Action',
          'ActionUrl': 'https://api.funcx.org/automate',
          'ActionScope': 'https://auth.globus.org/scopes/facd7ccc-c5f4-42aa-916b-a0e270e2c2a9/all',
          'Parameters': {
              'tasks': [{
                'endpoint.$': '$.input.funcx_endpoint_compute',
                'func.$': '$.input.make_corr_plots_funcx_id',
                'payload.$': '$.input',
            }]
          },
          'ResultPath': '$.result',
          'WaitTime': 600,
          'End': True
        }
      }
    }

    required_input = [
        'proc_dir',
        'hdf_file',
    ]

    funcx_functions = [
        make_corr_plots
    ]


class CustomPilot(GladierDefaults):

    flow_definition = {
      'Comment': 'Run Pilot and upload the result to search + petreldata',
      'StartAt': 'CustomPilot',
      'States': {
        'CustomPilot': {
          'Comment': 'Upload to petreldata, ingest to xpcs search index',
          'Type': 'Action',
          'ActionUrl': 'https://api.funcx.org/automate',
          'ActionScope': 'https://auth.globus.org/scopes/facd7ccc-c5f4-42aa-916b-a0e270e2c2a9/all',
          'Parameters': {
              'tasks': [{
                'endpoint.$': '$.input.funcx_endpoint_non_compute',
                'func.$': '$.input.custom_pilot_funcx_id',
                'payload.$': '$.input',
            }]
          },
          'ResultPath': '$.result',
          'WaitTime': 600,
          'End': True
        }
      }
    }

    flow_input = {
        'reprocessing_suffix': '_qmap',
    }

    required_input = [
        'proc_dir',
        'hdf_file',
        'reprocessing_suffix',
    ]

    funcx_functions = [
        custom_pilot
    ]
