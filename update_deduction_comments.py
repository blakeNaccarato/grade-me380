from dynaconf import Dynaconf

deductions = Dynaconf(settings_files=["deductions.yaml"]).deductions
print([deduction.text for deduction in deductions if deduction.code == "G3"][0])
