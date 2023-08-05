

def make_corr_plots(event):
    import json
    with open(event['parameter_file']) as f:
        event = json.load(f)
    import os
    from XPCS.tools import xpcs_plots
    os.chdir(os.path.join(event['proc_dir'], os.path.dirname(event['hdf_file'])))
    try:
        xpcs_plots.make_plots(os.path.join(event['proc_dir'], event['hdf_file']))
    except (Exception, SystemExit) as e:
        return str(e)
    return [img for img in os.listdir('.') if img.endswith('.png')]
