"""
Abstract base class for a data model.

A data model holds either smlm_data, filter_specifications, regions
or other data structures.

The interface provides methods to manipulate the data contents.

"""

from __future__ import annotations

import logging
from abc import ABC, ABCMeta
from typing import Any

from qtpy.QtCore import QObject, Signal  # type: ignore[attr-defined]

logger = logging.getLogger(__name__)


class QABCMeta(type(QObject), ABCMeta):  # type: ignore[misc]
    # this is required to avoid metaclass conflicts with Qt metaclasses
    pass


class DataModel(QObject, ABC, metaclass=QABCMeta):  # type: ignore
    """
    Abstract base class for container classes holding various data structures.

    Attributes
    ----------
    count
        Monotonically increasing integer counting the overall created datasets.
    datasets_changed_signal
        A Qt signal for index
    names_changed_signal
        A Qt signal for names
    index_changed_signal
        A Qt signal for index
    datasets
        Data structures
    names
        Data structure string identifier
    index
        Current selection of data structure
    dataset
        The selected data object
    name
        The selected data identifier
    """

    count: int = 0

    datasets_changed_signal: Signal = Signal(int)
    names_changed_signal: Signal = Signal(list)
    index_changed_signal: Signal = Signal(int)

    def __init__(
        self,
        datasets: list[Any] | None = None,
        names: list[str] | None = None,
    ) -> None:
        super().__init__()
        self._datasets: list[Any] = []
        self._names: list[str] = []
        self._index: int = -1
        self.set_datasets_and_names(datasets=datasets, names=names)

    def __getstate__(self) -> dict[str, Any]:
        """Modify pickling behavior."""
        state: dict[str, Any] = {}
        state["count"] = self.count
        state["_datasets"] = self._datasets
        state["_names"] = self._names
        state["_index"] = self._index
        return state

    def __setstate__(self, state: dict[str, Any]) -> None:
        """Modify pickling behavior."""
        # Restore instance attributes.
        self.__dict__.update(state)
        super().__init__()

    @property
    def datasets(self) -> list[Any]:
        return self._datasets

    @property
    def names(self) -> list[str]:
        return self._names

    def set_datasets_and_names(
        self, datasets: list[Any] | None = None, names: list[str] | None = None
    ) -> None:
        """
        Set datasets and names to the given values and point index to the last item.
        """
        if datasets is None and names is None:
            self._datasets = []
            self._names = []
            self._index = -1
        elif names is None:
            assert datasets is not None  # type narrowing # noqa: S101
            self._datasets = datasets
            self._names = [str(i) for i, item in enumerate(self._datasets)]
            self._index = len(datasets) - 1
        elif datasets is not None and (len(datasets) != len(names)):
            raise ValueError(
                "Datasets and names must correspond and be of same length."
            )
        else:
            assert datasets is not None  # type narrowing # noqa: S101
            self._datasets = datasets
            self._names = names
            self._index = len(datasets) - 1

        self.count += len(self._datasets)

        self.datasets_changed_signal.emit(self._datasets)
        self.names_changed_signal.emit(self._names)
        self.index_changed_signal.emit(self._index)

    @property
    def index(self) -> int:
        return self._index

    @index.setter
    def index(self, value: int) -> None:
        if value > len(self.datasets) - 1:
            raise IndexError(
                f"Index is larger than n_datasets - 1: {len(self.datasets) - 1}"
            )
        elif value < 0:
            self._index = -1
        else:
            self._index = value
        self.index_changed_signal.emit(self._index)

    def set_index_slot(self, value: int) -> None:
        """QT slot for property self.index."""
        self.index = value

    @property
    def dataset(self) -> Any | None:
        if self._index == -1:
            return None
        else:
            return self._datasets[self._index]

    @dataset.setter
    def dataset(self, item: Any) -> None:
        if self._index == -1:
            raise ValueError(
                "Datasets is empty. "
                "There is no item available to be replaced."
                "Use self.append_item instead."
            )
        else:
            self._datasets[self._index] = item
            self.count += 1
        self.datasets_changed_signal.emit(self._datasets)
        self.index_changed_signal.emit(self._index)

    @property
    def name(self) -> str:
        if self._index == -1:
            return ""
        else:
            return self._names[self._index]

    @name.setter
    def name(self, text: str) -> None:
        if self._index == -1:
            raise ValueError(
                "names is empty. "
                "There is no item available to be replaced."
                "Use self.append_item instead."
            )
        else:
            self._names[self._index] = text
        self.names_changed_signal.emit(self._names)

    def append_item(
        self,
        dataset: Any | None,
        name: str | None = None,
        set_index: bool = True,
    ) -> None:
        """
        Append a new item to the end of datasets and point index to new dataset
        if set_index is true.
        """
        current_index = self.index
        if dataset is None and name is None:
            return
        elif name is None:
            assert dataset is not None  # type narrowing # noqa: S101
            self._datasets.append(dataset)
            identifier = f"{len(self._datasets)}"
            self._names.append(identifier)
        else:
            assert dataset is not None  # type narrowing # noqa: S101
            assert name is not None  # type narrowing # noqa: S101
            self._datasets.append(dataset)
            self._names.append(name)
        if set_index:
            self._index = len(self.datasets) - 1
        else:
            self._index = current_index
        self.count += 1
        self.datasets_changed_signal.emit(self.datasets)
        self.names_changed_signal.emit(self.names)
        self.index_changed_signal.emit(self.index)

    def delete_item(self) -> None:
        """
        Delete current dataset and set index to the previous dataset.
        """
        current_index = self.index
        try:
            self._datasets.pop(current_index)
            self._names.pop(current_index)
        except IndexError as exception:
            raise IndexError(
                "Index is out of range. No item available to be deleted."
            ) from exception

        if len(self._datasets) == 0:
            self._index = -1
        elif current_index == 0:
            self._index = 0
        else:
            self._index = current_index - 1

        self.names_changed_signal.emit(self.names)
        self.index_changed_signal.emit(self.index)

    def delete_all(self) -> None:
        """
        Delete all datasets and set index to -1.
        """
        self._datasets = []
        self._names = []
        self._index = -1
        self.names_changed_signal.emit(self.names)
        self.index_changed_signal.emit(self.index)
