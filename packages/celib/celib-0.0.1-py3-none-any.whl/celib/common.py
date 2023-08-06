import time
import logging
import os
import numpy as np
import pandas as pd
import random
import glob
from functools import wraps
from multiprocessing import cpu_count
from pathos.multiprocessing import ProcessingPool as Pool


class RunningTimeDecorator:
    """
    실행 시간 표시 데코레이터
    """

    def __init__(self, logger=None, show_section: bool = True, show_pid: bool = True):
        self.__param = logger
        self.__show_section = show_section
        self.__show_pid = show_pid

    def __call__(self, func):
        def printLog(str_arg):
            if isinstance(self.__param, logging.Logger):
                logger = logging.getLogger(self.__param.name)
                logger.info(str_arg)
            else:
                print(str_arg)

        @wraps(func)
        def decorator(*args, **kwargs):
            str_current_pid = ""

            if self.__show_section:
                if self.__show_pid:
                    str_current_pid = "(PID:" + str(os.getpid()) + ")"
                str_start = "{0}{1} Started.".format(func.__name__, str_current_pid)
                printLog(str_start)

            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()

            if self.__show_section:
                if self.__show_pid:
                    str_current_pid = "(PID:" + str(os.getpid()) + ")"
                str_finish = "{0}{1} Finished.".format(func.__name__, str_current_pid)
                printLog(str_finish)
            str_log = "{0}{1} Elapsed Time : {2:.2f} seconds".format(
                func.__name__, str_current_pid, end_time - start_time
            )
            printLog(str_log)
            return result

        return decorator


def get_last_dir(dir: str, by: str = "name"):
    """
    디렉토리 내림차순 정렬로 가장 마지막 디렉토리 경로 리턴
    by = "name" or "mtime"
    """
    dir_list = filter(os.path.isdir, glob.glob(dir + "/*"))
    if by == "mtime":
        sort_by = os.path.getmtime
    elif by == "ctime":
        sort_by = os.path.getctime
    elif by == "atime":
        sort_by = os.path.getatime
    elif by == "name":
        return max(dir_list)
    return max(dir_list, key=sort_by)


def parallelize_dataframe(func, df: pd.DataFrame):
    """
    데이터 프레임을 분할해서 병렬 처리
    """
    num_cores = cpu_count() - 1
    pool = Pool(num_cores)

    df_split = np.array_split(df, num_cores)

    len_df = len(df_split)
    if len_df < num_cores:
        num_cores = len_df

    df = pd.concat(pool.map(func, df_split))

    pool.close()
    pool.join()
    pool.clear()
    return df


def parallelize_dataframe_with_args(func, df: pd.DataFrame, *args):
    """
    데이터 프레임을 분할해서 병렬 처리(병렬처리 함수에 인자값이 있는 경우)
    """
    num_cores = cpu_count() - 1
    pool = Pool(num_cores)

    df_split = np.array_split(df, num_cores)

    len_df = len(df_split)
    if len_df < num_cores:
        num_cores = len_df

    list_tuple_args = []
    list_args = list(args)

    for item in df_split:
        each_list = [item]
        each_list.append(list_args)
        list_tuple_args.append(tuple(each_list))
    df = pd.concat(pool.map(lambda x: func(*x), list_tuple_args))
    pool.close()
    pool.join()
    pool.clear()
    return df


def string_to_boolean(arg_str: str):
    """
    return
        True: if in ["true", "1"]
        False : if in ["false", "0"]
        np.NaN : else
    """
    list_true = ["true", "1", "yes"]
    list_false = ["false", "0", "no"]

    if arg_str.lower() in list_true:
        return True
    if arg_str.lower() in list_false:
        return False
    return np.NaN


def set_random_seed(seed: int = 47):
    """
    랜덤 시드 초기화
    """
    np.random.seed(seed)
    random.seed(seed)
    # tf.set_random_seed(seed)
    # tf.random.set_seed(seed)


def list_chunk(lst: list, n: int):
    """
    list 분할
    """
    return [lst[i : i + n] for i in range(0, len(lst), n)]


def unnesting(df: pd.DataFrame, explode_columns: list):
    """
    멀티 컬럼 explode
    """
    list_columns = df.columns
    idx = df.index.repeat(df[explode_columns[0]].str.len())
    df1 = pd.concat([pd.DataFrame({x: np.concatenate(df[x].values)}) for x in explode_columns], axis=1)
    df1.index = idx
    result = df1.join(df.drop(explode_columns, 1), how="left").reset_index(drop=True)
    result = result[list_columns]
    return result
