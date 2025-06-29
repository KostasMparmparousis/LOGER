import os
from lib import filepath as fp
from tqdm import tqdm
from core.sql import Sql
import torch
from lib.timer import timer

def _load(directory, verbose=False):
    L = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.sql'):
                L.append(os.path.join(root, file))
    res = []
    if verbose:
        L = tqdm(L, desc='Loading files')
    for file in L:
        with open(file, 'r') as f:
            data = ' '.join(f.readlines())
            res.append((data, file))
    return res


def load(config, directory, device=torch.device('cpu'), verbose=False, detail=False):
    _timer = timer()

    # Ensure directory is absolute
    directory = os.path.abspath(directory)

    # Create a cache file name based on the directory name
    dir_name = os.path.basename(directory.rstrip(os.sep))
    parent_dir = os.path.dirname(directory)

    cache_filename = f'.{dir_name}.detail.pkl' if detail else f'.{dir_name}.pkl'
    cache_file = os.path.join(parent_dir, cache_filename)

    # Create the parent directory for the cache file if it doesn't exist
    os.makedirs(parent_dir, exist_ok=True)

    if os.path.isfile(cache_file):
        return torch.load(cache_file, map_location=device)

    res = []
    _detail = []
    gen = _load(directory, verbose=verbose)
    if verbose:
        gen = tqdm(gen, desc='Parsing')

    for sql, filename in gen:
        print(filename)
        fname = os.path.basename(filename)
        with _timer:
            sql = Sql(sql, config.feature_length, filename=fname)
        _detail.append((_timer.time))
        sql.to(device)
        res.append(sql)

    if detail:
        torch.save((res, _detail), cache_file)
        return res, _detail
    torch.save(res, cache_file)
    return res

def safe_load(config, directory, device=torch.device('cpu'), verbose=False, detail=False):
    """Wrapper around load() that ensures proper path handling"""
    # Convert to absolute path
    directory = os.path.abspath(directory)
    
    # Create cache directory in the workload directory instead of parent
    cache_dir = os.path.join(directory, '.cache')
    os.makedirs(cache_dir, exist_ok=True)
    
    # Set cache file path
    dir_name = os.path.basename(directory.rstrip('/'))
    if detail:
        cache_file = os.path.join(cache_dir, f'{dir_name}.detail.pkl')
    else:
        cache_file = os.path.join(cache_dir, f'{dir_name}.pkl')
    
    # Try loading from cache
    if os.path.isfile(cache_file):
        try:
            return torch.load(cache_file, map_location=device)
        except:
            print("Warning: Corrupt cache file, regenerating...")
            os.remove(cache_file)
    
    # Load fresh if no cache
    res = []
    _detail = []
    gen = _load(directory, verbose=verbose)
    if verbose:
        gen = tqdm(gen, desc='Parsing')
        
    for sql, filename in gen:
        fname = os.path.basename(filename)
        with timer() as _timer:
            sql = Sql(sql, config.feature_length, filename=fname)
        _detail.append(_timer.time)
        sql.to(device)
        res.append(sql)
    
    # Save to cache
    try:
        if detail:
            torch.save((res, _detail), cache_file)
            return res, _detail
        torch.save(res, cache_file)
        return res
    except Exception as e:
        print(f"Warning: Could not save cache: {str(e)}")
        return res if not detail else (res, _detail)