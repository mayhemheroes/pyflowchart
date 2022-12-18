#! /usr/bin/env python3
import atheris
import sys
import fuzz_helpers

with atheris.instrument_imports():
    import pyflowchart

def TestOneInput(data):
    if len(data) < 2:
        return
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    py_code = fdp.ConsumeRandomString()
    try:
        fc = pyflowchart.Flowchart.from_code(py_code,
                                        inner=fdp.ConsumeBool(),
                                        conds_align=fdp.ConsumeBool(),
                                        simplify=fdp.ConsumeBool())
        fc.flowchart()
    except SyntaxError:
        return -1
    except ValueError as e:
        if 'null bytes' in str(e):
            return -1
        raise
    except AssertionError as e:
        if 'nothing' in str(e):
            return -1
        raise


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
