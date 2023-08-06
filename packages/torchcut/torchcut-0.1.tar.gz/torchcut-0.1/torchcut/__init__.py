import warnings
import importlib

imports = {
    'mandatory': {
        'torch': {
            'torch': 'torch',
            'torch.nn': 'nn',
            'torch.nn.functional': 'F',
            'torch.optim': 'optim'
        }
    },
    'optional': {
        'torchvision': {
            'torchvision': 'tv',
            'torchvision.transforms': 'transforms',
        },
        'torchtext': {
            'torchtext': 'tt'
        },
        'numpy': {
            'numpy': 'np'
        },
        'pandas': {
            'pandas': 'pd'
        }
    }
}


__all__ = []


def do_imports(definitions, ignore_import_error=False):
    for name, mapping in definitions.items():
        try:
            for package, import_as in mapping.items():
                globals()[import_as] = importlib.import_module(package)
                __all__.append(import_as)
        except ImportError:
            if ignore_import_error:
                warnings.warn('{} is not installed and won\'t be available.'.format(name))


do_imports(imports['mandatory'], ignore_import_error=False)
do_imports(imports['optional'], ignore_import_error=True)
