import re
path = r"d:\Node\personal\3d\www.verostudio.com\www.verostudio.com\_next\static\chunks\0s5vc7gzwd48m.js"
data = open(path, encoding="utf-8").read()

# Find FullSizeScrollerStepper component implementation
for label, pat in [
    ("useId", r".{0,200}useId.{0,200}"),
    ("StepperItem", r".{0,100}FullSizeScrollerStepperItem.{0,200}"),
    ("Mask.Inject", r".{0,80}Mask\.Inject|Inject.{0,40}mask"),
    ("onProgress", r".{0,120}onProgressChange.{0,200}"),
    ("--active", r".{0,100}--active.{0,150}"),
]:
    print("====", label)
    for m in re.finditer(pat, data):
        print(m.group()[:300])
        print("---")
        if label != "useId":
            break

# Better: extract module that contains FullSizeScrollerStepperItem string near component
idx = data.find('FullSizeScrollerStepperItemBeacon')
print("\nBeacon idx", idx)
print(data[idx-500:idx+2500] if idx>=0 else "missing")
