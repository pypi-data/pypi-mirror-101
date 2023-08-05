from typing import Dict, Optional, Union

import numpy as np
import pandas as pd

from aporia.core.context import get_context
from aporia.core.errors import AporiaError, handle_error
from aporia.core.types.field import FieldType, FieldValue

# This is based on https://numpy.org/doc/stable/reference/generated/numpy.dtype.kind.html#numpy.dtype.kind
DTYPE_TO_FIELD_TYPE = {
    "b": FieldType.BOOLEAN,
    "i": FieldType.NUMERIC,
    "u": FieldType.NUMERIC,
    "f": FieldType.NUMERIC,
    "M": FieldType.DATETIME,
    "O": FieldType.STRING,
    "S": FieldType.STRING,
    "U": FieldType.STRING,
}


def convert_dtype_to_field_type(dtype: np.dtype) -> Optional[FieldType]:
    """Attempts to convert a numpy/pandas dtype to a FieldType.

    Args:
        dtype: Dtype to convert

    Returns:
        FieldType that matches the dtype, or None if conversion is impossible
    """
    if isinstance(dtype, pd.api.types.CategoricalDtype):
        category_type = DTYPE_TO_FIELD_TYPE.get(dtype.categories.dtype.kind)
        # We only support categorical fields with numeric categories
        if category_type == FieldType.NUMERIC:
            return FieldType.CATEGORICAL

        return category_type

    return DTYPE_TO_FIELD_TYPE.get(dtype.kind)  # type: ignore


def pandas_to_dict(data: Union[pd.DataFrame, pd.Series]) -> Optional[Dict[str, FieldValue]]:
    """Converts a pandas DataFrame or Series to a dict for log_* functions.

    Args:
        data: DataFrame or Series to convert.

    Returns:
        The data converted to a dict, mapping field names to their values

    Notes:
        * data must contain column names that match the fields defined in create_model_version
        * If data is a DataFrame, it must contain exactly one row
    """
    context = None
    try:
        context = get_context()

        if isinstance(data, pd.Series):
            return data.to_dict()
        elif isinstance(data, pd.DataFrame):
            num_rows, _ = data.shape
            if num_rows > 1:
                raise AporiaError("cannot convert DataFrame with more than 1 row")

            return data.iloc[0].to_dict()
        else:
            raise AporiaError("data must be a pandas DataFrame or Series")

    except Exception as err:
        handle_error(
            message_format="Converting pandas data to dict failed, {}",
            verbose=False if context is None else context.config.verbose,
            throw_errors=False if context is None else context.config.throw_errors,
            debug=False if context is None else context.config.debug,
            original_exception=err,
        )

    return None


def infer_schema_from_dataframe(data: pd.DataFrame) -> Optional[Dict[str, str]]:
    """Infers model version schema from a pandas DataFrame or Series.

    Field names and types are inferred from column names and types.

    Args:
        data: pandas DataFrame or Series

    Returns:
        A schema describing the data, as required by the create_model_version function.

    Notes:
        * The field types are inferred using the following logic, based on the column dtypes:
            * dtype="category" with numeric (integer of float) categories -> categorical field
            * dtype="category" with non-numeric categories -> See rules below
            * dtype="bool" -> boolean field
            * dtypes that represent signed/unsigned integers and floating point numbers -> numeric field
            * dtype is "string", "unicode", "object" -> string field
            * dtype is any datetime type (with or without timezone) -> datetime field
        * If data contains a column with a type that doesn't match any of the rules
          described above, an error will be raised.
    """
    context = get_context()
    try:
        if not isinstance(data, pd.DataFrame):
            raise AporiaError(
                "cannot infer schema from {}, data must be a pandas DataFrame".format(type(data))
            )

        schema = {}
        for column_name, values in data.items():
            values_without_nulls = values.dropna().infer_objects()
            column_type = convert_dtype_to_field_type(values_without_nulls.dtype)
            if column_type is None:
                raise AporiaError(
                    "the dtype {} of column {} is not supported".format(
                        values_without_nulls.dtype, column_name
                    )
                )

            schema[column_name] = column_type.value

        return schema

    except Exception as err:
        handle_error(
            message_format="Inferring schema from dataframe failed, {}",
            verbose=context.config.verbose,
            throw_errors=context.config.throw_errors,
            debug=context.config.debug,
            original_exception=err,
        )

    return None
