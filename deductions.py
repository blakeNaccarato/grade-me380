from dynaconf import Dynaconf

all_deductions = Dynaconf(
    settings_files=["deductions_common.yaml", "deductions_lab_specific.yaml"],
    
)
